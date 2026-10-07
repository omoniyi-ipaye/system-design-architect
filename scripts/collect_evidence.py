#!/usr/bin/env python3
"""Collect read-only operational evidence and render a bounded health report.

Supported adapters are generic JSON files, generic HTTP JSON endpoints, and
Prometheus-compatible query_range APIs. The collector never executes a response
plan; it reports observed signals separately from explicitly labelled inferences.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import html
import json
import math
import os
from pathlib import Path
import statistics
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

MAX_RESPONSE_BYTES = 5 * 1024 * 1024
STATISTICS = {"mean", "median", "min", "max", "last", "p95"}
OPERATORS = {"gt", "gte", "lt", "lte", "eq", "ne"}


def iso_now(value: datetime | None = None) -> str:
    value = value or datetime.now(timezone.utc)
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_time(value: Any) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("timestamp must be a non-empty ISO 8601 string")
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("timestamp must be ISO 8601") from exc
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return parsed.astimezone(timezone.utc)


def extract_path(value: Any, dotted_path: str) -> Any:
    current = value
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise ValueError(f"configured data path is missing: {dotted_path}")
        current = current[part]
    return current


def scalar(value: Any, label: str) -> str | int | float | bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{label} must be finite")
        return value
    if isinstance(value, str) and value.strip() and len(value) <= 256:
        return value.strip()
    raise ValueError(f"{label} must be a scalar value")


def validate_endpoint(endpoint: str, allow_insecure_http: bool = False) -> None:
    parsed = urlparse(endpoint)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("source endpoint must be an absolute HTTP(S) URL")
    if parsed.username or parsed.password or parsed.fragment or parsed.query:
        raise ValueError("source endpoint must not contain credentials, a query, or a fragment")
    local_hosts = {"localhost", "127.0.0.1", "::1"}
    if parsed.scheme == "http" and parsed.hostname not in local_hosts and not allow_insecure_http:
        raise ValueError("HTTP source endpoints must use HTTPS, unless allow_insecure_http is explicitly enabled")


class SameOriginRedirectHandler(HTTPRedirectHandler):
    """Prevent an authenticated evidence request from following a cross-origin redirect."""

    def redirect_request(self, request: Request, fp: Any, code: int, message: str, headers: Any, new_url: str) -> Request | None:
        old = urlparse(request.full_url)
        new = urlparse(new_url)
        if (old.scheme, old.hostname, old.port) != (new.scheme, new.hostname, new.port):
            raise ValueError("cross-origin redirects are blocked for evidence sources")
        return super().redirect_request(request, fp, code, message, headers, new_url)


def open_readonly(request: Request, timeout: int) -> Any:
    return build_opener(SameOriginRedirectHandler()).open(request, timeout=timeout)


def auth_headers(source: dict[str, Any], endpoint: str) -> dict[str, str]:
    auth = source.get("auth_env")
    if not auth:
        return {}
    if not isinstance(auth, dict) or not auth.get("variable") or not auth.get("header"):
        raise ValueError("auth_env needs variable and header fields")
    parsed = urlparse(endpoint)
    if parsed.scheme != "https" and parsed.hostname not in {"localhost", "127.0.0.1", "::1"} and not source.get("allow_insecure_http"):
        raise ValueError("refusing to send an environment credential over insecure HTTP")
    value = os.environ.get(str(auth["variable"]))
    if not value:
        raise ValueError(f"required credential environment variable is not set: {auth['variable']}")
    prefix = str(auth.get("prefix", ""))
    return {str(auth["header"]): prefix + value}


def fetch_json_url(url: str, source: dict[str, Any], timeout: int) -> Any:
    validate_endpoint(url, bool(source.get("allow_insecure_http")))
    headers = {"Accept": "application/json", "User-Agent": "system-design-architect-evidence/1.0"}
    headers.update(auth_headers(source, url))
    request = Request(url, headers=headers, method="GET")
    try:
        with open_readonly(request, timeout) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise ValueError("source response exceeded the 5 MiB limit")
            if response.status < 200 or response.status >= 300:
                raise ValueError(f"source returned HTTP {response.status}")
    except HTTPError as exc:
        raise ValueError(f"source returned HTTP {exc.code}") from exc
    except URLError as exc:
        # Avoid printing the full URL; it can contain sensitive query parameters.
        raise ValueError(f"source request failed ({type(exc.reason).__name__})") from exc
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("source did not return valid UTF-8 JSON") from exc


def load_source_payload(source: dict[str, Any], config_path: Path, timeout: int) -> Any:
    adapter = source["adapter"]
    if adapter == "json_file":
        path = Path(source["path"])
        if not path.is_absolute():
            path = config_path.parent / path
        try:
            if path.stat().st_size > MAX_RESPONSE_BYTES:
                raise ValueError("source file exceeded the 5 MiB limit")
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError("could not read configured JSON evidence file") from exc
    if adapter == "http_json":
        return fetch_json_url(str(source["endpoint"]), source, timeout)
    raise ValueError(f"unsupported JSON adapter: {adapter}")


def reduce_values(values: list[float], method: str) -> float:
    if not values:
        raise ValueError("no numeric samples available")
    if method == "mean":
        return statistics.fmean(values)
    if method == "median":
        return statistics.median(values)
    if method == "min":
        return min(values)
    if method == "max":
        return max(values)
    if method == "last":
        return values[-1]
    if method == "p95":
        ordered = sorted(values)
        return ordered[max(0, math.ceil(0.95 * len(ordered)) - 1)]
    raise ValueError(f"unsupported statistic: {method}")


def prometheus_points(source: dict[str, Any], query: str, start: datetime, end: datetime, timeout: int) -> list[tuple[float, float]]:
    endpoint = str(source["endpoint"]).rstrip("/")
    validate_endpoint(endpoint, bool(source.get("allow_insecure_http")))
    url = endpoint + "/api/v1/query_range?" + urlencode({
        "query": query,
        "start": start.timestamp(),
        "end": end.timestamp(),
        "step": int(source.get("step_seconds", 60)),
    })
    headers = {"Accept": "application/json", "User-Agent": "system-design-architect-evidence/1.0"}
    headers.update(auth_headers(source, endpoint))
    request = Request(url, headers=headers, method="GET")
    try:
        with open_readonly(request, timeout) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise ValueError("Prometheus response exceeded the 5 MiB limit")
    except HTTPError as exc:
        raise ValueError(f"Prometheus source returned HTTP {exc.code}") from exc
    except URLError as exc:
        raise ValueError(f"Prometheus request failed ({type(exc.reason).__name__})") from exc
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Prometheus source did not return valid UTF-8 JSON") from exc
    if not isinstance(data, dict) or data.get("status") != "success":
        raise ValueError("Prometheus query did not succeed")
    results = data.get("data", {}).get("result")
    if not isinstance(results, list) or not results:
        return []
    if len(results) > 1 and not source.get("series_reduce"):
        raise ValueError("Prometheus query returned multiple series; configure series_reduce or aggregate in PromQL")
    grouped: dict[float, list[float]] = {}
    for series in results:
        for point in series.get("values", []):
            if not isinstance(point, list) or len(point) != 2:
                continue
            try:
                timestamp, value = float(point[0]), float(point[1])
            except (TypeError, ValueError):
                continue
            if math.isfinite(timestamp) and math.isfinite(value):
                grouped.setdefault(timestamp, []).append(value)
    series_reduce = source.get("series_reduce", "mean")
    if series_reduce not in {"sum", "mean", "min", "max", "median"}:
        raise ValueError("series_reduce must be sum, mean, min, max, or median")
    points: list[tuple[float, float]] = []
    for timestamp in sorted(grouped):
        values = grouped[timestamp]
        if series_reduce == "sum":
            value = sum(values)
        else:
            value = reduce_values(values, series_reduce)
        points.append((timestamp, value))
    return points


def collect_prometheus_signal(source: dict[str, Any], signal: dict[str, Any], now: datetime, timeout: int) -> dict[str, Any]:
    current_seconds = int(signal.get("current_window_seconds", source.get("current_window_seconds", 3600)))
    baseline_seconds = int(signal.get("baseline_window_seconds", source.get("baseline_window_seconds", 604800)))
    start = now - timedelta(seconds=current_seconds + baseline_seconds)
    points = prometheus_points(source, str(signal["query"]), start, now, timeout)
    current_start = now.timestamp() - current_seconds
    baseline_points = [value for ts, value in points if ts < current_start]
    current_points = [(ts, value) for ts, value in points if ts >= current_start]
    if not current_points:
        raise ValueError("Prometheus query returned no samples in the current window")
    current_stat = str(signal.get("current_statistic", "last"))
    baseline_stat = str(signal.get("baseline_statistic", "median"))
    current_value = reduce_values([value for _, value in current_points], current_stat)
    baseline_value = reduce_values(baseline_points, baseline_stat) if baseline_points else None
    observed_at = datetime.fromtimestamp(max(ts for ts, _ in current_points), timezone.utc)
    return {
        "current_value": current_value,
        "baseline_value": baseline_value,
        "observed_at": iso_now(observed_at),
        "timestamp_source": "prometheus_sample",
        "baseline_window": f"previous {baseline_seconds}s",
        "current_window": f"previous {current_seconds}s",
        "baseline_sample_count": len(baseline_points),
        "current_sample_count": len(current_points),
        "baseline_statistic": baseline_stat,
        "current_statistic": current_stat,
    }


def validate_config(config: Any) -> None:
    if not isinstance(config, dict) or config.get("schema_version") != "1.0":
        raise ValueError("config must be an object with schema_version 1.0")
    system = config.get("system")
    if not isinstance(system, dict) or not all(system.get(k) for k in ("id", "name", "intended_outcome")):
        raise ValueError("system needs id, name, and intended_outcome")
    sources = config.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("config needs at least one source")
    ids: set[str] = set()
    signal_ids: set[str] = set()
    for source in sources:
        if not isinstance(source, dict) or not source.get("id"):
            raise ValueError("every source needs an id")
        source_id = str(source["id"])
        if source_id in ids:
            raise ValueError(f"duplicate source id: {source_id}")
        ids.add(source_id)
        adapter = source.get("adapter")
        if adapter not in {"json_file", "http_json", "prometheus"}:
            raise ValueError(f"unsupported adapter for source {source_id}")
        if adapter == "json_file" and not source.get("path"):
            raise ValueError(f"JSON file source {source_id} needs path")
        if adapter in {"http_json", "prometheus"} and not source.get("endpoint"):
            raise ValueError(f"HTTP source {source_id} needs endpoint")
        signals = source.get("signals")
        if not isinstance(signals, list) or not signals:
            raise ValueError(f"source {source_id} needs at least one signal")
        for signal in signals:
            if not isinstance(signal, dict) or not all(signal.get(k) for k in ("id", "name", "unit")):
                raise ValueError(f"every signal in {source_id} needs id, name, and unit")
            signal_id = str(signal["id"])
            if signal_id in signal_ids:
                raise ValueError(f"duplicate signal id: {signal_id}")
            signal_ids.add(signal_id)
            if adapter in {"json_file", "http_json"} and not signal.get("current_path"):
                raise ValueError(f"JSON signal {signal_id} needs current_path")
            if adapter == "prometheus" and not signal.get("query"):
                raise ValueError(f"Prometheus signal {signal_id} needs query")
            threshold = signal.get("threshold")
            if threshold is None and not signal.get("monitor_only", False):
                raise ValueError(f"signal {signal_id} needs an explicit threshold or monitor_only: true")
            if threshold is not None and (not isinstance(threshold, dict) or threshold.get("op") not in OPERATORS or "value" not in threshold):
                raise ValueError(f"signal {signal_id} has an invalid threshold")
            if int(signal.get("max_age_seconds", 86400)) < 1:
                raise ValueError(f"signal {signal_id} max_age_seconds must be positive")
    rule_ids: set[str] = set()
    for rule in config.get("diagnosis_rules", []):
        if not isinstance(rule, dict) or not rule.get("id") or not isinstance(rule.get("when"), list) or not rule["when"]:
            raise ValueError("each diagnosis rule needs id and non-empty when conditions")
        if str(rule["id"]) in rule_ids:
            raise ValueError(f"duplicate diagnosis rule id: {rule['id']}")
        rule_ids.add(str(rule["id"]))
        for condition in rule["when"]:
            if not isinstance(condition, dict) or condition.get("signal_id") not in signal_ids or condition.get("status") not in {"breach", "ok", "monitored"}:
                raise ValueError(f"diagnosis rule {rule['id']} references an invalid signal or status")
        if rule.get("confidence", "low") not in {"low", "medium", "high"}:
            raise ValueError(f"diagnosis rule {rule['id']} has invalid confidence")
        response = rule.get("response", {})
        if not isinstance(response, dict):
            raise ValueError(f"diagnosis rule {rule['id']} response must be an object")
        if response.get("auto_execute", False) is not False:
            raise ValueError("operational evidence reports may only recommend responses; auto_execute must be false")
        if "reversible" in response and not isinstance(response["reversible"], bool):
            raise ValueError(f"diagnosis rule {rule['id']} response reversible must be boolean")
    if not isinstance(config.get("diagnosis_rules", []), list):
        raise ValueError("diagnosis_rules must be an array")


def compare_threshold(value: Any, threshold: dict[str, Any] | None) -> str:
    if threshold is None:
        return "monitored"
    target = threshold["value"]
    if isinstance(value, bool) or isinstance(target, bool):
        comparable = value == target if threshold["op"] == "eq" else value != target if threshold["op"] == "ne" else None
    elif isinstance(value, (int, float)) and isinstance(target, (int, float)):
        comparable = {
            "gt": value > target,
            "gte": value >= target,
            "lt": value < target,
            "lte": value <= target,
            "eq": value == target,
            "ne": value != target,
        }[threshold["op"]]
    elif isinstance(value, str) and isinstance(target, str):
        comparable = value == target if threshold["op"] == "eq" else value != target if threshold["op"] == "ne" else None
    else:
        comparable = None
    if comparable is None:
        raise ValueError("threshold operator and observed value have incompatible types")
    return "ok" if comparable else "breach"


def collect_report(config: dict[str, Any], config_path: Path, timeout: int = 10, now: datetime | None = None) -> dict[str, Any]:
    validate_config(config)
    now = now or datetime.now(timezone.utc)
    now = now.astimezone(timezone.utc)
    collected_at = iso_now(now)
    raw_signals: dict[str, dict[str, Any]] = {}
    sources_report: list[dict[str, Any]] = []
    source_errors: list[dict[str, str]] = []

    for source in config["sources"]:
        source_record = {"id": str(source["id"]), "adapter": source["adapter"], "status": "collected"}
        sources_report.append(source_record)
        try:
            source_timeout = int(source.get("timeout_seconds", timeout))
            if source_timeout < 1 or source_timeout > 120:
                raise ValueError("source timeout_seconds must be between 1 and 120")
            if source["adapter"] == "prometheus":
                for signal in source["signals"]:
                    raw_signals[str(signal["id"])] = collect_prometheus_signal(source, signal, now, source_timeout)
            else:
                payload = load_source_payload(source, config_path, source_timeout)
                for signal in source["signals"]:
                    current = scalar(extract_path(payload, signal["current_path"]), f"{signal['id']} current value")
                    baseline = None
                    if signal.get("baseline_path"):
                        baseline = scalar(extract_path(payload, signal["baseline_path"]), f"{signal['id']} baseline value")
                    timestamp_source = "collector"
                    observed_at = collected_at
                    if signal.get("observed_at_path"):
                        observed_at = iso_now(parse_time(extract_path(payload, signal["observed_at_path"])))
                        timestamp_source = "source"
                    elif source.get("generated_at_path"):
                        observed_at = iso_now(parse_time(extract_path(payload, source["generated_at_path"])))
                        timestamp_source = "source"
                    raw_signals[str(signal["id"])] = {
                        "current_value": current,
                        "baseline_value": baseline,
                        "observed_at": observed_at,
                        "timestamp_source": timestamp_source,
                        "baseline_window": signal.get("baseline_window", "source-provided baseline"),
                        "current_window": signal.get("current_window", "current source value"),
                        "baseline_sample_count": extract_path(payload, signal["baseline_sample_count_path"]) if signal.get("baseline_sample_count_path") else None,
                    }
        except (ValueError, KeyError, OSError, TypeError) as exc:
            source_record["status"] = "unavailable"
            source_errors.append({"source_id": str(source["id"]), "adapter": source["adapter"], "message": str(exc)[:300]})
            for signal in source["signals"]:
                raw_signals.setdefault(str(signal["id"]), {"error": str(exc)})

    observations: list[dict[str, Any]] = []
    baselines: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []
    signal_config: dict[str, dict[str, Any]] = {}
    for source in config["sources"]:
        for signal in source["signals"]:
            signal_id = str(signal["id"])
            signal_config[signal_id] = signal
            collected = raw_signals.get(signal_id, {"error": "no evidence returned"})
            if "error" in collected:
                checks.append({
                    "signal_id": signal_id,
                    "name": signal["name"],
                    "status": "unavailable",
                    "freshness": "unavailable",
                    "source_id": str(source["id"]),
                    "adapter": source["adapter"],
                    "message": collected["error"],
                    "threshold": signal.get("threshold"),
                })
                continue
            observation_id = f"obs:{signal_id}"
            observed_at = parse_time(collected["observed_at"])
            age_seconds = max(0, int((now - observed_at).total_seconds()))
            max_age = int(signal.get("max_age_seconds", 86400))
            freshness = "stale" if age_seconds > max_age else "fresh"
            observation = {
                "id": observation_id,
                "signal_id": signal_id,
                "name": str(signal["name"]),
                "value": collected["current_value"],
                "unit": str(signal["unit"]),
                "observed_at": collected["observed_at"],
                "timestamp_source": collected["timestamp_source"],
                "window": collected.get("current_window"),
                "evidence_state": "observed",
                "source": {"id": str(source["id"]), "adapter": source["adapter"]},
            }
            observations.append(observation)
            baseline_id = None
            baseline_value = collected.get("baseline_value")
            if baseline_value is not None:
                baseline_id = f"base:{signal_id}"
                baselines.append({
                    "id": baseline_id,
                    "signal_id": signal_id,
                    "value": baseline_value,
                    "unit": str(signal["unit"]),
                    "window": collected.get("baseline_window"),
                    "sample_count": collected.get("baseline_sample_count"),
                    "statistic": collected.get("baseline_statistic", "source-reported"),
                    "evidence_state": "observed",
                    "source": {"id": str(source["id"]), "adapter": source["adapter"]},
                })
            status = "stale" if freshness == "stale" else compare_threshold(collected["current_value"], signal.get("threshold"))
            delta = None
            if isinstance(baseline_value, (int, float)) and not isinstance(baseline_value, bool) and isinstance(collected["current_value"], (int, float)) and not isinstance(collected["current_value"], bool):
                delta = {
                    "absolute": collected["current_value"] - baseline_value,
                    "percent": ((collected["current_value"] - baseline_value) / abs(baseline_value) * 100) if baseline_value else None,
                }
            checks.append({
                "signal_id": signal_id,
                "name": str(signal["name"]),
                "observation_id": observation_id,
                "baseline_id": baseline_id,
                "observed_value": collected["current_value"],
                "baseline_value": baseline_value,
                "delta": delta,
                "unit": str(signal["unit"]),
                "threshold": signal.get("threshold"),
                "status": status,
                "freshness": freshness,
                "age_seconds": age_seconds,
                "max_age_seconds": max_age,
                "source_id": str(source["id"]),
                "adapter": source["adapter"],
            })

    check_by_signal = {item["signal_id"]: item for item in checks}
    diagnoses: list[dict[str, Any]] = []
    response_plan: list[dict[str, Any]] = []
    for rule in config.get("diagnosis_rules", []):
        if not all(
            check_by_signal.get(condition["signal_id"], {}).get("freshness") == "fresh"
            and check_by_signal.get(condition["signal_id"], {}).get("status") == condition["status"]
            for condition in rule["when"]
        ):
            continue
        evidence = []
        for condition in rule["when"]:
            check = check_by_signal[condition["signal_id"]]
            evidence.append({
                "signal_id": condition["signal_id"],
                "observed_value": check.get("observed_value"),
                "baseline_value": check.get("baseline_value"),
                "threshold": check.get("threshold"),
                "status": check["status"],
            })
        diagnosis_id = f"diagnosis:{rule['id']}"
        diagnoses.append({
            "id": diagnosis_id,
            "title": str(rule.get("title", rule["id"])),
            "classification": str(rule.get("classification", "system_health")),
            "claim": str(rule.get("claim", "")),
            "evidence_state": "inferred",
            "confidence": str(rule.get("confidence", "low")),
            "supporting_evidence": evidence,
            "limitations": str(rule.get("limitations", "This is a hypothesis from the configured signals; it does not establish causality.")),
        })
        response = rule.get("response", {})
        response_plan.append({
            "id": f"response:{rule['id']}",
            "diagnosis_id": diagnosis_id,
            "action": str(response.get("action", "Review the evidence and decide on a bounded response.")),
            "authority": str(response.get("authority", "A named human system owner")),
            "authorization_required": True,
            "auto_execute": False,
            "reversible": bool(response.get("reversible", True)),
            "max_blast_radius": str(response.get("max_blast_radius", "One case or one bounded operating unit")),
            "verification": str(response.get("verification", "Re-read the source signals and confirm the intended outcome.")),
            "escalation": str(response.get("escalation", "Escalate when evidence is stale, the cause is uncertain, or the action exceeds the approved boundary.")),
        })

    if any(item["status"] == "breach" for item in checks):
        overall_status = "attention"
    elif any(item["status"] in {"stale", "unavailable", "monitored"} for item in checks):
        overall_status = "insufficient_evidence"
    else:
        overall_status = "healthy"
    return {
        "schema_version": "1.0",
        "system": config["system"],
        "collected_at": collected_at,
        "status": overall_status,
        "sources": sources_report,
        "source_errors": source_errors,
        "observations": observations,
        "baselines": baselines,
        "checks": checks,
        "diagnoses": diagnoses,
        "response_plan": response_plan,
        "actions_executed": [],
        "authority_boundary": "Evidence collection and detection do not authorize action. All response plans require human approval.",
    }


def show_value(value: Any, unit: str = "") -> str:
    if isinstance(value, float):
        value = f"{value:.2f}".rstrip("0").rstrip(".")
    return f"{html.escape(str(value))}{html.escape((' ' + unit) if unit else '')}"


def render_html(report: dict[str, Any]) -> str:
    system = report["system"]
    status = report["status"]
    status_label = status.replace("_", " ").title()
    check_rows = []
    for check in report["checks"]:
        threshold = check.get("threshold")
        threshold_text = "No threshold configured"
        if threshold:
            symbol = {"gt": ">", "gte": "≥", "lt": "<", "lte": "≤", "eq": "=", "ne": "≠"}.get(threshold["op"], threshold["op"])
            threshold_text = f"{symbol} {show_value(threshold['value'], check.get('unit', ''))}"
        current = "Unavailable" if "observed_value" not in check else show_value(check["observed_value"], check.get("unit", ""))
        baseline = "—" if check.get("baseline_value") is None else show_value(check["baseline_value"], check.get("unit", ""))
        delta = check.get("delta")
        change_text = "—"
        if delta:
            change_text = show_value(delta["absolute"], check.get("unit", ""))
            if delta.get("percent") is not None:
                change_text += f" ({delta['percent']:+.1f}%)"
        row_status = html.escape(str(check.get("status", "unknown")).replace("_", " ").title())
        check_rows.append(
            "<tr>"
            f"<td><strong>{html.escape(str(check['name']))}</strong><small>{html.escape(str(check['source_id']))} · {html.escape(str(check['adapter']))}</small></td>"
            f"<td>{current}</td><td>{baseline}</td><td>{html.escape(threshold_text)}</td>"
            f"<td>{html.escape(change_text)}</td><td><span class=\"pill {html.escape(str(check.get('status', 'unknown')))}\">{row_status}</span></td>"
            "</tr>"
        )
    diagnosis_cards = []
    for diagnosis in report["diagnoses"]:
        proof = "".join(
            f"<li><strong>{html.escape(str(item['signal_id']))}:</strong> {show_value(item.get('observed_value'))} (baseline {show_value(item.get('baseline_value'))}); status {html.escape(str(item['status']))}</li>"
            for item in diagnosis["supporting_evidence"]
        )
        diagnosis_cards.append(
            "<article class=\"panel diagnosis\">"
            f"<div class=\"eyebrow\">INFERENCE · {html.escape(str(diagnosis['confidence']).upper())} CONFIDENCE</div>"
            f"<h3>{html.escape(str(diagnosis['title']))}</h3>"
            f"<p>{html.escape(str(diagnosis['claim']))}</p><ul>{proof}</ul>"
            f"<p class=\"muted\">Limit: {html.escape(str(diagnosis['limitations']))}</p></article>"
        )
    if not diagnosis_cards:
        diagnosis_cards = ["<article class=\"panel\"><h3>No diagnosis rule matched</h3><p>Signals are shown without inventing a cause.</p></article>"]
    response_cards = []
    for response in report["response_plan"]:
        response_cards.append(
            "<article class=\"panel response\">"
            f"<div class=\"eyebrow\">HUMAN-AUTHORIZED RESPONSE</div><h3>{html.escape(str(response['action']))}</h3>"
            f"<p><strong>Authority:</strong> {html.escape(str(response['authority']))}</p>"
            f"<p><strong>Boundary:</strong> limited to {html.escape(str(response['max_blast_radius']))}; reversible={str(response['reversible']).lower()}</p>"
            f"<p><strong>Verify:</strong> {html.escape(str(response['verification']))}</p>"
            f"<p><strong>Escalate:</strong> {html.escape(str(response['escalation']))}</p></article>"
        )
    if not response_cards:
        response_cards = ["<article class=\"panel\"><h3>No response required</h3><p>There is no matched, evidence-backed response rule.</p></article>"]
    source_errors = "".join(
        f"<li>{html.escape(item['source_id'])}: {html.escape(item['message'])}</li>"
        for item in report["source_errors"]
    )
    errors_block = f"<aside class=\"warning\"><strong>Evidence gaps</strong><ul>{source_errors}</ul></aside>" if source_errors else ""
    classification = system.get("data_classification", "Operational evidence")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(str(system['name']))} · System Health</title>
<style>
:root{{--ink:#18242e;--muted:#5b6a73;--line:#dce5e9;--paper:#f4f8f8;--teal:#116b66;--mint:#dff2ed;--amber:#a66100;--amber-bg:#fff3dc;--red:#a93e36;--red-bg:#fde9e6;--white:#fff}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.wrap{{max-width:1120px;margin:auto;padding:38px 28px 56px}}.top{{display:flex;align-items:flex-start;justify-content:space-between;gap:24px}}.brand{{color:var(--teal);font-weight:750;letter-spacing:.12em;text-transform:uppercase;font-size:11px}}h1{{font-size:clamp(30px,5vw,48px);line-height:1.08;letter-spacing:-.04em;margin:12px 0}}.lede{{max-width:690px;color:var(--muted);font-size:17px}}.badge{{padding:10px 14px;border-radius:999px;font-weight:700;background:var(--mint);color:var(--teal);white-space:nowrap}}.badge.attention{{background:var(--amber-bg);color:var(--amber)}}.badge.insufficient_evidence{{background:#e8edf0;color:#52616b}}
.meta{{margin-top:15px;color:var(--muted);font-size:12px}}.flow{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:32px 0}}.flow div{{background:var(--white);border:1px solid var(--line);border-radius:14px;padding:15px;position:relative}}.flow strong{{display:block;color:var(--teal);font-size:13px}}.flow span{{color:var(--muted);font-size:12px}}.flow div:not(:last-child):after{{content:"→";position:absolute;right:-13px;top:20px;color:var(--teal);font-weight:800;z-index:2}}
h2{{font-size:21px;letter-spacing:-.02em;margin:34px 0 12px}}.panel{{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:20px;margin:12px 0}}.table-wrap{{overflow-x:auto;background:var(--white);border:1px solid var(--line);border-radius:16px}}table{{border-collapse:collapse;width:100%;min-width:790px}}th,td{{text-align:left;padding:15px;border-bottom:1px solid var(--line);vertical-align:top}}th{{font-size:11px;color:var(--muted);letter-spacing:.08em;text-transform:uppercase}}td small{{display:block;color:var(--muted);margin-top:4px}}tr:last-child td{{border-bottom:0}}.pill{{display:inline-block;padding:4px 8px;border-radius:999px;background:var(--mint);color:var(--teal);font-size:11px;font-weight:800;text-transform:uppercase}}.pill.breach,.pill.attention{{background:var(--amber-bg);color:var(--amber)}}.pill.stale,.pill.unavailable{{background:var(--red-bg);color:var(--red)}}.eyebrow{{font-size:10px;color:var(--teal);font-weight:800;letter-spacing:.12em}}h3{{font-size:18px;line-height:1.25;margin:7px 0 9px}}p{{margin:7px 0}}ul{{padding-left:20px}}.muted{{color:var(--muted);font-size:13px}}.warning{{background:var(--amber-bg);border:1px solid #f2d69c;border-radius:12px;padding:16px;margin:18px 0}}.guardrail{{padding:18px 20px;background:#eaf3f2;border-radius:14px;margin-top:24px;color:#244f4c}}footer{{border-top:1px solid var(--line);margin-top:38px;padding-top:16px;color:var(--muted);font-size:12px}}
@media(max-width:700px){{.wrap{{padding:24px 16px}}.top{{display:block}}.badge{{display:inline-block;margin-top:12px}}.flow{{grid-template-columns:1fr 1fr}}.flow div:nth-child(2):after{{display:none}}}}
@media print{{body{{background:#fff}}.wrap{{padding:15mm}}.panel,.table-wrap,.flow div{{break-inside:avoid}}}}
</style></head><body><main class="wrap">
<div class="top"><div><div class="brand">System Design Architect · System Health</div><h1>{html.escape(str(system['name']))}</h1><p class="lede">{html.escape(str(system['intended_outcome']))}</p><div class="meta">{html.escape(str(classification))} · Evidence collected {html.escape(report['collected_at'])}</div></div><div class="badge {html.escape(status)}">{html.escape(status_label)}</div></div>
<section class="flow" aria-label="Health analysis flow"><div><strong>1 · Observe</strong><span>Read-only source adapters</span></div><div><strong>2 · Compare</strong><span>Freshness, baseline, explicit threshold</span></div><div><strong>3 · Diagnose</strong><span>Inference cites its evidence</span></div><div><strong>4 · Respond</strong><span>Human-authorized bounded plan</span></div></section>
{errors_block}
<h2>Signals and baselines</h2><div class="table-wrap"><table><thead><tr><th>Signal</th><th>Current</th><th>Baseline</th><th>Threshold</th><th>Change</th><th>State</th></tr></thead><tbody>{''.join(check_rows)}</tbody></table></div>
<h2>What the evidence may indicate</h2>{''.join(diagnosis_cards)}
<h2>Bounded response plan</h2>{''.join(response_cards)}
<div class="guardrail"><strong>Authority boundary:</strong> {html.escape(report['authority_boundary'])} No operational action was executed.</div>
<footer>Sources: {html.escape(', '.join(f"{s['id']} ({s['adapter']})" for s in report['sources']))}. This report separates observed values from inferred causes; thresholds and baselines should be reviewed with the system owner.</footer>
</main></body></html>"""


def write_outputs(report: dict[str, Any], json_out: Path | None, html_out: Path | None) -> None:
    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if html_out:
        html_out.parent.mkdir(parents=True, exist_ok=True)
        html_out.write_text(render_html(report), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, help="operational evidence adapter configuration JSON")
    parser.add_argument("--json-out", type=Path, help="write normalized health evidence JSON")
    parser.add_argument("--html-out", type=Path, help="write a self-contained visual health report")
    parser.add_argument("--timeout", type=int, default=10, help="per-source HTTP timeout in seconds")
    args = parser.parse_args()
    try:
        config_path = args.config.resolve()
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if args.timeout < 1 or args.timeout > 120:
            raise ValueError("timeout must be between 1 and 120 seconds")
        report = collect_report(config, config_path, timeout=args.timeout)
        write_outputs(report, args.json_out, args.html_out)
        if not args.json_out and not args.html_out:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f"Health report: {report['status']} · {len(report['observations'])} observed signals · {len(report['diagnoses'])} grounded inferences")
            if args.json_out:
                print(f"JSON: {args.json_out}")
            if args.html_out:
                print(f"HTML: {args.html_out}")
        return 0
    except (OSError, json.JSONDecodeError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

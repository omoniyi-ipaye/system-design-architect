# Operational Evidence Adapters

System Health mode can use read-only operational data through a small adapter contract. Adapters fetch evidence; they do not diagnose on their own and they never execute recovery actions. The collector normalizes the returned values, checks freshness and configured thresholds, compares a current window with a historical baseline, and renders observed signals separately from inferred explanations.

## Run a local health assessment

Create an adapter configuration and run:

```bash
python3 scripts/collect_evidence.py path/to/health-config.json \
  --json-out health-report.json \
  --html-out health-report.html
```

The collector uses only Python's standard library. It stores only configured scalar fields in the report, not the complete source payload. It omits endpoint URLs and credentials from the report. If a source cannot be read, it records the evidence gap and continues with other sources.

## Adapter types

### `http_json`

Performs a read-only `GET` against a JSON endpoint. Configure each signal with a dotted `current_path`, optional `baseline_path`, and optional timestamp paths. This can connect to an internal service, a ticket or case API that exposes aggregated counts, a device fleet summary, or an AI evaluation summary.

Use `auth_env` to name an environment variable holding an access token. The value is read at runtime and never written to logs or reports. HTTPS is required for remote endpoints. Plain HTTP is allowed for loopback endpoints; use `allow_insecure_http` only for a trusted private network.

### `prometheus`

Calls the Prometheus-compatible `query_range` API with the configured PromQL expression. Set explicit current and baseline windows. A query returning multiple time series must either aggregate in PromQL or configure `series_reduce` (`sum`, `mean`, `min`, `max`, or `median`). The default current statistic is the last sample; the default baseline statistic is the median.

Use aggregate queries that preserve privacy, such as a service-wide error rate or queue depth. Avoid querying or exporting individual employee, customer, or patient records.

See [`examples/health-demo/prometheus-config.example.json`](../examples/health-demo/prometheus-config.example.json) for a placeholder configuration. Replace the endpoint, metric names, time windows, and threshold with values approved by the service owner.

### `json_file`

Reads a JSON snapshot with the same dotted-path mapping as `http_json`. Use it for offline replay, a deterministic demo, or development. A file fixture is not evidence that a live production system is healthy.

## Configuration shape

The configuration contains:

- `system`: stable ID, name, and intended outcome;
- `sources`: adapter ID, endpoint or file, and signals to extract;
- each signal's `unit`, timestamp freshness limit, optional current and baseline paths/windows, and explicit threshold;
- `diagnosis_rules`: combinations of signal states, a clearly labelled inference, its evidence, and a bounded response plan.

Threshold operators are `gt`, `gte`, `lt`, `lte`, `eq`, and `ne`. A threshold is explicit and reviewable. `max_age_seconds` prevents stale evidence from triggering a diagnosis rule. JSON values are limited to scalars so an adapter cannot silently copy an unbounded record set into the report.

## Normalized evidence contract

`model/operational-evidence.schema.json` defines the report format:

- `observations` are source-backed values with source, timestamp, unit, and evidence state `observed`;
- `baselines` include a period/statistic when the source provides one;
- `checks` show freshness, threshold status, and delta from baseline;
- `diagnoses` are explicitly `inferred`, cite the signals that support them, and include limitations;
- `response_plan` names the authority, blast radius, reversibility, verification, and escalation rule;
- `actions_executed` is always empty. Collection and detection never authorize response.

Do not present a correlation as cause. If a signal is stale or unavailable, surface the gap and withhold diagnoses that depend on it. Compare the result with the system's actual desired outcomes and fitness criteria before recommending a structural change.

## Extending the contract

An adapter should implement a narrow read-only fetch operation and map its result into the normalized observation shape. Keep vendor-specific authentication, pagination, timestamps, and rate limits inside the adapter. Keep system meaning, thresholds, diagnosis rules, privacy boundaries, and action authority in explicit configuration owned by the system owner.

For a new provider, document the returned fields, timestamp semantics, aggregation, baseline method, freshness behavior, error behavior, credential source, privacy limits, and safe retry policy. Never allow a source adapter to change policy or dispatch a recovery action.

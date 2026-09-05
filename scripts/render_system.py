#!/usr/bin/env python3
"""Render canonical System Design Architect JSON into a self-contained HTML visual report."""
from __future__ import annotations
from pathlib import Path
import argparse
import html
import json
import math

STAGES = ("as_is", "transition", "target")
STAGE_LABELS = {"as_is": "AS-IS", "transition": "TRANSITION", "target": "TARGET"}


def esc(value) -> str:
    return html.escape(str(value if value is not None else ""))


def load_model(path: Path) -> dict:
    model = json.loads(path.read_text(encoding="utf-8"))
    for key in ("schema_version", "system", "elements", "flows"):
        if key not in model:
            raise SystemExit(f"Model missing required key: {key}")
    return model


def badge(text: str, cls: str = "") -> str:
    return f'<span class="badge {cls}">{esc(text)}</span>'


def render_summary(model: dict) -> str:
    s = model["system"]
    outcomes = "".join(
        f"<li>{esc(x.get('text'))} {badge(x.get('evidence', ''))}</li>"
        for x in s.get("desired_outcomes", [])
    )
    return f"""
<section class="summary">
  <div class="eyebrow">Canonical system model · schema {esc(model.get('schema_version'))}</div>
  <h1>{esc(s.get('name'))}</h1>
  <p class="purpose">{esc(s.get('purpose'))}</p>
  <div class="summary-grid">
    <div><span>Domain</span><strong>{esc(s.get('domain', '—'))}</strong></div>
    <div><span>Model stage</span><strong>{esc(s.get('stage', '—'))}</strong></div>
    <div><span>Elements</span><strong>{len(model.get('elements', []))}</strong></div>
    <div><span>Flows</span><strong>{len(model.get('flows', []))}</strong></div>
  </div>
  {('<div class="outcomes"><h3>Desired outcomes</h3><ul>' + outcomes + '</ul></div>') if outcomes else ''}
</section>"""


def render_stage_map(model: dict, stage: str) -> str:
    elems = [e for e in model.get("elements", []) if e.get("stage") == stage]
    flows = [f for f in model.get("flows", []) if f.get("stage") == stage]
    if not elems:
        return f'<section><div class="eyebrow">Stage view</div><h2>{STAGE_LABELS[stage]}</h2><p class="muted">No model elements for this stage.</p></section>'

    order = {"actor": 0, "external": 0, "system": 1, "service": 1, "capability": 2, "process": 2,
             "decision": 3, "device": 3, "state": 4, "resource": 4, "data_store": 4,
             "queue": 5, "control": 5, "metric": 6}
    elems = sorted(elems, key=lambda e: (order.get(e.get("kind"), 9), e.get("name", "")))
    cols = min(4, max(1, math.ceil(math.sqrt(len(elems)))))
    gap_x, gap_y, pad_x, pad_y = 220, 125, 70, 65
    rows = math.ceil(len(elems) / cols)
    width = max(720, pad_x * 2 + (cols - 1) * gap_x + 180)
    height = max(260, pad_y * 2 + (rows - 1) * gap_y + 80)

    positions = {}
    nodes = []
    for i, e in enumerate(elems):
        row, col = divmod(i, cols)
        x, y = pad_x + col * gap_x, pad_y + row * gap_y
        positions[e["id"]] = (x, y)
        nodes.append(
            f'<g class="node {esc(e.get("kind", ""))}"><rect x="{x}" y="{y}" width="170" height="64" rx="12"/>'
            f'<text x="{x+85}" y="{y+26}" text-anchor="middle">{esc(e.get("name"))}</text>'
            f'<text class="node-meta" x="{x+85}" y="{y+47}" text-anchor="middle">{esc(e.get("kind"))} · {esc(e.get("evidence"))}</text></g>'
        )

    arrows = []
    for f in flows:
        if f.get("from") not in positions or f.get("to") not in positions:
            continue
        x1, y1 = positions[f["from"]]
        x2, y2 = positions[f["to"]]
        x1 += 170
        y1 += 32
        y2 += 32
        midx, midy = (x1 + x2) / 2, (y1 + y2) / 2 - 7
        arrows.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#arrow)"/>'
            f'<text class="edge-label" x="{midx}" y="{midy}" text-anchor="middle">{esc(f.get("label") or f.get("type"))}</text>'
        )

    legend = " ".join(badge(x, "flow") for x in sorted({f.get("type") for f in flows if f.get("type")}))
    return f"""
<section>
  <div class="section-head"><div><div class="eyebrow">Stage view</div><h2>{STAGE_LABELS[stage]}</h2></div><div>{legend}</div></div>
  <div class="viz-scroll"><svg class="system-map" viewBox="0 0 {width} {height}" role="img" aria-label="{STAGE_LABELS[stage]} system map">
    <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z"/></marker></defs>
    {''.join(arrows)}{''.join(nodes)}
  </svg></div>
</section>"""


def render_transition(model: dict) -> str:
    items = model.get("transitions", [])
    if not items:
        return ""
    blocks = []
    for t in items:
        blocks.append(
            "<div class='transition'>"
            f"<div>{badge(STAGE_LABELS.get(t.get('from'), t.get('from', '')))}</div>"
            "<div class='transition-arrow'>→</div>"
            f"<div><strong>{esc(t.get('change'))}</strong><div class='muted'>Verify: {esc(t.get('verification', '—'))}</div>"
            f"<div class='muted'>Rollback: {esc(t.get('rollback', '—'))}</div></div>"
            "<div class='transition-arrow'>→</div>"
            f"<div>{badge(STAGE_LABELS.get(t.get('to'), t.get('to', '')))}</div></div>"
        )
    return f"<section><div class='eyebrow'>Evolution path</div><h2>Current → transition → target</h2>{''.join(blocks)}</section>"


def render_capacity(model: dict) -> str:
    items = model.get("capacity", [])
    if not items:
        return ""
    cards = []
    for c in items:
        arrival, process = c.get("arrival_rate"), c.get("processing_rate")
        status = "Unknown"
        if isinstance(arrival, (int, float)) and isinstance(process, (int, float)):
            status = "Overloaded" if arrival > process else "Within capacity"
        cards.append(
            "<div class='card'>"
            f"<div class='eyebrow'>{esc(c.get('stage', ''))}</div><h3>{esc(c.get('name'))}</h3>"
            f"<div class='metric-row'><span>Arrival</span><strong>{esc(arrival if arrival is not None else '—')} {esc(c.get('unit', ''))}</strong></div>"
            f"<div class='metric-row'><span>Processing</span><strong>{esc(process if process is not None else '—')} {esc(c.get('unit', ''))}</strong></div>"
            f"<div class='metric-row'><span>Status</span><strong>{esc(status)}</strong></div>"
            f"<p class='muted'>{esc(c.get('notes', ''))}</p></div>"
        )
    return f"<section><div class='eyebrow'>Flow pressure</div><h2>Capacity & queues</h2><div class='cards'>{''.join(cards)}</div></section>"


def render_risks(model: dict) -> str:
    risks = model.get("risks", [])
    if not risks:
        return ""
    rows = "".join(
        f"<tr><td>{badge(r.get('severity', ''))}</td><td><strong>{esc(r.get('name'))}</strong><div class='muted'>{esc(r.get('cause'))}</div></td>"
        f"<td>{esc(r.get('control', '—'))}</td><td>{esc(r.get('recovery', '—'))}</td></tr>"
        for r in risks
    )
    return f"<section><div class='eyebrow'>Failure overlay</div><h2>Risks, controls & recovery</h2><div class='table-wrap'><table><thead><tr><th>Severity</th><th>Risk / cause</th><th>Control</th><th>Recovery</th></tr></thead><tbody>{rows}</tbody></table></div></section>"


def render_fitness(model: dict) -> str:
    checks = model.get("fitness_checks", [])
    if not checks:
        return ""
    rows = "".join(
        f"<tr><td>{esc(c.get('requirement'))}</td><td>{esc(c.get('mechanism'))}</td><td>{esc(c.get('verification'))}</td>"
        f"<td>{esc(c.get('pass_condition'))}</td><td>{esc(c.get('validation', '—'))}</td></tr>"
        for c in checks
    )
    return f"<section><div class='eyebrow'>Proof</div><h2>Verification & validation</h2><div class='table-wrap'><table><thead><tr><th>Requirement</th><th>Mechanism</th><th>Verification</th><th>Pass condition</th><th>Validation</th></tr></thead><tbody>{rows}</tbody></table></div></section>"


def render_health(model: dict) -> str:
    signals = model.get("health_signals", [])
    recoveries = model.get("recovery_actions", [])
    adapt = model.get("adaptation", {})
    if not signals and not recoveries and not adapt:
        return ""
    signal_rows = "".join(
        f"<tr><td><strong>{esc(s.get('name'))}</strong></td><td>{esc(s.get('desired_state'))}</td><td>{esc(s.get('threshold', '—'))}</td><td>{esc(s.get('owner', '—'))}</td></tr>"
        for s in signals
    )
    recovery_rows = "".join(
        f"<tr><td>{badge(r.get('level', ''))}</td><td>{esc(r.get('trigger'))}</td><td>{esc(r.get('action'))}</td><td>{esc(r.get('authority'))}</td><td>{esc(r.get('verification', '—'))}</td></tr>"
        for r in recoveries
    )
    allowed = "".join(f"<li>{esc(x)}</li>" for x in adapt.get("allowed", [])) or "<li>None defined</li>"
    governed = "".join(f"<li>{esc(x)}</li>" for x in adapt.get("requires_governed_redesign", [])) or "<li>None defined</li>"
    return f"""
<section><div class="eyebrow">Operating nervous system</div><h2>Health & adaptive loop</h2>
<div class="loop"><span>Desired state</span><b>→</b><span>Sense</span><b>→</b><span>Detect</span><b>→</b><span>Diagnose</span><b>→</b><span>Authorize</span><b>→</b><span>Respond</span><b>→</b><span>Recover</span><b>→</b><span>Verify</span><b>→</b><span>Learn</span><b>→</b><span>Adapt</span></div>
{('<div class="table-wrap"><table><thead><tr><th>Signal</th><th>Desired</th><th>Trigger</th><th>Owner</th></tr></thead><tbody>' + signal_rows + '</tbody></table></div>') if signals else ''}
{('<div class="table-wrap"><table><thead><tr><th>Level</th><th>Trigger</th><th>Action</th><th>Authority</th><th>Verify</th></tr></thead><tbody>' + recovery_rows + '</tbody></table></div>') if recoveries else ''}
<div class="adapt-grid"><div><h3>Allowed inside envelope {badge(adapt.get('level', '—'))}</h3><ul>{allowed}</ul></div><div><h3>Requires governed redesign</h3><ul>{governed}</ul></div></div>
</section>"""


def stylesheet() -> str:
    return """
:root{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#171717;background:#f7f7f5}*{box-sizing:border-box}body{margin:0}.page{max-width:1180px;margin:0 auto;padding:36px 22px 80px}.summary,section{background:white;border:1px solid #deded9;border-radius:18px;padding:24px;margin:0 0 18px}.eyebrow{text-transform:uppercase;letter-spacing:.09em;font-size:11px;font-weight:700;color:#6b6b65}.summary h1{font-size:38px;margin:6px 0 8px}.purpose{font-size:18px;color:#444;max-width:820px}.summary-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:20px}.summary-grid div,.card{border:1px solid #e6e6e1;border-radius:13px;padding:14px;background:#fbfbf9}.summary-grid span,.metric-row span{display:block;font-size:12px;color:#777}.summary-grid strong{display:block;margin-top:4px}.outcomes{margin-top:18px}.section-head{display:flex;justify-content:space-between;gap:16px;align-items:end}h2{font-size:25px;margin:3px 0 16px}h3{margin:4px 0 10px;font-size:16px}.badge{display:inline-block;border:1px solid #d7d7d1;border-radius:999px;padding:3px 8px;font-size:11px;background:#f4f4f1}.badge.flow{margin-left:4px}.viz-scroll{overflow-x:auto;border:1px solid #ecece8;border-radius:14px;background:#fcfcfa}.system-map{display:block;width:100%;min-width:720px;height:auto}.system-map line{stroke:#8b8b84;stroke-width:1.6}.system-map marker path{fill:#8b8b84}.node rect{fill:#fff;stroke:#a8a8a1;stroke-width:1.5}.node.control rect,.node.queue rect{stroke-dasharray:5 3}.node text{font-size:12px;font-weight:650;fill:#202020}.node .node-meta{font-size:9px;font-weight:500;fill:#73736d}.edge-label{font-size:9px;fill:#5f5f59}.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:13px}th{text-align:left;color:#6b6b65;font-size:11px;text-transform:uppercase;letter-spacing:.04em}th,td{padding:12px 10px;border-bottom:1px solid #ededE8;vertical-align:top}.muted{color:#74746e;font-size:12px;margin-top:4px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}.metric-row{display:flex;justify-content:space-between;gap:10px;padding:8px 0;border-bottom:1px solid #eeeeea}.metric-row span{display:inline}.loop{display:flex;flex-wrap:wrap;align-items:center;gap:7px;margin:0 0 16px}.loop span{border:1px solid #dcdcd7;border-radius:10px;padding:8px 10px;background:#fafaf7;font-size:12px}.adapt-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px}.adapt-grid>div{border:1px solid #e6e6e1;border-radius:13px;padding:14px}.transition{display:grid;grid-template-columns:auto 35px 1fr 35px auto;align-items:center;gap:8px;border-top:1px solid #ecece8;padding:16px 0}.transition-arrow{text-align:center;font-size:20px;color:#777}@media(max-width:700px){.summary-grid{grid-template-columns:1fr 1fr}.adapt-grid{grid-template-columns:1fr}.transition{grid-template-columns:1fr}.transition-arrow{transform:rotate(90deg)}.summary h1{font-size:30px}}
"""


def render_html(model: dict) -> str:
    sections = [render_summary(model)]
    sections.extend(render_stage_map(model, stage) for stage in STAGES)
    sections.extend([render_transition(model), render_capacity(model), render_risks(model), render_fitness(model), render_health(model)])
    title = esc(model["system"].get("name"))
    return f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title} — System Views</title><style>{stylesheet()}</style></head><body><main class='page'>{''.join(s for s in sections if s)}</main></body></html>"


def main() -> None:
    p = argparse.ArgumentParser(description="Render a canonical System Design Architect model")
    p.add_argument("model", help="Path to system.json")
    p.add_argument("--out", default=None, help="Output HTML path")
    args = p.parse_args()
    src = Path(args.model)
    model = load_model(src)
    out = Path(args.out) if args.out else src.with_name(src.stem + "-views.html")
    out.write_text(render_html(model), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()

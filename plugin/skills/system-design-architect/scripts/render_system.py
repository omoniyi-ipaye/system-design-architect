#!/usr/bin/env python3
"""Dependency-free HTML renderer for the canonical System Design Architect model."""
from pathlib import Path
import argparse, html, json, math

STAGES = ("as_is", "transition", "target")
LABEL = {"as_is": "AS-IS", "transition": "TRANSITION", "target": "TARGET"}


def e(v): return html.escape(str(v if v is not None else ""))
def badge(v): return f'<span class="badge">{e(v)}</span>'

def load(path):
    m=json.loads(Path(path).read_text(encoding="utf-8"))
    for k in ("schema_version","system","elements","flows"):
        if k not in m: raise SystemExit(f"missing {k}")
    return m

def visible(item, stage): return item.get("stage") in (stage, "shared")

def stage_map(m, stage):
    elems=[x for x in m.get("elements",[]) if visible(x,stage)]
    flows=[x for x in m.get("flows",[]) if visible(x,stage)]
    if not elems: return ""
    kinds={"actor":0,"external":0,"system":1,"service":1,"capability":2,"process":2,"decision":3,"device":3,"state":4,"resource":4,"data_store":4,"queue":5,"control":5,"metric":6}
    elems=sorted(elems,key=lambda x:(kinds.get(x.get("kind"),9),x.get("name","")))
    cols=min(4,max(1,math.ceil(math.sqrt(len(elems)))))
    pos={}; nodes=[]; gx,gy=220,120
    for i,x in enumerate(elems):
        r,c=divmod(i,cols); px,py=60+c*gx,55+r*gy; pos[x["id"]]=(px,py)
        shared=" · shared" if x.get("stage")=="shared" else ""
        nodes.append(f'<g><rect x="{px}" y="{py}" width="170" height="62" rx="12"/><text x="{px+85}" y="{py+25}" text-anchor="middle">{e(x.get("name"))}</text><text class="meta" x="{px+85}" y="{py+45}" text-anchor="middle">{e(x.get("kind"))} · {e(x.get("evidence"))}{shared}</text></g>')
    lines=[]
    for f in flows:
        if f.get("from") not in pos or f.get("to") not in pos: continue
        x1,y1=pos[f["from"]]; x2,y2=pos[f["to"]]; x1+=170; y1+=31; y2+=31
        lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#a)"/><text class="edge" x="{(x1+x2)/2}" y="{(y1+y2)/2-6}" text-anchor="middle">{e(f.get("label") or f.get("type"))}</text>')
    rows=math.ceil(len(elems)/cols); w=max(720,140+(cols-1)*gx+180); h=max(240,120+(rows-1)*gy+70)
    legend=" ".join(badge(x) for x in sorted({f.get("type") for f in flows if f.get("type")}))
    return f'<section><div class="head"><div><small>Stage view</small><h2>{LABEL[stage]}</h2></div><div>{legend}</div></div><div class="scroll"><svg viewBox="0 0 {w} {h}"><defs><marker id="a" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z"/></marker></defs>{"".join(lines)}{"".join(nodes)}</svg></div></section>'

def table(title, headers, rows, cls=""):
    if not rows: return ""
    hs="".join(f"<th>{e(h)}</th>" for h in headers)
    rs="".join("<tr>"+"".join(f"<td>{v}</td>" for v in r)+"</tr>" for r in rows)
    return f'<section class="{cls}"><h2>{e(title)}</h2><div class="scroll"><table><thead><tr>{hs}</tr></thead><tbody>{rs}</tbody></table></div></section>'

def build_steps(m):
    steps=sorted(m.get("process_steps",[]), key=lambda x:(x.get("sequence",9999),x.get("id","")))
    rows=[]
    for x in steps:
        ex="<br>".join(e(v) for v in x.get("exceptions",[])) or "—"
        rows.append([
            f"<strong>{e(x.get('id'))}</strong><br>{e(x.get('name'))}",
            e(x.get("trigger")),
            f"<strong>{e(x.get('owner'))}</strong><br><span class='muted'>{e(x.get('executor'))}</span>",
            e(x.get("action")),
            f"{e(x.get('state_before'))} → {e(x.get('state_after'))}",
            e(x.get("completion_evidence")),
            ex,
            e(x.get("exception_route","—")),
            badge(x.get("automation","—")),
            e(x.get("verification","—"))
        ])
    return table("Granular build specification",["Step","Trigger","Owner / executor","Exact action","State transition","Success evidence","Known exceptions","Exception route","Automation","Verification"],rows,"build-spec")

def report(m):
    s=m["system"]
    outcomes="".join(f'<li>{e(x.get("text"))} {badge(x.get("evidence",""))}</li>' for x in s.get("desired_outcomes",[]))
    out=[f'<section><small>Canonical system model · schema {e(m.get("schema_version"))}</small><h1>{e(s.get("name"))}</h1><p class="purpose">{e(s.get("purpose"))}</p><div class="stats"><div>Domain<strong>{e(s.get("domain","—"))}</strong></div><div>Stage<strong>{e(s.get("stage","—"))}</strong></div><div>Elements<strong>{len(m.get("elements",[]))}</strong></div><div>Build steps<strong>{len(m.get("process_steps",[]))}</strong></div></div>{("<h3>Desired outcomes</h3><ul>"+outcomes+"</ul>") if outcomes else ""}</section>']
    out += [stage_map(m,x) for x in STAGES]
    out.append(build_steps(m))
    trs=[]
    for x in m.get("transitions",[]): trs.append([badge(LABEL.get(x.get("from"),x.get("from"))),e(x.get("change")),e(x.get("verification","—")),e(x.get("rollback","—")),badge(LABEL.get(x.get("to"),x.get("to")))])
    out.append(table("Current → transition → target",["From","Change","Verify","Rollback","To"],trs))
    caps=[]
    for x in m.get("capacity",[]):
        a,p=x.get("arrival_rate"),x.get("processing_rate"); status="Unknown" if a is None or p is None else ("Overloaded" if a>p else "Within capacity")
        caps.append([e(x.get("name")),e(a if a is not None else "—"),e(p if p is not None else "—"),e(x.get("unit","")),e(status)])
    out.append(table("Capacity & queues",["Capacity","Arrival","Processing","Unit","Status"],caps))
    risks=[[badge(x.get("severity","")),e(x.get("name")),e(x.get("cause","—")),e(x.get("control","—")),e(x.get("recovery","—"))] for x in m.get("risks",[])]
    out.append(table("Risks, controls & recovery",["Severity","Risk","Cause","Control","Recovery"],risks))
    fit=[[e(x.get("requirement")),e(x.get("mechanism")),e(x.get("verification")),e(x.get("pass_condition")),e(x.get("validation","—"))] for x in m.get("fitness_checks",[])]
    out.append(table("Verification & validation",["Requirement","Mechanism","Verification","Pass","Validation"],fit))
    sig=[[e(x.get("name")),e(x.get("desired_state")),e(x.get("threshold","—")),e(x.get("owner","—"))] for x in m.get("health_signals",[])]
    rec=[[badge(x.get("level","")),e(x.get("trigger")),e(x.get("action")),e(x.get("authority")),e(x.get("verification","—"))] for x in m.get("recovery_actions",[])]
    out.append('<section><small>Operating nervous system</small><h2>Adaptive loop</h2><div class="loop">Desired state → Sense → Detect → Diagnose → Authorize → Respond → Recover → Verify → Learn → Adapt</div></section>')
    out.append(table("Health signals",["Signal","Desired","Trigger","Owner"],sig)); out.append(table("Recovery actions",["Level","Trigger","Action","Authority","Verify"],rec))
    return "".join(x for x in out if x)

CSS='''*{box-sizing:border-box}body{margin:0;background:#f6f6f3;color:#181818;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif}.page{max-width:1320px;margin:auto;padding:32px 20px 72px}section{background:white;border:1px solid #dfdfda;border-radius:18px;padding:22px;margin-bottom:16px}small{color:#777;text-transform:uppercase;letter-spacing:.08em;font-weight:700}h1{font-size:36px;margin:6px 0}h2{font-size:24px;margin:4px 0 14px}h3{font-size:15px}.purpose{font-size:18px;color:#454545}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.stats div{border:1px solid #e7e7e2;border-radius:12px;padding:12px;color:#777;font-size:12px}.stats strong{display:block;color:#222;margin-top:4px}.head{display:flex;justify-content:space-between;align-items:end}.badge{display:inline-block;border:1px solid #d8d8d3;border-radius:999px;padding:3px 8px;font-size:11px;background:#f7f7f4}.scroll{overflow:auto}svg{width:100%;min-width:720px;height:auto;background:#fcfcfa;border:1px solid #eee;border-radius:12px}svg rect{fill:#fff;stroke:#aaa;stroke-width:1.4}svg text{font-size:12px;font-weight:650;fill:#222}.meta,.edge{font-size:9px;font-weight:500;fill:#777}svg line{stroke:#888;stroke-width:1.5}marker path{fill:#888}table{width:100%;border-collapse:collapse;font-size:13px}th{text-align:left;color:#777;font-size:11px;text-transform:uppercase}th,td{padding:11px 9px;border-bottom:1px solid #eee;vertical-align:top}.muted{color:#777;font-size:11px}.build-spec table{min-width:1600px}.build-spec td:nth-child(1){min-width:160px}.build-spec td:nth-child(4){min-width:260px}.loop{border:1px solid #e4e4df;border-radius:12px;padding:14px;background:#fafaf7;line-height:1.8}@media(max-width:700px){.stats{grid-template-columns:1fr 1fr}h1{font-size:29px}}'''

def main():
    p=argparse.ArgumentParser(); p.add_argument("model"); p.add_argument("--out"); a=p.parse_args()
    m=load(a.model); out=Path(a.out) if a.out else Path(a.model).with_name(Path(a.model).stem+"-views.html")
    title=e(m["system"].get("name")); out.write_text(f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title} — System Views</title><style>{CSS}</style></head><body><main class='page'>{report(m)}</main></body></html>",encoding="utf-8"); print(out)

if __name__=="__main__": main()

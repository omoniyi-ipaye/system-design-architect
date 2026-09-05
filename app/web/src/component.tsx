import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";

type AnyRecord = Record<string, any>;
type View = "system" | "build" | "risk" | "health";
type Stage = "as_is" | "target";

type ToolResult = {
  structuredContent?: {
    model?: AnyRecord;
    validation?: AnyRecord;
    generatedAt?: string;
  };
};

declare global {
  interface Window {
    openai?: {
      toolOutput?: any;
      widgetState?: any;
      setWidgetState?: (state: any) => void;
      requestDisplayMode?: (args: { mode: "inline" | "fullscreen" | "pip" }) => Promise<any>;
    };
  }
}

function useToolPayload() {
  const initial = window.openai?.toolOutput ?? null;
  const [payload, setPayload] = useState<any>(initial);

  useEffect(() => {
    const onMessage = (event: MessageEvent) => {
      if (event.source !== window.parent) return;
      const message = event.data;
      if (!message || message.jsonrpc !== "2.0") return;
      if (message.method === "ui/notifications/tool-result") {
        setPayload(message.params?.structuredContent ?? null);
      }
    };
    window.addEventListener("message", onMessage, { passive: true });
    return () => window.removeEventListener("message", onMessage);
  }, []);

  return payload;
}

const safeArray = (value: any): AnyRecord[] => (Array.isArray(value) ? value.filter(Boolean) : []);
const text = (value: any, fallback = "—") =>
  typeof value === "string" || typeof value === "number" ? String(value) : fallback;

function visible(item: AnyRecord, stage: Stage) {
  return item.stage === stage || item.stage === "shared";
}

function SystemGraph({ model, stage }: { model: AnyRecord; stage: Stage }) {
  const elements = safeArray(model.elements).filter((item) => visible(item, stage));
  const flows = safeArray(model.flows).filter((item) => visible(item, stage));
  const elementIds = new Set(elements.map((e) => e.id));

  const ordered = [...elements].sort((a, b) => {
    const rank: Record<string, number> = {
      actor: 0,
      external: 0,
      capability: 1,
      service: 1,
      system: 1,
      process: 2,
      decision: 3,
      control: 4,
      queue: 4,
      state: 5,
      resource: 5,
      data_store: 5,
      metric: 6,
    };
    return (rank[a.kind] ?? 9) - (rank[b.kind] ?? 9) || text(a.name).localeCompare(text(b.name));
  });

  const cols = Math.min(4, Math.max(1, Math.ceil(Math.sqrt(Math.max(1, ordered.length)))));
  const gapX = 220;
  const gapY = 118;
  const positions = new Map<string, { x: number; y: number }>();
  ordered.forEach((item, index) => {
    const row = Math.floor(index / cols);
    const col = index % cols;
    positions.set(item.id, { x: 56 + col * gapX, y: 52 + row * gapY });
  });
  const rows = Math.ceil(ordered.length / cols);
  const width = Math.max(720, 140 + (cols - 1) * gapX + 180);
  const height = Math.max(250, 115 + (rows - 1) * gapY + 75);

  return (
    <div className="graph-wrap">
      <svg viewBox={`0 0 ${width} ${height}`} aria-label={`${stage} system graph`}>
        <defs>
          <marker id={`arrow-${stage}`} markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
            <path d="M0,0 L0,6 L9,3 z" />
          </marker>
        </defs>
        {flows.map((flow) => {
          if (!elementIds.has(flow.from) || !elementIds.has(flow.to)) return null;
          const from = positions.get(flow.from);
          const to = positions.get(flow.to);
          if (!from || !to) return null;
          const x1 = from.x + 168;
          const y1 = from.y + 31;
          const x2 = to.x;
          const y2 = to.y + 31;
          const mx = (x1 + x2) / 2;
          const my = (y1 + y2) / 2 - 7;
          return (
            <g key={flow.id}>
              <line x1={x1} y1={y1} x2={x2} y2={y2} markerEnd={`url(#arrow-${stage})`} />
              <text className="edge-label" x={mx} y={my} textAnchor="middle">
                {text(flow.label, text(flow.type, "flow"))}
              </text>
            </g>
          );
        })}
        {ordered.map((item) => {
          const pos = positions.get(item.id)!;
          const shared = item.stage === "shared" ? " · shared" : "";
          return (
            <g key={item.id} className={`graph-node kind-${item.kind}`}>
              <rect x={pos.x} y={pos.y} width="168" height="62" rx="13" />
              <text x={pos.x + 84} y={pos.y + 24} textAnchor="middle">
                {text(item.name)}
              </text>
              <text className="node-meta" x={pos.x + 84} y={pos.y + 44} textAnchor="middle">
                {text(item.kind, "element")} · {text(item.evidence, "unknown")}{shared}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

function BuildSteps({ model }: { model: AnyRecord }) {
  const steps = safeArray(model.process_steps);
  const persisted = window.openai?.widgetState?.selectedStepId;
  const [selectedId, setSelectedId] = useState<string | null>(persisted ?? steps[0]?.id ?? null);
  const selected = steps.find((step) => step.id === selectedId) ?? steps[0];

  const choose = (id: string) => {
    setSelectedId(id);
    window.openai?.setWidgetState?.({
      ...(window.openai?.widgetState ?? {}),
      selectedStepId: id,
    });
  };

  if (!steps.length) {
    return <Empty title="No granular build steps yet" body="The model is not BUILD READY. Add process_steps with implementation contracts." />;
  }

  const field = (label: string, value: any) => {
    if (Array.isArray(value)) value = value.join(" · ");
    if (value === undefined || value === null || value === "") return null;
    return (
      <div className="detail-row">
        <span>{label}</span>
        <strong>{String(value)}</strong>
      </div>
    );
  };

  return (
    <div className="build-grid">
      <div className="step-list" role="list">
        {steps.map((step) => (
          <button
            key={step.id}
            className={`step-row ${step.id === selected?.id ? "active" : ""}`}
            onClick={() => choose(step.id)}
            type="button"
          >
            <span className="step-id">{text(step.id)}</span>
            <span className="step-name">{text(step.name)}</span>
            <span className="step-meta">{text(step.owner)} · {text(step.automation_mode, text(step.executor))}</span>
          </button>
        ))}
      </div>
      {selected && (
        <div className="step-detail">
          <div className="detail-head">
            <div>
              <div className="eyebrow">Granular build contract</div>
              <h3>{text(selected.id)} · {text(selected.name)}</h3>
              <p>{text(selected.purpose)}</p>
            </div>
            <span className="pill">{text(selected.stage, "target").toUpperCase()}</span>
          </div>
          <div className="detail-columns">
            <div>
              {field("Trigger", selected.trigger)}
              {field("Preconditions", selected.preconditions)}
              {field("Inputs", selected.inputs)}
              {field("Authoritative sources", selected.sources)}
              {field("Owner", selected.owner)}
              {field("Executor", selected.executor)}
              {field("Exact action", selected.action)}
              {field("Decision rule", selected.decision_rule)}
            </div>
            <div>
              {field("State transition", `${text(selected.state_before)} → ${text(selected.state_after)}`)}
              {field("Outputs", selected.outputs)}
              {field("Downstream", selected.downstream)}
              {field("SLA", selected.sla)}
              {field("Controls", selected.controls)}
              {field("Success evidence", selected.success_evidence)}
              {field("Exceptions", selected.exceptions)}
              {field("Exception route", selected.exception_route)}
            </div>
            <div>
              {field("Recovery", selected.recovery)}
              {field("Escalation", selected.escalation)}
              {field("Automation", selected.automation_mode)}
              {field("Audit evidence", selected.audit_evidence)}
              {field("Health signal", selected.health_signal)}
              {field("Verification", selected.verification)}
              {field("Outcome validation", selected.validation)}
              {field("Implementation dependencies", selected.implementation_dependencies)}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function RiskView({ model }: { model: AnyRecord }) {
  const risks = safeArray(model.risks);
  if (!risks.length) return <Empty title="No risks modeled" body="Add failure modes, controls, and recovery to make resilience explicit." />;
  return (
    <div className="cards">
      {risks.map((risk) => (
        <article className="risk-card" key={risk.id}>
          <div className="risk-top"><span className={`severity severity-${risk.severity}`}>{text(risk.severity).toUpperCase()}</span><span>{text(risk.stage).toUpperCase()}</span></div>
          <h3>{text(risk.name)}</h3>
          <p><b>Cause:</b> {text(risk.cause)}</p>
          <p><b>Control:</b> {text(risk.control)}</p>
          <p><b>Recovery:</b> {text(risk.recovery)}</p>
          <p><b>Affects:</b> {Array.isArray(risk.affects) ? risk.affects.join(" · ") : "—"}</p>
        </article>
      ))}
    </div>
  );
}

function HealthView({ model }: { model: AnyRecord }) {
  const signals = safeArray(model.health_signals);
  const recovery = safeArray(model.recovery_actions);
  const adaptation = model.adaptation ?? {};
  return (
    <div className="health-stack">
      <div className="loop">
        {[
          "Desired state", "Sense", "Detect", "Diagnose", "Authorize", "Respond", "Recover", "Verify", "Learn", "Adapt",
        ].map((item, i, all) => (
          <React.Fragment key={item}>
            <span>{item}</span>{i < all.length - 1 && <b>→</b>}
          </React.Fragment>
        ))}
      </div>
      <div className="cards">
        {signals.map((signal) => (
          <article className="metric-card" key={signal.id}>
            <div className="eyebrow">Health signal</div>
            <h3>{text(signal.name)}</h3>
            <p><b>Desired:</b> {text(signal.desired_state)}</p>
            <p><b>Trigger:</b> {text(signal.threshold)}</p>
            <p><b>Owner:</b> {text(signal.owner)}</p>
          </article>
        ))}
      </div>
      <div className="adapt-grid">
        <div>
          <div className="eyebrow">Inside adaptation envelope · {text(adaptation.level, "L0")}</div>
          <ul>{safeArray(adaptation.allowed).map((item, i) => <li key={i}>{String(item)}</li>)}</ul>
        </div>
        <div>
          <div className="eyebrow">Requires governed redesign</div>
          <ul>{safeArray(adaptation.requires_governed_redesign).map((item, i) => <li key={i}>{String(item)}</li>)}</ul>
        </div>
      </div>
      {!!recovery.length && (
        <div className="cards">
          {recovery.map((action) => (
            <article className="metric-card" key={action.id}>
              <div className="eyebrow">Recovery · {text(action.level)}</div>
              <h3>{text(action.trigger)}</h3>
              <p>{text(action.action)}</p>
              <p><b>Authority:</b> {text(action.authority)}</p>
              <p><b>Verify:</b> {text(action.verification)}</p>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

function Empty({ title, body }: { title: string; body: string }) {
  return <div className="empty"><h3>{title}</h3><p>{body}</p></div>;
}

function App() {
  const payload = useToolPayload();
  const model = payload?.model ?? payload?.structuredContent?.model ?? null;
  const validation = payload?.validation ?? payload?.structuredContent?.validation ?? null;
  const restoredView = window.openai?.widgetState?.view as View | undefined;
  const [view, setView] = useState<View>(restoredView ?? "system");
  const restoredStage = window.openai?.widgetState?.stage as Stage | undefined;
  const [stage, setStage] = useState<Stage>(restoredStage ?? "as_is");

  const system = useMemo(() => (model?.system && typeof model.system === "object" ? model.system : {}), [model]);

  const setWorkspaceView = (next: View) => {
    setView(next);
    window.openai?.setWidgetState?.({ ...(window.openai?.widgetState ?? {}), view: next, stage });
  };
  const setWorkspaceStage = (next: Stage) => {
    setStage(next);
    window.openai?.setWidgetState?.({ ...(window.openai?.widgetState ?? {}), view, stage: next });
  };

  if (!model) {
    return <main className="shell"><Empty title="System workspace waiting for a model" body="Ask ChatGPT to build or load a system with System Design Architect." /></main>;
  }

  const stats = validation?.stats ?? {
    elements: safeArray(model.elements).length,
    flows: safeArray(model.flows).length,
    processSteps: safeArray(model.process_steps).length,
    risks: safeArray(model.risks).length,
    healthSignals: safeArray(model.health_signals).length,
  };

  return (
    <main className="shell">
      <header className="hero">
        <div>
          <div className="eyebrow">System Design Architect</div>
          <h1>{text(system.name, "Untitled system")}</h1>
          <p>{text(system.purpose, "No purpose defined yet")}</p>
        </div>
        <div className="hero-actions">
          <span className={`validation ${validation?.valid === false ? "bad" : "good"}`}>
            {validation?.valid === false ? `${validation.issues?.length ?? 0} issue(s)` : "Model valid"}
          </span>
          {window.openai?.requestDisplayMode && (
            <button type="button" className="ghost" onClick={() => window.openai?.requestDisplayMode?.({ mode: "fullscreen" })}>Fullscreen</button>
          )}
        </div>
      </header>

      <div className="stats">
        <Stat label="Domain" value={text(system.domain)} />
        <Stat label="Elements" value={stats.elements} />
        <Stat label="Flows" value={stats.flows} />
        <Stat label="Build steps" value={stats.processSteps} />
        <Stat label="Health signals" value={stats.healthSignals} />
      </div>

      <nav className="tabs" aria-label="System workspace views">
        {([
          ["system", "System"],
          ["build", "Build steps"],
          ["risk", "Risks"],
          ["health", "Health"],
        ] as [View, string][]).map(([id, label]) => (
          <button type="button" key={id} className={view === id ? "active" : ""} onClick={() => setWorkspaceView(id)}>{label}</button>
        ))}
      </nav>

      {view === "system" && (
        <section className="panel">
          <div className="panel-head">
            <div>
              <div className="eyebrow">Synchronized structural view</div>
              <h2>{stage === "as_is" ? "AS-IS" : "TARGET"}</h2>
            </div>
            <div className="stage-toggle">
              <button type="button" className={stage === "as_is" ? "active" : ""} onClick={() => setWorkspaceStage("as_is")}>AS-IS</button>
              <button type="button" className={stage === "target" ? "active" : ""} onClick={() => setWorkspaceStage("target")}>TARGET</button>
            </div>
          </div>
          <SystemGraph model={model} stage={stage} />
          {!!validation?.warnings?.length && (
            <div className="warning-box"><b>Model warnings</b><ul>{validation.warnings.map((w: string, i: number) => <li key={i}>{w}</li>)}</ul></div>
          )}
        </section>
      )}
      {view === "build" && <section className="panel"><BuildSteps model={model} /></section>}
      {view === "risk" && <section className="panel"><RiskView model={model} /></section>}
      {view === "health" && <section className="panel"><HealthView model={model} /></section>}

      <style>{styles}</style>
    </main>
  );
}

function Stat({ label, value }: { label: string; value: any }) {
  return <div className="stat"><span>{label}</span><strong>{String(value)}</strong></div>;
}

const styles = `
:root{color-scheme:light dark;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.shell{padding:16px;color:var(--sda-text,#181818);background:transparent}.hero{display:flex;gap:18px;justify-content:space-between;align-items:flex-start;margin-bottom:14px}.hero h1{margin:4px 0 6px;font-size:28px;line-height:1.1}.hero p{margin:0;color:#70706b;max-width:760px;font-size:14px}.eyebrow{text-transform:uppercase;letter-spacing:.08em;font-size:10px;font-weight:750;color:#777770}.hero-actions{display:flex;gap:8px;align-items:center}.validation,.pill{border:1px solid #d5d5cf;border-radius:999px;padding:5px 9px;font-size:11px;white-space:nowrap}.validation.good{background:#f3f7f2}.validation.bad{background:#fff2f0}.ghost{border:1px solid #d5d5cf;background:transparent;border-radius:9px;padding:7px 10px;color:inherit}.stats{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-bottom:12px}.stat{border:1px solid #dfdfd9;border-radius:11px;padding:10px;background:rgba(255,255,255,.38)}.stat span{display:block;font-size:10px;color:#777770}.stat strong{display:block;font-size:13px;margin-top:2px;overflow:hidden;text-overflow:ellipsis}.tabs,.stage-toggle{display:flex;gap:4px}.tabs{margin-bottom:10px;overflow-x:auto}.tabs button,.stage-toggle button{border:1px solid #dcdcd6;background:transparent;border-radius:9px;padding:8px 11px;color:inherit;white-space:nowrap}.tabs button.active,.stage-toggle button.active{background:#ecece7;font-weight:700}.panel{border:1px solid #deded8;border-radius:14px;padding:14px;background:rgba(255,255,255,.38)}.panel-head{display:flex;justify-content:space-between;align-items:flex-end;gap:10px;margin-bottom:10px}.panel-head h2{font-size:21px;margin:2px 0 0}.graph-wrap{overflow:auto;border:1px solid #e7e7e1;border-radius:12px;background:rgba(255,255,255,.45)}.graph-wrap svg{display:block;width:100%;min-width:720px;height:auto}.graph-wrap line{stroke:#8d8d86;stroke-width:1.4}.graph-wrap marker path{fill:#8d8d86}.graph-node rect{fill:rgba(255,255,255,.84);stroke:#a8a8a1;stroke-width:1.3}.kind-control rect,.kind-queue rect{stroke-dasharray:5 3}.graph-node text{font-size:11px;font-weight:700;fill:#222}.graph-node .node-meta,.edge-label{font-size:8.5px;font-weight:500;fill:#777}.warning-box{margin-top:10px;border:1px dashed #d7a463;border-radius:10px;padding:10px;font-size:12px}.warning-box ul{margin:5px 0 0 17px}.build-grid{display:grid;grid-template-columns:280px 1fr;gap:12px;min-height:400px}.step-list{display:flex;flex-direction:column;gap:5px;max-height:590px;overflow:auto}.step-row{text-align:left;border:1px solid #dfdfd9;border-radius:10px;padding:10px;background:transparent;color:inherit}.step-row.active{background:#ecece7;border-color:#bdbdb5}.step-id{display:block;font-size:10px;font-weight:800;color:#777}.step-name{display:block;font-size:13px;font-weight:750;margin-top:2px}.step-meta{display:block;font-size:10px;color:#777;margin-top:3px}.step-detail{border:1px solid #e0e0da;border-radius:12px;padding:13px;overflow:auto}.detail-head{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}.detail-head h3{margin:3px 0 4px;font-size:19px}.detail-head p{margin:0 0 10px;color:#74746e;font-size:12px}.detail-columns{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.detail-row{padding:8px;border-bottom:1px solid #ebebe5}.detail-row span{display:block;font-size:9px;text-transform:uppercase;letter-spacing:.05em;color:#81817b}.detail-row strong{display:block;font-size:11.5px;line-height:1.4;margin-top:3px;font-weight:650}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:9px}.risk-card,.metric-card{border:1px solid #dfdfd9;border-radius:11px;padding:12px}.risk-card h3,.metric-card h3{font-size:14px;margin:7px 0}.risk-card p,.metric-card p{font-size:11.5px;color:#666;margin:5px 0}.risk-top{display:flex;justify-content:space-between;font-size:9px;color:#777}.severity{font-weight:800}.severity-critical,.severity-high{color:#9a3529}.loop{display:flex;align-items:center;gap:5px;overflow:auto;margin-bottom:12px}.loop span{border:1px solid #ddddD7;border-radius:8px;padding:7px 8px;white-space:nowrap;font-size:10px}.loop b{color:#888}.adapt-grid{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin:11px 0}.adapt-grid>div{border:1px solid #dfdfd9;border-radius:11px;padding:11px}.adapt-grid ul{margin:7px 0 0 17px;font-size:11.5px}.empty{padding:44px 16px;text-align:center}.empty h3{margin:0 0 7px}.empty p{margin:0;color:#777;font-size:13px}@media(prefers-color-scheme:dark){.shell{--sda-text:#f0f0ed}.hero p,.eyebrow,.stat span,.step-id,.step-meta,.detail-head p,.detail-row span,.risk-top{color:#aaa}.panel,.stat,.graph-wrap{background:rgba(30,30,28,.6);border-color:#454540}.graph-node rect{fill:#252522;stroke:#777}.graph-node text{fill:#f2f2ef}.graph-node .node-meta,.edge-label{fill:#aaa}.tabs button,.stage-toggle button,.step-row,.step-detail,.risk-card,.metric-card,.adapt-grid>div,.detail-row{border-color:#454540}.tabs button.active,.stage-toggle button.active,.step-row.active{background:#343431}.validation.good{background:#203426}.validation.bad{background:#442522}}@media(max-width:850px){.stats{grid-template-columns:repeat(2,1fr)}.build-grid{grid-template-columns:1fr}.step-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));max-height:none}.detail-columns{grid-template-columns:1fr}.hero{flex-direction:column}.adapt-grid{grid-template-columns:1fr}}@media(max-width:520px){.step-list{grid-template-columns:1fr}.stats{grid-template-columns:1fr 1fr}.shell{padding:10px}}
`;

const root = document.getElementById("root");
if (root) createRoot(root).render(<App />);

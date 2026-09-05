import {
  registerAppResource,
  registerAppTool,
  RESOURCE_MIME_TYPE,
} from "@modelcontextprotocol/ext-apps/server";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import cors from "cors";
import express from "express";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { z } from "zod";

const SERVER_VERSION = "0.1.0";
const WIDGET_URI = "ui://system-design-architect/system-workspace-v1.html";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PLUGIN_ROOT = path.resolve(__dirname, "..", "..");
const WIDGET_BUNDLE = path.resolve(PLUGIN_ROOT, "web", "dist", "component.js");

type CanonicalModel = Record<string, unknown>;

type ValidationResult = {
  valid: boolean;
  issues: string[];
  warnings: string[];
  stats: {
    elements: number;
    flows: number;
    processSteps: number;
    risks: number;
    healthSignals: number;
  };
};

function asArray(value: unknown): unknown[] {
  return Array.isArray(value) ? value : [];
}

function asObject(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};
}

function validateCanonicalModel(model: CanonicalModel): ValidationResult {
  const issues: string[] = [];
  const warnings: string[] = [];
  const system = asObject(model.system);
  const elements = asArray(model.elements).map(asObject);
  const flows = asArray(model.flows).map(asObject);
  const steps = asArray(model.process_steps).map(asObject);
  const risks = asArray(model.risks);
  const signals = asArray(model.health_signals);

  if (!model.schema_version) issues.push("schema_version is required");
  if (!system.id) issues.push("system.id is required");
  if (!system.name) issues.push("system.name is required");
  if (!system.purpose) issues.push("system.purpose is required");
  if (!Array.isArray(model.elements)) issues.push("elements must be an array");
  if (!Array.isArray(model.flows)) issues.push("flows must be an array");

  const elementIds = new Set<string>();
  for (const element of elements) {
    const id = typeof element.id === "string" ? element.id : "";
    if (!id) {
      issues.push("every element requires a stable id");
      continue;
    }
    if (elementIds.has(id)) issues.push(`duplicate element id: ${id}`);
    elementIds.add(id);
    if (!element.name) issues.push(`element ${id} requires a name`);
    if (!element.kind) issues.push(`element ${id} requires a kind`);
    if (!element.stage) issues.push(`element ${id} requires a stage`);
  }

  const flowIds = new Set<string>();
  for (const flow of flows) {
    const id = typeof flow.id === "string" ? flow.id : "";
    if (!id) issues.push("every flow requires a stable id");
    if (id && flowIds.has(id)) issues.push(`duplicate flow id: ${id}`);
    if (id) flowIds.add(id);
    const from = typeof flow.from === "string" ? flow.from : "";
    const to = typeof flow.to === "string" ? flow.to : "";
    if (from && !elementIds.has(from)) issues.push(`flow ${id || "<unknown>"} references unknown from element: ${from}`);
    if (to && !elementIds.has(to)) issues.push(`flow ${id || "<unknown>"} references unknown to element: ${to}`);
  }

  const stepIds = new Set<string>();
  const requiredStepFields = [
    "id",
    "name",
    "purpose",
    "trigger",
    "owner",
    "executor",
    "action",
    "state_before",
    "state_after",
    "success_evidence",
    "verification",
  ];
  for (const step of steps) {
    const id = typeof step.id === "string" ? step.id : "<unknown>";
    if (id !== "<unknown>" && stepIds.has(id)) issues.push(`duplicate process step id: ${id}`);
    if (id !== "<unknown>") stepIds.add(id);
    for (const field of requiredStepFields) {
      if (!step[field]) issues.push(`process step ${id} missing ${field}`);
    }
    if (!step.exception_route && !step.exceptions) {
      warnings.push(`process step ${id} has no explicit exception route`);
    }
  }

  if (steps.length === 0) {
    warnings.push("No process_steps found. The system may be designed but is not yet BUILD READY.");
  }
  if (signals.length === 0) warnings.push("No health_signals found; operability is not yet observable.");

  return {
    valid: issues.length === 0,
    issues,
    warnings,
    stats: {
      elements: elements.length,
      flows: flows.length,
      processSteps: steps.length,
      risks: risks.length,
      healthSignals: signals.length,
    },
  };
}

const exampleModel: CanonicalModel = {
  schema_version: "1.1.0",
  system: {
    id: "example-onboarding",
    name: "Employee Onboarding System",
    purpose: "Make every new hire productive, compliant, equipped, and connected by Day 1.",
    stage: "mixed",
    domain: "people-operations",
    desired_outcomes: [
      { text: "New hire can perform core work on Day 1", evidence: "proposed" },
      { text: "Access, equipment, and payroll are ready before start", evidence: "proposed" },
    ],
  },
  elements: [
    { id: "new-hire", name: "New Hire", kind: "actor", stage: "shared", evidence: "observed" },
    { id: "manager", name: "Manager", kind: "actor", stage: "shared", evidence: "observed" },
    { id: "people-ops", name: "People Ops", kind: "capability", stage: "shared", evidence: "observed" },
    { id: "it", name: "IT Provisioning", kind: "capability", stage: "shared", evidence: "observed" },
    { id: "payroll", name: "Payroll", kind: "capability", stage: "shared", evidence: "observed" },
    { id: "readiness", name: "Readiness Gate", kind: "control", stage: "target", evidence: "proposed" },
    { id: "exception", name: "Exception Lane", kind: "queue", stage: "target", evidence: "proposed" },
  ],
  flows: [
    { id: "f1", from: "manager", to: "people-ops", type: "information", stage: "as_is", evidence: "observed", label: "Role/access/equipment details" },
    { id: "f2", from: "people-ops", to: "it", type: "work", stage: "as_is", evidence: "observed", label: "Provision access/equipment" },
    { id: "f3", from: "people-ops", to: "payroll", type: "information", stage: "as_is", evidence: "observed", label: "Payroll-ready record" },
    { id: "f4", from: "manager", to: "readiness", type: "information", stage: "target", evidence: "proposed", label: "Validated requirements" },
    { id: "f5", from: "readiness", to: "people-ops", type: "feedback", stage: "target", evidence: "proposed", label: "Readiness status" },
    { id: "f6", from: "readiness", to: "exception", type: "work", stage: "target", evidence: "proposed", label: "At-risk case" },
  ],
  process_steps: [
    {
      id: "ONB-010",
      name: "Create onboarding case",
      stage: "target",
      purpose: "Create the authoritative onboarding work item when the hire is confirmed.",
      trigger: "Signed hire / worker record becomes active",
      preconditions: ["Authoritative worker identifier exists"],
      inputs: ["Worker ID", "start date", "manager", "work location"],
      sources: ["HRIS / hiring system"],
      owner: "People Ops",
      executor: "Deterministic workflow",
      action: "Create one idempotent onboarding case keyed by worker ID.",
      decision_rule: "Do not create a duplicate open case for the same worker and start date.",
      state_before: "HIRED",
      state_after: "INPUT_PENDING",
      outputs: ["Onboarding case ID"],
      downstream: ["Manager requirements collection"],
      sla: "Within 15 minutes",
      controls: ["Idempotency", "source-of-truth worker ID"],
      success_evidence: "Case ID and creation event recorded",
      exceptions: ["Missing worker identifier", "duplicate case"],
      exception_route: "People Ops review queue",
      recovery: "Correct source data or reconcile duplicate and retry safely",
      escalation: "People Ops systems owner",
      automation_mode: "deterministic",
      audit_evidence: ["case_created event", "source record reference"],
      health_signal: "case creation failure rate",
      verification: "Integration test proves one case per worker/start-date key",
      validation: "All eligible hires enter onboarding without manual chasing",
      implementation_dependencies: ["HRIS/hiring trigger", "case store"],
    },
    {
      id: "ONB-030",
      name: "Validate manager requirements",
      stage: "target",
      purpose: "Prevent provisioning from starting with incomplete or invalid requirements.",
      trigger: "Manager submits role, equipment, and access package",
      preconditions: ["Case state is INPUT_SUBMITTED"],
      inputs: ["Manager requirements", "role/access catalogue", "worker record"],
      sources: ["Manager form", "policy catalogue", "HRIS"],
      owner: "People Ops",
      executor: "Deterministic validation rules",
      action: "Validate completeness, eligibility, and catalogue mappings.",
      decision_rule: "Provisioning cannot start if mandatory information or eligibility fails.",
      state_before: "INPUT_SUBMITTED",
      state_after: "READY_TO_PROVISION",
      outputs: ["Validated provisioning package"],
      downstream: ["IT", "Payroll"],
      sla: "Within 4 business hours",
      controls: ["Deterministic rule set", "rule version recorded"],
      success_evidence: "Validation result and rule version stored",
      exceptions: ["Policy conflict", "unsupported request", "missing authoritative data"],
      exception_route: "People Ops policy review",
      recovery: "Correct data/request and rerun validation",
      escalation: "Policy owner",
      automation_mode: "deterministic",
      audit_evidence: ["validation decision", "rule version", "source references"],
      health_signal: "validation rework rate",
      verification: "Tests cover every deterministic rule",
      validation: "Valid requests proceed without unnecessary delay",
      implementation_dependencies: ["policy catalogue", "role/access catalogue"],
    },
  ],
  risks: [
    { id: "r1", name: "Late manager input blocks provisioning", severity: "high", stage: "as_is", affects: ["manager", "it", "new-hire"], cause: "requirements arrive too late", control: "T-10 readiness gate", recovery: "route to exception lane and escalate" },
  ],
  health_signals: [
    { id: "s1", name: "Day-1 readiness rate", desired_state: ">=98%", threshold: "<95% over rolling 20 hires", owner: "People Ops" },
    { id: "s2", name: "Late manager submissions", desired_state: "<5%", threshold: ">10% in 30 days", owner: "People Ops" },
  ],
  adaptation: {
    level: "L2",
    allowed: ["reroute late case", "send escalation", "assign backup follow-up owner"],
    requires_governed_redesign: ["change eligibility policy", "change source-of-truth ownership"],
    max_blast_radius: "single onboarding case",
  },
};

function widgetHtml(): string {
  if (!fs.existsSync(WIDGET_BUNDLE)) {
    throw new Error(`Widget bundle missing at ${WIDGET_BUNDLE}. Run npm run build:widget first.`);
  }
  const component = fs.readFileSync(WIDGET_BUNDLE, "utf8");
  return `<div id="root"></div><script type="module">${component}</script>`;
}

function createServer(): McpServer {
  const server = new McpServer(
    { name: "system-design-architect", version: SERVER_VERSION },
    {
      instructions:
        "Use validate_system for canonical model quality checks. Use visualize_system whenever a non-trivial system should be shown visually. Keep AS-IS, TRANSITION, and TARGET distinct.",
    }
  );

  registerAppTool(
    server,
    "validate_system",
    {
      title: "Validate system model",
      description:
        "Use this when a canonical System Design Architect model needs structural and BUILD READY validation before it is presented as complete.",
      inputSchema: {
        model: z.record(z.string(), z.unknown()).describe("Canonical System Design Architect model"),
      },
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        openWorldHint: false,
      },
      _meta: {},
    },
    async ({ model }) => {
      const validation = validateCanonicalModel(model as CanonicalModel);
      return {
        structuredContent: validation,
        content: [
          {
            type: "text" as const,
            text: validation.valid
              ? `System model is structurally valid. ${validation.stats.processSteps} granular process steps are defined.`
              : `System model has ${validation.issues.length} blocking validation issue(s).`,
          },
        ],
      };
    }
  );

  registerAppTool(
    server,
    "visualize_system",
    {
      title: "Visualize system",
      description:
        "Use this when the user wants to see or inspect a system. Pass the canonical model to render the interactive System Design Architect workspace with AS-IS/TARGET views and granular build-step drill-down.",
      inputSchema: {
        model: z.record(z.string(), z.unknown()).describe("Canonical System Design Architect model"),
      },
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        openWorldHint: false,
      },
      _meta: {
        ui: { resourceUri: WIDGET_URI },
        "openai/toolInvocation/invoking": "Building system workspace…",
        "openai/toolInvocation/invoked": "System workspace ready.",
      },
    },
    async ({ model }) => {
      const canonical = model as CanonicalModel;
      const validation = validateCanonicalModel(canonical);
      const system = asObject(canonical.system);
      return {
        structuredContent: {
          model: canonical,
          validation,
          generatedAt: new Date().toISOString(),
        },
        content: [
          {
            type: "text" as const,
            text: `Showing ${String(system.name ?? "the system")} as an interactive system workspace. Validation: ${validation.valid ? "valid" : `${validation.issues.length} issue(s)`}.`,
          },
        ],
      };
    }
  );

  registerAppTool(
    server,
    "load_example_system",
    {
      title: "Load example system",
      description:
        "Use this when the user wants to try System Design Architect quickly with a worked employee-onboarding example.",
      inputSchema: {},
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        openWorldHint: false,
      },
      _meta: {
        ui: { resourceUri: WIDGET_URI },
      },
    },
    async () => ({
      structuredContent: {
        model: exampleModel,
        validation: validateCanonicalModel(exampleModel),
        generatedAt: new Date().toISOString(),
      },
      content: [
        {
          type: "text" as const,
          text: "Loaded the employee-onboarding reference system. Use the widget to inspect context, flows, risks, build steps, and health controls.",
        },
      ],
    })
  );

  registerAppResource(
    server,
    "System Design Architect Workspace",
    WIDGET_URI,
    {
      mimeType: RESOURCE_MIME_TYPE,
      description: "Interactive visual workspace for canonical System Design Architect models",
    },
    async () => ({
      contents: [
        {
          uri: WIDGET_URI,
          mimeType: RESOURCE_MIME_TYPE,
          text: widgetHtml(),
          _meta: {
            ui: {
              prefersBorder: true,
              csp: {
                connectDomains: [],
                resourceDomains: [],
              },
            },
            "openai/widgetDescription":
              "Interactive system-design workspace with synchronized system views and granular process-step inspection.",
          },
        },
      ],
    })
  );

  return server;
}

const port = Number.parseInt(process.env.PORT ?? "8000", 10);
const app = express();
app.use(cors());
app.use(express.json({ limit: "8mb" }));

app.get("/", (_req, res) => {
  res.json({
    name: "System Design Architect MCP",
    version: SERVER_VERSION,
    endpoint: "/mcp",
  });
});

app.all("/mcp", async (req, res) => {
  const server = createServer();
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
  });

  res.on("close", () => {
    transport.close().catch(() => {});
    server.close().catch(() => {});
  });

  try {
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  } catch (error) {
    console.error("MCP error:", error);
    if (!res.headersSent) {
      res.status(500).json({
        jsonrpc: "2.0",
        error: { code: -32603, message: "Internal server error" },
        id: null,
      });
    }
  }
});

app.listen(port, () => {
  console.log(`System Design Architect MCP listening on http://localhost:${port}/mcp`);
});

# System Design Architect

A vendor-neutral **Agent Skill** for designing, building, reviewing, operating, and evolving well-grounded systems in any domain.

A system can be software, an AI agent, a business process, an operating model, a customer service, a smart environment, a supply chain, a learning system, a physical operation, or another network of interacting elements organized around an outcome.

System Design Architect does not stop at a launch diagram or process map. It helps answer:

1. **Why does the system exist?**
2. **How should it work?**
3. **How will we know it actually works?**
4. **How will it stay healthy, recover, learn, and improve over time?**

## v2 core lifecycle

```text
Purpose / Outcome
      ↓
Boundary + Stakeholders
      ↓
Needs + Requirements
      ↓
Actors + Decisions + State / Resources
      ↓
Flows + Interfaces / Handoffs
      ↓
Capacity + Dependencies + Risks
      ↓
Design Options + Controls
      ↓
Resilience + Recovery
      ↓
Verify + Validate
      ↓
Operate + Measure
      ↓
Sense + Detect Drift
      ↓
Diagnose + Respond
      ↓
Recover + Verify
      ↓
Learn + Adapt
      └──────────────↺
```

The goal is a system that is **grounded at design time and governably adaptive at run time**.

## What “self-healing” means here

Self-healing does **not** mean unrestricted autonomous redesign.

The skill distinguishes four levels:

- **L0 Observable** — detect degradation and surface it.
- **L1 Assisted recovery** — recommend a corrective action; a human executes.
- **L2 Bounded auto-heal** — automatically execute pre-approved, reversible recovery actions.
- **L3 Governed adaptive optimization** — adjust routing, capacity, scheduling, configuration, or process parameters inside a defined adaptation envelope.

The system must not silently rewrite its own purpose, critical policies, authority model, safety boundaries, or sources of truth. Structural adaptation returns to the normal design → verification → validation loop.

See [`references/adaptive-systems.md`](references/adaptive-systems.md).

## Four lifecycle modes

### New System Design
Start from an idea, need, desired outcome, new process, product, service, or operating model.

### Existing System Review
Reconstruct the as-is system from evidence before recommending change.

### Change Design
Understand the relevant current system before adding or modifying a significant capability.

### Adaptive Operation / System Health
Use operational evidence to diagnose drift, incidents, recurring exceptions, bottlenecks, poor metrics, weak controls, or resilience gaps; recover first, then adapt safely.

## Domain lenses

### Software / digital
Services, APIs, events, data/state, identity/security, infrastructure, deployment, reliability, observability, scale.

### General systems
Actors, responsibilities, handoffs, resources/information/state, decision rights, policies, capacity, queues, controls, feedback, resilience, outcomes.

The skill does **not** force software concepts onto business or physical systems.

Examples:
- People Operations and employee onboarding
- organizational operating models
- procurement / finance approvals
- customer-service operations
- restaurant / hospitality flow
- logistics and supply chains
- manufacturing and physical operations
- smart homes / buildings
- learning and education systems
- public/service-delivery workflows
- software, APIs, AI and agent platforms

See [`references/domain-neutral-systems.md`](references/domain-neutral-systems.md).

## Teaching Mode

Teaching is a presentation mode, not the purpose of the skill. When useful, it progressively unfolds the system graph so the learner understands causality rather than memorizing a finished diagram.

Typical progression:

```text
Purpose
  ↓
Actors
  ↓
Boundary
  ↓
State / Resources / Inputs / Outputs
  ↓
Flows + Decisions + Interfaces
  ↓
Capacity + Dependencies
  ↓
Controls + Failure Modes
  ↓
Verification + Validation
  ↓
Health Signals + Feedback
  ↓
Recovery + Self-Healing Loop
  ↓
Target + Transition / Adaptation
```

See [`references/teaching-mode.md`](references/teaching-mode.md).

## Core principles

- Start with system-level outcomes, not technology or process ceremony.
- Distinguish **Observed / Assumed / Proposed / Unknown**.
- Establish the system boundary.
- Make ownership and decision rights explicit.
- Trace work, information, authority, state, and resource flows when relevant.
- Treat interfaces and handoffs as contracts.
- Understand demand, capacity, queues, bottlenecks, and rework.
- Treat dependencies as fallible.
- Design controls, recovery, and exception paths—not only the happy path.
- Distinguish **verification** (built correctly) from **validation** (right system / desired outcome achieved).
- Prefer whole-system metrics over local metrics that reward harmful optimization.
- Design sensing and feedback before claiming a system is adaptive.
- Bound self-healing autonomy with authority, reversibility, blast-radius, and escalation rules.
- Prefer evolutionary, reversible change.
- For AI: probabilistic models interpret/propose; deterministic controls enforce critical permissions and invariants.

## Example prompts

### Build a business system
```text
Use System Design Architect to design our employee onboarding system from first principles. I want a production-grade process with clear ownership, handoffs, states, exception recovery, capacity assumptions, outcome measures, and a bounded self-healing loop.
```

### Review an existing operation
```text
Review our current restaurant dinner-service system. Reconstruct the as-is flow and operational evidence first. Identify queues, handoff failures, capacity constraints, feedback loops, and recovery gaps. Then design the smallest target system and operating loop.
```

### Software
```text
Design a family budget application. Ground the architecture before implementation, define data ownership, failure/recovery behavior, fitness checks, observability, and the safe adaptation loop.
```

### AI system
```text
Design an AI employee assistant that can take selected actions. Define model vs deterministic responsibilities, tool permissions, approvals, grounding, evals, drift monitoring, recovery, and its autonomy envelope.
```

### System health
```text
This system has been running for six months and exceptions are increasing. Use System Health mode: compare actual behavior to intended outcomes, diagnose drift, propose safe recovery and adaptation, and identify what requires full redesign.
```

## Methodology

The skill synthesizes:
- systems thinking and systems engineering;
- process and service design;
- requirements, interfaces, verification and validation;
- capacity and flow analysis;
- reliability / resilience engineering;
- adaptive and bounded self-healing systems;
- Well-Architected quality lenses;
- C4 views for software where appropriate;
- Architecture / System Decision Records;
- security, privacy, safety and governance controls;
- AI/agent risk, grounding, autonomy and evals;
- architecture/system fitness checks;
- progressive teaching when requested.

See [`references/sources.md`](references/sources.md).

## Key references

- [`references/process.md`](references/process.md)
- [`references/domain-neutral-systems.md`](references/domain-neutral-systems.md)
- [`references/adaptive-systems.md`](references/adaptive-systems.md)
- [`references/teaching-mode.md`](references/teaching-mode.md)
- [`references/discovery.md`](references/discovery.md)
- [`references/data-systems.md`](references/data-systems.md)
- [`references/reliability.md`](references/reliability.md)
- [`references/security.md`](references/security.md)
- [`references/ai-systems.md`](references/ai-systems.md)
- [`references/architecture-fitness.md`](references/architecture-fitness.md)
- [`references/review-matrix.md`](references/review-matrix.md)

## Templates

- [`templates/DESIGN.md`](templates/DESIGN.md)
- [`templates/ARCHITECTURE_REVIEW.md`](templates/ARCHITECTURE_REVIEW.md)
- [`templates/ADAPTIVE_OPERATING_LOOP.md`](templates/ADAPTIVE_OPERATING_LOOP.md)
- [`templates/ADR.md`](templates/ADR.md)
- [`templates/THREAT_MODEL.md`](templates/THREAT_MODEL.md)
- [`templates/FITNESS_CHECKS.md`](templates/FITNESS_CHECKS.md)

Create a dossier:

```bash
python scripts/scaffold.py "My System" --out ./system-design
```

## Validation and evals

```bash
python scripts/validate_skill.py
```

CI also runs the Agent Skills reference validator and validates [`evals/evals.json`](evals/evals.json).

The eval suite checks whether the skill:
- resists unjustified technical/process complexity;
- adapts vocabulary to non-software domains;
- reconstructs existing systems before redesign;
- distinguishes verification from validation;
- identifies demand/capacity/queue issues;
- designs bounded recovery instead of uncontrolled “self-healing”;
- escalates novel/high-impact failures;
- recognizes recurring drift as evidence for governed redesign;
- protects high-impact AI actions;
- teaches progressively when requested.

## License

Apache License 2.0. See [`LICENSE`](LICENSE).

## Versioning

The project uses semantic versioning. **v2.0.0** makes adaptive, domain-neutral systems design the core methodology rather than an extension to software architecture. See [`CHANGELOG.md`](CHANGELOG.md).

## Contributing

Contributions are welcome, especially domain lenses, system-health cases, resilience patterns, process/operating-model examples, self-healing guardrails, verification/validation examples, and eval scenarios. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

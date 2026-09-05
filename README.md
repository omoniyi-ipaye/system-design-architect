# System Design Architect

A vendor-neutral **Agent Skill** for designing, reviewing, operating, explaining, and evolving grounded systems in any domain.

A system can be software, an AI agent, a business process, an operating model, a service, a smart environment, a supply chain, a learning system, a physical operation, or another network of interacting elements organized around an outcome.

## What v2.1 changes

System Design Architect is now explicitly **visual-first and end-to-end for daily use**.

The default behavior is no longer “write a complete architecture report.” It is:

```text
Question / Idea / Existing System
          ↓
Inspect Evidence
          ↓
Show First System View Early
          ↓
Trace End-to-End Flow
          ↓
Expose Bottlenecks / Risks / Unknowns
          ↓
Show Smallest Useful Target
          ↓
Show Transition
          ↓
Verify + Validate
          ↓
Attach Health / Recovery / Learning Loop
```

Visuals are treated as **semantic system models**, not decoration. Prose explains what the user should notice in the visual.

## Core promise

The skill helps answer four questions:

1. **Why does this system exist?** — purpose, outcomes, boundary, stakeholders, constraints.
2. **How should it work?** — actors, flows, decisions, state/resources, handoffs, capacity, controls, dependencies.
3. **How will we know it works?** — verification, validation, fitness checks, operational and outcome measures.
4. **How will it stay healthy and improve?** — sensing, drift detection, recovery, learning, bounded adaptation, governance.

## Daily-use defaults

### New system

```text
Purpose / Boundary
      ↓
Context View
      ↓
Core Flow
      ↓
Decisions / State / Capacity
      ↓
Options
      ↓
Target View
      ↓
Controls / Resilience
      ↓
Verify / Validate
      ↓
Transition
      ↓
Operating Loop
```

### Existing system

```text
Evidence
   ↓
AS-IS View
   ↓
Critical Flow
   ↓
Findings Overlay
   ↓
TARGET View
   ↓
Transition
   ↓
Verification / Validation
   ↓
Health / Adaptation Loop
```

### System health

```text
Desired Outcome
      ↓
Current Signals
      ↓
Health / Drift View
      ↓
Diagnosis
      ↓
Contain / Recover
      ↓
Verify Recovery
      ↓
Smallest Adaptation
      ↓
Monitor / Learn
```

## Visual view selection

The skill chooses the diagram based on the design question:

| Question | Preferred view |
|---|---|
| What is the system and its boundary? | System context / boundary map |
| How does work move end to end? | Process / value-stream / sequence |
| How is a service actually delivered? | Service blueprint |
| Who owns each step? | Swimlane / responsibility map |
| Who decides what? | Decision map |
| How does lifecycle/state change? | State machine |
| Where does work accumulate? | Queue / demand-capacity / bottleneck view |
| Why does behavior repeat? | Causal-loop diagram |
| What accumulates over time? | Stock-and-flow / resource map |
| How is software structured? | C4 views |
| How does execution behave? | Sequence / dynamic view |
| How does failure recover? | Failure / recovery view |
| How do we move to the future? | CURRENT → TRANSITION → TARGET |
| How does the system stay healthy? | Adaptive operating loop |

See [`references/visual-first.md`](references/visual-first.md) and [`references/diagramming.md`](references/diagramming.md).

## End-to-end discipline

Even when the user asks about one component, the skill checks the material consequences across the system:

- purpose/outcome;
- stakeholders and boundary;
- ownership and decision rights;
- state/resources/source of truth;
- work/information/authority/state/resource flows;
- handoffs/interfaces;
- dependencies;
- demand/capacity/queues/bottlenecks;
- controls/security/safety/privacy/governance;
- exception/failure/recovery paths;
- verification and validation;
- metrics/feedback;
- drift detection and self-healing envelope;
- transition and operating ownership.

It does **not** add sections mechanically for every item. It ensures material end-to-end effects are not missed.

See [`references/daily-use.md`](references/daily-use.md).

## Four lifecycle modes

- **Mode A — New System**: start from an idea, need, outcome, process, product, service, or operating model.
- **Mode B — Existing System**: reconstruct AS-IS from evidence before recommending TARGET.
- **Mode C — Change Design**: understand the affected current slice before adding or changing a capability.
- **Mode D — System Health / Adaptive Operation**: use real operating evidence to diagnose incidents, drift, recurring exceptions, capacity problems, weak controls, or resilience gaps.

## Domain-neutral by design

### Software / digital lens
Services, APIs/events, data/state, identity/security, infrastructure, deployment, reliability, observability, technical scale.

### General systems lens
Actors, responsibilities, handoffs, records/resources/state, decision rights, policies, capacity, queues, controls, feedback, resilience, outcomes.

The skill does not force APIs, microservices, or software terminology onto business or physical systems.

Examples include:
- People Operations and onboarding;
- organizational operating models;
- procurement and finance approvals;
- customer-service operations;
- hospitality/service flow;
- logistics and supply chains;
- manufacturing and physical operations;
- smart homes/buildings;
- learning systems;
- public-service workflows;
- software and AI platforms.

See [`references/domain-neutral-systems.md`](references/domain-neutral-systems.md).

## Verification vs validation

The skill explicitly separates:

- **Verification** — did we implement the specified system correctly?
- **Validation** — does the system actually produce the intended outcome in the real environment?

A process can complete every task and still fail its purpose.

Consequential requirements map to:

```text
Requirement → System Mechanism → Verification → Pass Condition
```

Outcome success is then validated separately.

## Bounded self-healing

Self-healing is deliberately constrained:

- **L0 Observable** — detect and surface;
- **L1 Assisted** — recommend recovery, human executes;
- **L2 Bounded auto-heal** — pre-authorized reversible recovery;
- **L3 Governed adaptive optimization** — controlled adjustment inside an explicit envelope.

The system must not silently rewrite its purpose, critical policy, authority model, safety boundaries, or sources of truth.

See [`references/adaptive-systems.md`](references/adaptive-systems.md).

## Teaching Mode

Teaching is a presentation mode, not the core purpose. When requested, the skill progressively unfolds the graph so the learner understands causality instead of seeing an unexplained final architecture.

For existing systems it uses:

```text
AS-IS → Findings → TARGET → Operating / Adaptive Loop
```

See [`references/teaching-mode.md`](references/teaching-mode.md).

## Daily artifact set

When persistent artifacts are useful, keep these synchronized:

- system view pack;
- evidence ledger;
- System Decision Records / ADRs;
- fitness checks;
- transition plan;
- adaptive operating loop.

Use [`templates/SYSTEM_VIEW_PACK.md`](templates/SYSTEM_VIEW_PACK.md) for the visual dossier.

Other templates:
- [`templates/DESIGN.md`](templates/DESIGN.md)
- [`templates/ARCHITECTURE_REVIEW.md`](templates/ARCHITECTURE_REVIEW.md)
- [`templates/SYSTEM_HEALTH.md`](templates/SYSTEM_HEALTH.md)
- [`templates/ADAPTIVE_OPERATING_LOOP.md`](templates/ADAPTIVE_OPERATING_LOOP.md)
- [`templates/FITNESS_CHECKS.md`](templates/FITNESS_CHECKS.md)
- [`templates/THREAT_MODEL.md`](templates/THREAT_MODEL.md)
- [`templates/ADR.md`](templates/ADR.md)

## Scaffold

```bash
python scripts/scaffold.py "My System" --mode design --out ./system-design
python scripts/scaffold.py "My System" --mode review --out ./system-design
python scripts/scaffold.py "My System" --mode health --out ./system-design
python scripts/scaffold.py "My System" --mode adaptive --out ./system-design
```

## Validation and evals

```bash
python scripts/validate_skill.py
```

CI also runs the Agent Skills reference validator and validates [`evals/evals.json`](evals/evals.json).

The eval suite protects key behavior: simplicity, domain-neutral reasoning, AS-IS-first reviews, verification-vs-validation, capacity analysis, bounded self-healing, safe AI actions, progressive teaching, and visual-first end-to-end daily use.

## Key references

- [`references/daily-use.md`](references/daily-use.md)
- [`references/visual-first.md`](references/visual-first.md)
- [`references/process.md`](references/process.md)
- [`references/domain-neutral-systems.md`](references/domain-neutral-systems.md)
- [`references/diagramming.md`](references/diagramming.md)
- [`references/discovery.md`](references/discovery.md)
- [`references/review-matrix.md`](references/review-matrix.md)
- [`references/architecture-fitness.md`](references/architecture-fitness.md)
- [`references/reliability.md`](references/reliability.md)
- [`references/adaptive-systems.md`](references/adaptive-systems.md)
- [`references/security.md`](references/security.md)
- [`references/data-systems.md`](references/data-systems.md)
- [`references/ai-systems.md`](references/ai-systems.md)
- [`references/teaching-mode.md`](references/teaching-mode.md)
- [`references/sources.md`](references/sources.md)

## License

Apache License 2.0. See [`LICENSE`](LICENSE).

## Versioning

The project uses semantic versioning. **v2.1.0** makes visual-first, end-to-end daily operation part of the core execution contract.

See [`CHANGELOG.md`](CHANGELOG.md).

## Contributing

Contributions are welcome, especially domain lenses, visual modeling patterns, system-health cases, process/operating-model examples, resilience patterns, self-healing guardrails, and behavioral evals.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).
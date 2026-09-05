# System Design Architect

A vendor-neutral **Agent Skill** for designing, reviewing, operating, and evolving well-grounded systems in any domain — visual-first, end-to-end, and model-driven.

A system can be software, an AI agent, a business process, an operating model, a customer service, a smart environment, a supply chain, a learning system, a physical operation, or another network of interacting elements organized around an outcome.

## What changed in v2.2

For non-trivial engagements, System Design Architect can now maintain a canonical machine-readable `system.json` and generate synchronized visual views from that one source of truth.

```text
Evidence / user input / operational data
                ↓
            system.json
                ↓
       ┌────────┼─────────┐
       ▼        ▼         ▼
     AS-IS    TARGET    TRANSITION
       │        │         │
       ├────────┼─────────┤
       ▼        ▼         ▼
   Capacity   Risks    Verification
       │        │         │
       └────────┼─────────┘
                ▼
        Health / adaptive loop
```

This prevents the context map, flow map, target design, risk analysis, fitness checks, and recovery loop from drifting apart.

### Canonical model

- [`model/system.schema.json`](model/system.schema.json)
- [`model/system.example.json`](model/system.example.json)
- [`model/README.md`](model/README.md)
- [`references/canonical-model.md`](references/canonical-model.md)

Validate a model:

```bash
python scripts/validate_model.py model/system.example.json
```

Render synchronized visual views:

```bash
python scripts/render_system.py model/system.example.json
```

The renderer creates a self-contained HTML visual report.

## Core behavior

The skill is designed to answer four questions:

1. **Why does the system exist?**
2. **How does it work end to end?**
3. **How will we know it actually works?**
4. **How will it remain healthy, recover, learn, and improve?**

It works **visual-first**: the agent should show useful system structure early, then use prose to explain the visual rather than substitute for it.

## Lifecycle modes

- **New System Design** — design from an idea or desired outcome.
- **Existing System Review** — reconstruct AS-IS from evidence before recommending change.
- **Change Design** — understand the affected current slice before modifying it.
- **System Health / Adaptive Operation** — diagnose drift, failure, bottlenecks, recurring exceptions, and recovery gaps using operational evidence.

## Domain lenses

### Software / digital
Services, APIs/events, data/state, identity/security, infrastructure, deployment, reliability, observability, technical scale.

### General systems
Actors, responsibilities, handoffs, resources/information/state, decision rights, policies, capacity, queues, controls, feedback, resilience, outcomes.

The skill does **not** force software concepts onto business, service, organizational, physical, or learning systems.

## Visual views

Depending on the system, the skill may use:

- system context / boundary map
- process or value-stream map
- service blueprint
- swimlane / responsibility map
- decision map
- state machine
- capacity / queue view
- causal-loop diagram
- stock-and-flow/resource map
- C4 views for software
- sequence/dynamic view
- failure/recovery map
- AS-IS → TRANSITION → TARGET
- adaptive operating loop

See [`references/visual-first.md`](references/visual-first.md) and [`references/diagramming.md`](references/diagramming.md).

## Daily-use workflow

```text
Classify
   ↓
Purpose + boundary
   ↓
Inspect evidence
   ↓
Show first system view
   ↓
Establish/update system.json
   ↓
Trace end to end
   ↓
Expose bottlenecks / risks
   ↓
Check state + capacity
   ↓
Compare material options
   ↓
Show TARGET
   ↓
Controls + resilience
   ↓
Verify + validate
   ↓
Show TRANSITION
   ↓
Attach health / adaptive loop
```

See [`references/daily-use.md`](references/daily-use.md).

## Self-healing

Self-healing is deliberately bounded:

- **L0 Observable** — detect and surface.
- **L1 Assisted** — recommend recovery; human executes.
- **L2 Bounded auto-heal** — pre-authorized reversible recovery.
- **L3 Governed adaptive optimization** — controlled adjustment inside an explicit adaptation envelope.

The system must not silently rewrite its purpose, critical policies, authority model, safety boundaries, or sources of truth.

See [`references/adaptive-systems.md`](references/adaptive-systems.md).

## Teaching Mode

Teaching is a presentation mode. It progressively unfolds the same system model so the learner understands why each role, process, control, handoff, or dependency exists.

See [`references/teaching-mode.md`](references/teaching-mode.md).

## Templates

- [`templates/SYSTEM_VIEW_PACK.md`](templates/SYSTEM_VIEW_PACK.md)
- [`templates/DESIGN.md`](templates/DESIGN.md)
- [`templates/ARCHITECTURE_REVIEW.md`](templates/ARCHITECTURE_REVIEW.md)
- [`templates/SYSTEM_HEALTH.md`](templates/SYSTEM_HEALTH.md)
- [`templates/ADAPTIVE_OPERATING_LOOP.md`](templates/ADAPTIVE_OPERATING_LOOP.md)
- [`templates/FITNESS_CHECKS.md`](templates/FITNESS_CHECKS.md)
- [`templates/THREAT_MODEL.md`](templates/THREAT_MODEL.md)
- [`templates/ADR.md`](templates/ADR.md)

## Validation

```bash
python scripts/validate_skill.py
python scripts/validate_model.py model/system.example.json
python scripts/render_system.py model/system.example.json
```

CI runs project validation, canonical-model validation, a renderer smoke test, the official Agent Skills reference validator, and JSON validation for the behavioral eval suites.

## Evals

- [`evals/evals.json`](evals/evals.json) — systems-design and safety behavior.
- [`evals/visual-daily-evals.json`](evals/visual-daily-evals.json) — visual-first and daily-use behavior.

## Current roadmap

The next major work is intentionally not more methodology prose:

1. executable model/agent behavioral eval harness;
2. live operational evidence adapters for System Health and bounded self-healing.

See the open GitHub issues.

## License

Apache License 2.0. See [`LICENSE`](LICENSE).

## Contributing

Contributions are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Versioning

The project follows semantic versioning. See [`CHANGELOG.md`](CHANGELOG.md).

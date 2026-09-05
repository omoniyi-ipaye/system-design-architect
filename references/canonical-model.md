# Canonical System Model

The canonical system model is the machine-readable source of truth for a System Design Architect engagement.

Use it for non-trivial systems whenever the working environment can create files or maintain structured state.

## Why it exists

Independent diagrams drift. A context map may say one thing while the process map, risk table, fitness checks, and adaptive loop say another.

The canonical model solves that by storing the system once and rendering multiple synchronized views from the same data.

```text
Evidence / user input / operational data
                ↓
            system.json
                ↓
       ┌────────┼────────┐
       ▼        ▼        ▼
   Context    Flow     State
      map      map      view
       │        │        │
       ├────────┼────────┤
       ▼        ▼        ▼
  Capacity    Risk     Health
      view     view      loop
       └────────┼────────┘
                ▼
      CURRENT → TARGET
```

## Files

- `model/system.schema.json` — canonical schema.
- `model/system.example.json` — worked domain-neutral example.
- `scripts/validate_model.py` — structural validation.
- `scripts/render_system.py` — dependency-free visual HTML renderer.

## Model invariants

The model must preserve:

- AS-IS, TRANSITION, and TARGET as explicit stages;
- Observed, Assumed, Proposed, and Unknown as evidence states;
- stable element IDs;
- typed flows: work, information, authority, state, money, material, resource, feedback, dependency;
- important handoff contracts;
- capacity and queue assumptions;
- risk → control → recovery relationships;
- requirement → mechanism → verification → validation relationships;
- health signal → trigger → response → recovery verification;
- adaptation level and maximum blast radius.

Never create one merged graph where current and proposed elements are visually indistinguishable.

## Daily workflow

### New system

1. Begin with purpose, outcomes, boundary, and actors.
2. Create the first `system.json` as soon as the first meaningful system view exists.
3. Add flows, decisions, state/resources, dependencies, and capacity as evidence emerges.
4. Add TARGET elements only after requirements and trade-offs justify them.
5. Add fitness checks and health/adaptation data before calling the design operationally complete.
6. Validate and render after significant updates.

### Existing system

1. Populate only observed/assumed AS-IS elements first.
2. Render AS-IS and trace end-to-end behavior.
3. Overlay risks and capacity issues.
4. Add proposed TARGET elements separately.
5. Add explicit transition records connecting current to target.
6. Do not delete inconvenient AS-IS evidence merely because a target design is preferred.

### System health

Update operational fields and health signals without rewriting design history. If recurring evidence implies structural change, add a governed transition or return to Change Design mode.

## Validation

Run:

```bash
python scripts/validate_model.py path/to/system.json
```

The validator catches broken references, invalid stages/evidence, flow inconsistencies, unsafe missing authority on recovery actions, and adaptation envelopes without a blast-radius definition.

## Rendering

Run:

```bash
python scripts/render_system.py path/to/system.json
```

This produces a self-contained HTML report with synchronized views for:

- AS-IS / TRANSITION / TARGET system maps;
- transition path;
- capacity and queue pressure;
- risks, controls, and recovery;
- verification and validation;
- health signals and adaptive operating loop.

The renderer is intentionally dependency-free so the model remains portable. A richer interactive renderer can be layered on top later without changing the model contract.

## Evidence discipline

Every element and flow should carry an evidence classification. For existing systems, add a source/path/reference when available.

A rendered diagram is not evidence by itself. It is a view of the model, and the model should point back to its evidence.

## Relationship to prose artifacts

Markdown design/review documents remain useful for rationale, decisions, explanations, and stakeholder communication. They should reference the canonical model rather than duplicate its structural truth manually.

The preferred hierarchy is:

```text
Evidence
  ↓
system.json       ← structural source of truth
  ↓
visual views      ← generated understanding
  ↓
SDRs / narrative ← rationale and decisions
```

Do not invert this hierarchy by manually editing generated views as if they were the system source of truth.

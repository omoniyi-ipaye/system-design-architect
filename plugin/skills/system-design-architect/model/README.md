# Canonical System Model

This directory contains the structural source-of-truth format for System Design Architect.

## Files

- `system.schema.json` — JSON Schema for the canonical model.
- `system.example.json` — worked employee-onboarding example with AS-IS, TARGET, risks, verification, health, recovery, and adaptation.

The model is designed to be domain-neutral. Elements may be people, teams, processes, services, systems, devices, resources, queues, controls, states, or data stores.

## Stage semantics

- `as_is` — exists in the current system only.
- `transition` — temporary migration/implementation structure.
- `target` — proposed desired-state structure.
- `shared` — stable element that persists across views, such as the same customer, team, supplier, or external system.

Flows remain stage-aware so current behavior and target behavior do not silently merge.

## Evidence semantics

- `observed` — supported by evidence.
- `assumed` — provisional assumption needed to continue.
- `unknown` — material fact not yet established.
- `proposed` — recommendation or future-state design.

## Validate

```bash
python scripts/validate_model.py model/system.example.json
```

## Render

```bash
python scripts/render_system.py model/system.example.json
```

The renderer creates a portable self-contained HTML report from the same model, including synchronized stage maps, transition path, capacity, risks/recovery, verification/validation, health signals, and adaptive operating loop.

See `references/canonical-model.md` for how an agent should create and maintain the model during daily work.

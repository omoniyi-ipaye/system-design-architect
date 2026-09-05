# Contributing

Thank you for improving System Design Architect.

## Principles for contributions

Changes should preserve these properties:
- domain-neutral rather than software-first;
- outcome- and requirement-driven;
- evidence-aware: Observed / Assumed / Proposed / Unknown;
- explicit about boundaries, ownership, decisions, state/resources, flows, interfaces, and capacity;
- simplicity-first;
- safety/security/privacy/governance conscious where relevant;
- verification **and** validation aware;
- resilient and recovery-aware;
- adaptive from evidence without uncontrolled self-modification;
- useful for AI and non-AI systems;
- evolutionary for existing systems;
- measurable enough to detect drift and know whether an intervention worked.

## Proposing methodology changes

For a new mandatory design step, explain:
1. what system failure or blind spot it prevents;
2. which domains/systems need it;
3. why it belongs in the core lifecycle rather than an optional reference;
4. how it affects Lightweight systems;
5. how the behavior can be evaluated;
6. whether it changes design-time, run-time, or adaptation-time responsibilities.

Avoid adding a framework merely because it is popular.

## Domain contributions

Domain-specific guidance is welcome when it maps to the universal systems lifecycle rather than replacing it.

A domain lens should explain:
- domain-specific actors/components;
- flows/resources/state;
- important quality attributes;
- decisions/controls;
- capacity/bottlenecks;
- evidence sources;
- failure/recovery patterns;
- validation measures;
- adaptation boundaries.

## Self-healing / adaptation contributions

Do not propose unrestricted autonomous redesign.

Any automated recovery/adaptation pattern should define:
- triggering evidence;
- diagnosis confidence;
- authority;
- reversibility;
- maximum blast radius;
- verification of recovery;
- escalation conditions;
- protected invariants that must not change automatically.

## Pull requests

- keep `SKILL.md` concise enough for agent loading;
- put deep guidance in `references/`;
- add/update evals for behavioral changes;
- add examples when they clarify a new domain or operating pattern;
- run `python scripts/validate_skill.py`;
- run the Agent Skills reference validator where available;
- cite primary/official methodology sources in `references/sources.md`;
- update `CHANGELOG.md` for user-visible behavioral changes.

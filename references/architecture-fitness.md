# Architecture Fitness Checks

Architecture should be testable engineering intent, not documentation alone.

For each consequential requirement map:
1. **Requirement** — measurable behavior or quality.
2. **Architecture mechanism** — design element intended to satisfy it.
3. **Verification** — test, eval, probe, review, or operational evidence.
4. **Pass condition** — observable success criterion.

Example:
| Requirement | Mechanism | Verification | Pass condition |
|---|---|---|---|
| Duplicate webhook delivery must not create duplicate adjustments | Idempotency key + unique transaction constraint | Integration test replays same webhook 10x | Exactly one adjustment exists |
| Agent cannot change salary without approval | Policy gateway + approval state machine | Adversarial tool eval | Zero unapproved writes |

## Good-enough rule
A design is ready when the important requirements and risks have mechanisms and credible verification paths. Completeness is not the goal; sufficient confidence to implement reversibly is.

## Fitness categories
- correctness/invariants
- authorization/isolation
- resilience/recovery
- latency/throughput
- compatibility/migration
- operability
- cost envelope
- AI task success/groundedness/tool safety

Prefer automated fitness checks for invariants likely to regress.

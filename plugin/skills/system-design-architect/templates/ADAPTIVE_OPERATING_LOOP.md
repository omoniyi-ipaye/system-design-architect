# Adaptive Operating Loop: <System>

## 1. Desired outcomes and acceptable operating range
### Intended outcome
### Guardrails / unacceptable states
### Current autonomy level
L0 Observable | L1 Assisted | L2 Bounded Auto-Heal | L3 Governed Adaptive Optimization

## 2. Signals
| Outcome / risk | Signal | Evidence source | Cadence / freshness | Owner |
|---|---|---|---|---|

## 3. Detection conditions
| Signal | Threshold / anomaly / condition | Why it matters | False-positive risk |
|---|---|---|---|

## 4. Diagnosis
| Condition | Likely causes | Evidence needed | Confidence rule | Alternative explanations |
|---|---|---|---|---|

## 5. Response catalogue
| Condition | Allowed response | Authority | Autonomy level | Reversible? | Max blast radius |
|---|---|---|---|---|---|

## 6. Escalation boundary
Escalate instead of auto-healing when:
- diagnosis confidence is below the approved threshold;
- impact is consequential or irreversible;
- the failure is novel / outside known scenarios;
- recovery would cross the adaptation envelope;
- repeated recovery indicates a structural cause;
- policy, authority, safety, or source-of-truth rules may need to change.

## 7. Recovery verification
| Response | Verification | Success condition | Time bound | Escalation if unsuccessful |
|---|---|---|---|---|

## 8. Learning loop
Capture:
- incidents and near misses;
- recurring exceptions;
- manual workarounds / overrides;
- queue/backlog and capacity trends;
- stakeholder feedback;
- fitness-check failures;
- successful and unsuccessful recovery actions;
- environmental / policy / dependency drift.

Classify resulting action:
- no change;
- operational adjustment;
- capacity/routing adjustment;
- control/rule adjustment;
- interface/handoff redesign;
- structural redesign;
- requirement/outcome reconsideration.

## 9. Adaptation envelope
### May happen automatically

### May be recommended but requires approval

### Requires full change-design + verification/validation

### Never silently auto-change
- system purpose / intended outcome;
- critical policy;
- authority / decision-right model;
- safety boundaries;
- source-of-truth rules;
- legal / regulatory interpretation;
- other explicitly protected invariants.

## 10. Change controls
- maximum frequency of automated adaptation:
- maximum magnitude:
- maximum blast radius:
- rollback / contingency:
- audit / learning record:
- stop / kill condition:

## 11. Review cadence

## 12. Re-enter system design when
- purpose/outcome changes;
- a critical assumption is invalidated;
- failures recur despite bounded recovery;
- demand/capacity changes materially;
- regulation/policy/environment changes;
- an adaptation changes boundaries, authority, or critical controls;
- fitness/validation evidence shows the current system no longer produces the intended outcome.

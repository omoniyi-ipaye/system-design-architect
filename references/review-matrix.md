# System Review Matrix

Rate only where evidence exists: **Strong / Adequate / Needs attention / Critical / Unknown**.

| Dimension | Review questions |
|---|---|
| Purpose fit | Does the system directly support the intended stakeholder/system outcome? |
| Boundary clarity | Is it clear what is inside the system, outside it, and crossing the boundary? |
| Simplicity | Is every major role/component/control/handoff justified by a requirement or risk? |
| Ownership | Are responsibility, accountability, decision rights, and sources of truth explicit? |
| Flow quality | Are work, information, authority, state, and resource flows coherent end to end? |
| Interfaces/handoffs | Are inputs, ownership transfer, acknowledgement, timing, and exceptions clear? |
| State/resource integrity | Are important states/resources, transitions, invariants, and reconciliation explicit? |
| Capacity/queues | Are demand, capacity, backlog/WIP, bottlenecks, and overload behavior understood? |
| Incentives / human behavior | Where people are central, do incentives and informal workarounds align with intended behavior? |
| Controls/governance | Are consequential decisions/actions controlled, authorized, auditable, and reversible where appropriate? |
| Safety/security/privacy | Are domain-relevant safety, security, confidentiality, abuse, and trust boundaries addressed? |
| Reliability/resilience | Are critical failures, partial success, recovery, reconciliation, contingency, and blast radius addressed? |
| Outcome validation | Can the system demonstrate that it creates the intended real-world outcome, not merely completes activities? |
| Verification/fitness | Do consequential requirements map to mechanisms and credible pass/fail checks? |
| Measurement quality | Do health/feedback signals measure the whole-system outcome without encouraging harmful local optimization? |
| Observability/sensing | Can degradation, drift, backlog, control failure, and outcome decline be detected in time? |
| Recovery | Are known failure states paired with owned, tested, reversible recovery actions? |
| Adaptive loop | Is there an explicit Sense → Detect → Diagnose → Respond → Recover → Verify → Learn loop where needed? |
| Adaptation governance | Is the self-healing/adaptation envelope explicit, with authority, blast-radius, rollback, and escalation limits? |
| Evolvability | Can important changes occur incrementally without destroying useful behavior? |
| Cost/resource efficiency | Are expensive or scarce resources justified and visible? |
| Sustainability | Are material long-term resource/environmental impacts addressed where relevant? |
| AI necessity | Is AI used only where probabilistic capability adds value? |
| AI grounding | Are authoritative sources, retrieval, provenance, conflicts, and drift handled? |
| AI action safety | Are tool permissions narrow and high-impact actions controlled/audited/approved? |
| AI evaluation | Are representative, adversarial, regression, and failure-recovery evals part of the lifecycle? |

For every `Needs attention` or `Critical` rating provide:
1. evidence;
2. impact on system outcome;
3. proposed treatment;
4. how improvement will be verified.

Do not average ratings into a single score unless a user explicitly needs one and the weighting is justified. A single critical control or safety gap can matter more than many strong dimensions.

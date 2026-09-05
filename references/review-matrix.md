# System Review Matrix

Rate only where evidence exists: **Strong / Adequate / Needs attention / Critical / Unknown**.

| Dimension | Review questions |
|---|---|
| Purpose fit | Does the system clearly serve a defined stakeholder/system outcome rather than merely complete activities? |
| Boundary clarity | Is it clear what is inside the system, outside it, and crossing the boundary? |
| End-to-end completeness | Are the material actors, flows, decisions, state/resources, handoffs, dependencies, controls, outcomes, and feedback visible across the full path? |
| Visual model quality | Can a stakeholder see the important structure/flow/causality without reading a long prose translation? Are AS-IS and TARGET clearly separated? |
| Simplicity | Is every major capability, handoff, control, tool, or component justified by a requirement or risk? |
| Ownership | Are accountability, responsibility, decision rights, and operating ownership explicit? |
| Interfaces / handoffs | Are required inputs, acknowledgement, timing, failure behavior, and escalation clear at important boundaries? |
| State / source of truth | Is important state, resource ownership, authoritative record, lifecycle, and transition logic clear? |
| Data consistency | Where digital/distributed state exists, are transaction boundaries, concurrency, consistency, schema evolution, and reconciliation explicit? |
| Capacity / queues | Are demand, processing capacity, backlog/WIP, bottlenecks, and overload behavior understood? |
| Human incentives | Where people are central, could incentives, workarounds, or local optimization produce behavior different from the designed process? |
| Controls / governance | Are consequential decisions, quality/safety controls, approval boundaries, escalation, accountability, and audit enforceable? |
| Security | Where relevant, are identity, authorization, secrets, trust boundaries, privileged actions, and abuse paths controlled? |
| Privacy | Is sensitive information minimized, retained intentionally, and prevented from unnecessary propagation? |
| Reliability / resilience | Are critical failures, partial success, dependency loss, bypass, and recovery treated explicitly? |
| Overload / blast radius | Are backpressure, quotas, load shedding, queue growth, failure containment, and degraded modes handled where relevant? |
| Performance / flow | Are the important speed, lead-time, latency, throughput, or responsiveness requirements explicit and evidence-based? |
| Verification | Can important requirements and controls be tested or inspected with credible pass conditions? |
| Validation | Is there evidence that the real system produces the intended outcome, not merely that the designed steps execute? |
| Measurement quality | Do metrics represent whole-system outcomes and leading risks rather than reward harmful local optimization? |
| Feedback dynamics | Are important reinforcing/balancing loops, delays, recurring workarounds, and unintended consequences understood? |
| Operability | Can the system's current condition be sensed, diagnosed, escalated, and acted upon by a clear owner? |
| Recovery | Are known failures recoverable and is successful recovery explicitly verified? |
| Drift detection | Can recurring exceptions, overrides, backlog growth, behavior changes, model/data changes, or dependency changes be detected before major failure? |
| Adaptive loop | Does operating evidence feed learning and governed improvement? |
| Adaptation governance | Are automatic responses bounded by authority, reversibility, blast radius, audit, and escalation? Are structural changes routed through redesign/revalidation? |
| Evolvability | Can important changes be introduced incrementally without unnecessary broad rewrites or process disruption? |
| Cost / resource efficiency | Are expensive components, staffing, inventory, tooling, infrastructure, or coordination costs justified and observable? |
| AI necessity | If AI is present, does probabilistic capability actually add value? |
| AI grounding | Are authoritative sources, retrieval/provenance, conflicts, and freshness handled? |
| AI action safety | Are tool permissions narrow and high-impact actions validated, authorized, audited, and approved appropriately? |
| AI evaluation | Are representative, adversarial, regression, failure-recovery, and drift evals part of the lifecycle? |
| System fitness | Do consequential requirements map to mechanisms, verification, real-world validation, and continuing health signals? |

Every `Needs attention` or `Critical` rating must include:
- evidence;
- affected system outcome/risk;
- proposed treatment;
- how improvement will be verified or validated.

Do not average ratings into a fake numerical architecture score. Prioritize by impact, reversibility, propagation risk, and evidence strength.
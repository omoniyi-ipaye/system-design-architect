# Adaptive and Self-Healing Systems

A well-designed system should not only work at launch. It should be able to detect degradation, contain failure, recover, learn from operation, and adapt safely when conditions change.

Use **self-healing** carefully. It does not mean unrestricted autonomous change. It means designing explicit sensing, diagnosis, response, recovery, learning, and governance loops proportionate to the system's risk.

## Core resilience loop

1. **Anticipate** — identify likely stressors, failure modes, drift, bottlenecks, and changing conditions before they cause harm.
2. **Sense** — define observable signals that reveal system health and outcome quality.
3. **Detect** — identify deviation from expected ranges, requirements, policies, or fitness criteria.
4. **Diagnose** — distinguish symptom from likely cause and determine confidence.
5. **Respond** — apply the safest bounded intervention available.
6. **Recover** — restore acceptable operation, reconcile partial work, and verify the system is healthy again.
7. **Learn** — capture incidents, exceptions, bottlenecks, workarounds, user feedback, and recurring patterns.
8. **Adapt** — improve rules, capacity, controls, interfaces, process structure, or architecture through governed change.

This loop is domain-neutral.

## Four levels of healing

### Level 0 — Observable
The system can tell humans when performance, quality, safety, or outcomes degrade.

### Level 1 — Assisted recovery
The system recommends a known corrective action, while a human decides and executes.

### Level 2 — Bounded automatic recovery
The system automatically performs pre-authorized, reversible recovery actions within strict limits.

Examples:
- restart an unhealthy worker;
- reroute work to an available queue/team;
- switch to a backup supplier/channel;
- resend a failed notification using idempotent semantics;
- schedule a missed onboarding task to an alternate owner.

### Level 3 — Adaptive optimization
The system may recommend or perform controlled changes to configuration, capacity, routing, scheduling, or process parameters using evidence and predefined guardrails.

Do not use Level 3 for consequential policy, safety, employment, financial, legal, or other high-impact decisions without explicit governance and appropriate human authority.

## The control loop

For each critical outcome define:

| Element | Question |
|---|---|
| Desired state | What does healthy/good look like? |
| Signal | What evidence tells us current state? |
| Threshold | What counts as material deviation? |
| Diagnosis | How do we determine likely cause? |
| Action | What intervention is permitted? |
| Authority | Who/what may authorize and execute it? |
| Reversibility | Can the intervention be undone? |
| Verification | How do we know recovery worked? |
| Learning | What should change if this recurs? |

## Drift detection

Systems drift even without explicit failures. Look for:
- demand or workload growth;
- recurring exceptions;
- queue/backlog growth;
- increased manual workarounds;
- quality decline;
- policy/environment changes;
- dependency behavior changes;
- model/data drift in AI systems;
- stakeholder incentives changing behavior;
- local optimizations harming end-to-end outcomes.

Treat drift as evidence for review, not automatic justification for redesign.

## Safe adaptation rules

1. Define the adaptation envelope before autonomy.
2. Prefer reversible actions before structural changes.
3. Separate detection from authorization.
4. Require evidence before changing a stable system.
5. Cap frequency, magnitude, and blast radius of automated changes.
6. Keep an audit trail of diagnosis, decision, action, and outcome.
7. Test adaptation rules with historical and adversarial scenarios.
8. Escalate when confidence is low, impact is high, or the failure is novel.
9. Never let the system silently rewrite its own goals, authority model, critical controls, or source-of-truth rules.
10. Periodically review whether the feedback metrics themselves still represent the desired outcome.

## Learning loop

A self-improving system needs more than incident response.

Capture:
- incidents and near misses;
- exceptions and escalations;
- repeated manual interventions;
- bottleneck and capacity trends;
- user/customer/employee feedback;
- fitness-check failures;
- control overrides;
- model/tool errors for AI systems;
- successful recoveries and unsuccessful interventions.

Then convert evidence into one of:
- no change;
- operational adjustment;
- rule/control update;
- capacity adjustment;
- interface/handoff redesign;
- architecture/process change;
- requirement or outcome reconsideration.

Every structural change re-enters the normal system-design workflow and should be verified/validated before broad rollout.

## Domain examples

### Employee onboarding
Signal: Day-1 readiness falls below target.
Detection: laptop-access failures cluster around late manager submissions.
Response: route late cases into an exception lane and escalate missing manager input.
Learning: redesign the pre-start handoff and measure manager completion lead time.

### Restaurant service
Signal: ticket-to-table time rises while kitchen utilization remains normal.
Diagnosis: completed dishes wait for runners.
Response: temporarily rebalance runner coverage.
Learning: revise staffing trigger or pickup-zone design if pattern recurs.

### Software service
Signal: user-visible error rate exceeds its fitness threshold.
Response: stop risky rollout, shift traffic, restart/reconcile bounded components.
Learning: post-incident change to dependency, test, or capacity policy.

## Relationship to fitness checks

Fitness checks define what acceptable system behavior means. Adaptive loops use those signals to determine when to investigate or intervene.

Do not optimize every metric. Prefer a small set of outcome and safety measures with explicit consequences.

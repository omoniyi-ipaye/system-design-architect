# Systems Design Process

This reference expands the universal lifecycle used by System Design Architect.

## Design philosophy

A useful system design is a set of decisions that makes intended outcomes possible **and keeps the system healthy as conditions change**. It is not a diagram inventory, software shopping list, SOP checklist, or static process map.

Use seven recurring questions:

1. What outcome should the system create?
2. Where is the system boundary and who/what participates?
3. How does work, information, authority, state, money/material, or other resources flow?
4. What qualities, constraints, controls, and risks matter?
5. What is the simplest structure that satisfies those needs?
6. How will we verify/validate that it works and sense when it stops working?
7. How will it recover, learn, and adapt safely?

## Evidence labels

Use:
- **Observed** — directly supported by evidence.
- **Assumed** — needed to proceed but not verified.
- **Proposed** — recommendation or target-state design.
- **Unknown** — material information not yet established.

Do not hide uncertainty inside confident architecture prose.

## Outcome hierarchy

Distinguish:
- **activity** — something the system does;
- **output** — immediate product/result;
- **outcome** — change experienced by stakeholder/system;
- **system health** — ability to continue producing the outcome within acceptable bounds.

Example: sending onboarding emails is an activity; completing setup tasks is an output; Day-1 readiness is an outcome.

## Quality-attribute lens

Evaluate only what matters to the domain:
- effectiveness / functional fitness
- safety
- fairness
- security/privacy/confidentiality
- reliability/resilience/recoverability
- speed/latency/lead time
- throughput/capacity
- accuracy/quality
- operability/observability
- maintainability/evolvability
- adaptability
- cost/resource efficiency
- sustainability
- usability/accessibility
- compliance/governance
- employee/customer experience
- learning effectiveness
- AI trustworthiness/evaluation where relevant

Make material qualities measurable where useful, but do not invent precise targets.

## Requirements quality

Good requirements describe needed behavior/outcome and constraints without prematurely prescribing implementation.

Bad: `Use Kafka.`
Better: `Durably absorb bursts, support independent consumers, and replay seven days.`

Bad: `Add another manager approval.`
Better: `Purchases above the defined risk threshold must receive independent budget authority before commitment.`

Bad: `Automate onboarding.`
Better: `All required Day-1 dependencies must be ready by the employee start date, with explicit ownership and exception recovery.`

## System-boundary rule

Before optimizing a step, define what belongs inside the system and what is an external dependency. A local optimization that improves one component but damages end-to-end outcome is a system failure.

## Flow model

Trace separately when useful:
- work/case flow;
- information flow;
- authority/decision flow;
- state flow;
- money/material/resource flow.

For every meaningful handoff define: sender, receiver, required information/resource, acknowledgement, timing expectation, exception path, and ownership after transfer.

## State and decision model

Explicitly identify important states and allowed transitions. Define who/what may cause each consequential transition, according to which rules and evidence.

For software this may become a state machine/transaction model. For operations it may be case status, inventory state, approval status, or service stage.

## Capacity and queue method

For each constrained stage estimate:
- arrival/demand rate;
- processing capacity;
- queue/backlog/work-in-progress;
- waiting/lead time;
- variability;
- failure/rework load.

If sustained demand exceeds capacity, treat it as a structural constraint rather than a motivation slogan.

## Option rule

Do not create fake alternatives. Useful options differ materially in structure, control, centralization, automation, capacity model, or failure behavior.

Compare:
- which requirements/outcomes each optimizes;
- what becomes harder;
- new failure modes;
- coordination/operational burden;
- resource/cost implications;
- reversibility;
- evidence that would favor another option.

## Decision reversibility

Classify major choices:
- **Easy** — local configuration, implementation detail, reversible routing.
- **Moderate** — platform choice, supplier model, workflow ownership, database/event contracts, team responsibility boundaries.
- **Hard** — system boundary, identity/authority model, data ownership, tenancy, major operating-model design, public contracts, safety policy.

Spend effort proportionally.

## Failure-mode method

For every critical flow inspect:
1. invalid/missing input;
2. wrong or unavailable authority;
3. dependency/handoff delay or failure;
4. incorrect state/resource change;
5. partial execution;
6. duplicated work/request;
7. out-of-order/late work;
8. overload/capacity exhaustion;
9. failure detection delay;
10. recovery/reconciliation;
11. failure of the recovery action itself;
12. blast radius.

## Verification vs validation

**Verification** asks whether the implemented system satisfies its specified requirements, controls, and mechanisms.

**Validation** asks whether the system actually produces the intended outcome in its real environment.

Example: verifying that every onboarding task completed does not validate that the employee was actually productive on Day 1.

Use both.

## Fitness-check method

For consequential requirements create:

`requirement/outcome → mechanism → evidence/verification → pass condition → owner`

Prefer automated or routinely observable checks where feasible.

## Adaptive operating model

A complete operational system should define, where material:

`Desired state → Sense → Detect → Diagnose → Decide/Authorize → Respond → Recover → Verify → Learn → Adapt`

Self-healing must be bounded. Separate:
- automatic operational recovery;
- governed structural adaptation.

Recurring failures and drift are evidence for redesign, not permission for uncontrolled self-modification.

## Learning method

Capture incidents, near misses, bottlenecks, queue growth, exceptions, manual workarounds, control overrides, user feedback, fitness failures, and successful/failed recoveries.

Classify resulting action as:
- no change;
- operational adjustment;
- capacity/routing adjustment;
- control/rule adjustment;
- interface/handoff redesign;
- architecture/process change;
- requirement/outcome reconsideration.

Structural changes return to the normal design and validation lifecycle.

## Readiness criteria

### READY
- purpose/boundary coherent;
- core needs known;
- ownership and material decisions explicit;
- critical flows and interfaces understood;
- important risks/failure modes treated;
- consequential decisions have rationale;
- verification/validation approach exists;
- implementation can start in a reversible slice.

### READY WITH ASSUMPTIONS
Same as READY, with non-critical unknowns explicitly tracked and validation planned.

### NOT READY
Use sparingly for blockers such as:
- unknown authority/source of truth for consequential actions;
- unresolved safety/security/legal constraint that changes fundamental design;
- unverified dependency that determines the architecture/operating model;
- inability to define acceptable consistency/recovery for critical state;
- no credible way to measure the intended outcome.

## Operability maturity

After build/change readiness, assess separately:
- **Observable** — health/outcomes can be sensed.
- **Recoverable** — known failures have owned and tested recovery.
- **Adaptive** — evidence can drive governed changes.
- **Self-healing within bounds** — selected reversible recovery is automated inside a defined envelope.

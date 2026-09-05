# Build Layer — From System Design to Implementable Process

A system map explains structure. A build layer makes the system implementable.

For every material process or capability, decompose the design into **buildable process steps**. The implementation team should be able to build, configure, automate, document, or operate the system from these specifications without reverse-engineering intent from a diagram.

## Three layers

1. **System layer** — purpose, boundary, actors, capabilities, flows, dependencies, risks, outcomes.
2. **Process layer** — ordered processes, decisions, states, handoffs, exception paths, controls.
3. **Build layer** — granular executable/operational specifications for each step.

Do not stop at Layer 1 for a request to "build a system".

## Buildable process-step contract

Every material step should define:

- **Step ID** — stable identifier, e.g. `ONB-030`.
- **Name** — concise action-oriented label.
- **Stage** — AS-IS / TRANSITION / TARGET / shared.
- **Purpose** — why this step exists.
- **Trigger** — event/condition that starts it.
- **Preconditions** — facts/states that must be true before execution.
- **Inputs** — data, documents, resources, materials, requests, or signals required.
- **Source of input** — authoritative origin of each important input.
- **Owner** — role/component accountable for completion.
- **Executor** — human, system, device, vendor, or automation that performs the work.
- **Action** — exact operation performed.
- **Decision/rule** — deterministic rule or judgment point applied.
- **State transition** — state before → state after.
- **Outputs** — artifacts, state, notifications, resources, or records created.
- **Recipients/downstream** — who/what consumes the output.
- **Timing/SLA** — deadline, duration, service expectation, or sequence constraint.
- **Control** — authorization, validation, quality, safety, privacy, or compliance check.
- **Happy-path completion evidence** — what proves the step succeeded.
- **Exception conditions** — known ways the step can fail or be blocked.
- **Exception route** — where each exception goes.
- **Recovery** — how operation returns to an acceptable state.
- **Escalation** — authority/role for unresolved cases.
- **Automation boundary** — manual / deterministic automation / AI-assisted / autonomous-within-bounds.
- **Audit evidence** — what should be recorded.
- **Metric/health signal** — what reveals step quality, delay, or drift.
- **Verification** — how to prove the step was implemented correctly.
- **Validation** — how to prove it contributes to the intended system outcome.

Not every trivial step needs every field. Every consequential step does.

## Process granularity rule

Decompose until each step has:

- one clear owner/executor;
- one primary state transition or outcome;
- explicit inputs and outputs;
- a testable completion condition;
- a meaningful failure/recovery path if failure matters.

If a box still contains several independently failing actions, it is too coarse.

Bad:

`Onboard employee`

Still too coarse:

`Prepare employee for Day 1`

Buildable:

`ONB-030 Validate manager input`
`ONB-040 Create identity account`
`ONB-050 Assign application access`
`ONB-060 Order/allocate device`
`ONB-070 Register payroll record`
`ONB-080 Run readiness gate`

## Process graph

A target process should be expressible as a graph of steps and decisions rather than only prose:

Trigger → step → decision → branch → step → state → outcome

Show normal flow and exception/recovery routes separately when density would make one graph unreadable.

## Build pack

For a serious system build, produce enough of the following to implement the system:

1. system context/boundary view;
2. end-to-end process graph;
3. process-step catalogue;
4. state model;
5. decision/rule catalogue;
6. handoff/interface contracts;
7. data/resource/source-of-truth map;
8. control and authorization matrix;
9. exception/recovery catalogue;
10. automation allocation (human vs deterministic vs AI);
11. verification/validation tests;
12. operational health signals and adaptive loop;
13. transition/implementation backlog.

The canonical model should hold the structured source of truth. Visuals and process documents should be generated from, or traceable back to, that model.

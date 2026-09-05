# Teaching Mode — Progressive System Graph

Teaching Mode turns system design into a guided explanation rather than a one-shot architecture report. It can be combined with New System Design, Existing System Review, or Change Design.

## Goal

Help the learner understand **why the system has its shape**, not merely memorize the final diagram.

The graph should unfold progressively. Each stage adds only the concepts needed for the next reasoning step while preserving the previously established graph.

## Default unfolding sequence

1. **Purpose / outcome** — what the system exists to achieve.
2. **Actors / stakeholders** — people, teams, organizations, machines, or external systems that influence or depend on it.
3. **Boundary / environment** — what is inside the system and what remains external.
4. **Inputs, resources, and outputs** — information, materials, money, energy, demand, decisions, or services moving through the system.
5. **Core flow** — the normal path from trigger to outcome.
6. **Rules and decision points** — constraints, policies, invariants, approvals, and branching logic.
7. **Dependencies and interfaces** — handoffs, APIs, contracts, suppliers, teams, channels, or physical connections.
8. **Failure modes and constraints** — where the system can break, overload, become unsafe, or create unintended effects.
9. **Feedback and measurement** — signals that reveal whether the system is working and loops that influence future behavior.
10. **Design options and trade-offs** — credible alternative structures and what each optimizes.
11. **Target system** — the recommended design, now shown as the complete graph.
12. **Transition / implementation** — how to move from the current state to the target state in safe, testable increments.

For very small systems, combine adjacent stages. For complex systems, split a stage into subgraphs.

## How to teach each stage

For every stage:

- show the graph accumulated so far;
- visually emphasize only the nodes/edges introduced or changed at this stage when the medium supports it;
- explain **what was added**;
- explain **why it matters**;
- give one concrete example;
- identify one common mistake or failure mode;
- connect the stage to the next question the design must answer.

Do not reveal a dense final architecture first and then retroactively explain it unless the user explicitly asks for an overview-first approach.

## Interaction styles

### Guided lesson
Use when the user wants to learn. Teach one stage at a time. When the environment allows interaction, pause at meaningful checkpoints for the learner to explain the system back, choose between options, or answer a short applied question before continuing.

### Continuous walkthrough
Use when the user wants the whole explanation without pauses. Still preserve progressive disclosure by clearly showing Stage 1 → Stage 2 → … and how the graph evolves.

### Review walkthrough
For an existing system, unfold the **as-is graph first** from evidence, then layer findings and finally unfold the **target graph**. Never mix observed current-state elements with proposed future-state elements without labeling them.

## Graph semantics

Use consistent visual semantics where possible:

- people/stakeholders
- processes/capabilities
- information/resources/state
- decisions/policies
- external dependencies
- feedback/measurement
- risks/constraints

Always label important relationships. Avoid decorative arrows.

For software systems, C4 and sequence/dynamic views remain useful.
For non-software systems, prefer a system map, flow map, causal/feedback map, responsibility map, or value-stream view as appropriate.

## Evidence and certainty

Teaching Mode does not weaken evidence discipline. Mark graph elements as:

- **Observed** — established by evidence;
- **Assumed** — provisional;
- **Proposed** — recommended future structure.

For existing systems, cite or name the evidence supporting important nodes and relationships when available.

## Teach causality, not just structure

A useful explanation answers:

- Why is this component/role/process here?
- What happens if it is removed?
- What requirement does it satisfy?
- What risk does it control?
- What new failure mode does it introduce?
- What signal tells us whether it works?

The learner should finish able to reconstruct the system from first principles rather than merely recognize the final diagram.

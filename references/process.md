# System Design Process

This reference expands the main skill workflow and provides review criteria.

## Design philosophy

A useful architecture is a set of decisions that make important system qualities possible. It is not a diagram inventory and not a technology shopping list.

Use five recurring questions:

1. What must the system do?
2. What qualities must it exhibit while doing it?
3. What can fail or cause harm?
4. What is the simplest structure that meets those needs?
5. What evidence would cause us to change the design?

## Evidence labels

Use these labels throughout design/review:
- **Observed**: directly supported by code, config, logs, docs, or user-provided facts.
- **Assumed**: needed to proceed but not yet verified.
- **Proposed**: design recommendation.

## Quality-attribute lens

Evaluate, when relevant:
- functional fitness
- security and privacy
- reliability/resilience/recoverability
- performance and scalability
- operability and observability
- maintainability/evolvability
- cost efficiency
- sustainability/resource efficiency
- usability/accessibility when architecture-sensitive
- compliance/governance
- AI trustworthiness and evaluation (for AI systems)

## Requirements quality

Good requirements identify behavior and constraints without prematurely prescribing implementation.

Bad: “Use Kafka to process events.”
Better: “The system must durably absorb bursts of up to X events/s, allow independent consumers, and replay 7 days of events.”

Bad: “Use Redis.”
Better: “P95 read latency must remain below X ms for a read-heavy data set that tolerates Y seconds of staleness.”

## Architecture option rule

Do not create fake alternatives. Only compare options with meaningful differences.

A useful option comparison answers:
- Which requirements does this optimize?
- Which requirement becomes harder?
- Which new failure modes appear?
- What operational burden is introduced?
- How hard is it to reverse?

## Decision reversibility

Classify major decisions:
- **Easy to reverse**: implementation/library details behind a stable interface.
- **Moderate**: database technology, hosting topology, event contracts.
- **Hard**: tenancy model, identity boundary, data ownership, public API semantics, cross-region consistency model.

Spend design effort proportionally.

## Failure-mode method

For each critical flow, inspect:
1. entry validation
2. authorization
3. dependency call
4. state mutation
5. response/acknowledgement
6. crash between any two steps
7. duplicate request
8. late/out-of-order message
9. partial third-party success
10. recovery/reconciliation

## Architecture gate exit criteria

### READY
- problem and scope are coherent
- core requirements known
- significant trust/data boundaries identified
- architecture supports critical flows
- top failure modes have treatment
- consequential decisions have rationale
- implementation can start in a reversible slice

### READY WITH ASSUMPTIONS
Same as READY, except non-critical unknowns are explicitly listed with validation plans.

### NOT READY
Use sparingly, only for blockers such as:
- unknown authority/source of truth for destructive writes
- unresolved identity/authorization model for sensitive data
- unverified third-party constraint that determines fundamental architecture
- inability to define expected consistency or recovery for money/critical state
- missing legal/contractual constraint that changes data location/retention

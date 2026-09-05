# Domain-Neutral Systems Design

System Design Architect can be used beyond software. The invariant is not the technology stack; it is the discipline of understanding purpose, actors, boundaries, flows, constraints, dependencies, failure modes, feedback, trade-offs, and change.

## First classify the system domain

Use the most relevant lens rather than forcing software terminology.

### Software / digital
Typical elements:
- users and services
- applications/components
- APIs/events
- databases/state
- infrastructure
- identity/security
- deployment/operations

### Business process / operations
Typical elements:
- customers/employees/vendors
- activities and handoffs
- queues/backlogs
- policies and approvals
- information and documents
- capacity/resources
- SLAs and exception paths
- controls, metrics, ownership

### Organization / operating model
Typical elements:
- roles and teams
- decision rights
- responsibilities
- coordination mechanisms
- incentives
- information flows
- governance
- feedback and performance measures

### Service design / customer experience
Typical elements:
- customer goals
- touchpoints/channels
- frontstage/backstage work
- handoffs
- service standards
- demand/capacity
- failure recovery
- feedback loops

### Physical / smart environment
Typical elements:
- people
- devices/equipment
- physical zones
- energy/material flows
- sensors/actuators
- safety constraints
- maintenance
- environmental dependencies

### Supply chain / logistics
Typical elements:
- suppliers
- inventory
- transport
- lead time
- buffers
- demand signals
- capacity constraints
- failure propagation
- recovery options

### Learning / education
Typical elements:
- learner goals
- prerequisite knowledge
- content/activities
- practice
- assessment
- feedback
- adaptation
- retention/transfer

Other domains are valid. Adapt the vocabulary to the actual system.

## Universal system questions

Regardless of domain, answer:

1. What outcome is the system trying to create?
2. Who or what participates in it?
3. Where is the boundary?
4. What enters, moves through, changes, and exits?
5. What state or resources accumulate?
6. What rules and decisions govern behavior?
7. What dependencies and handoffs exist?
8. Where are delays, bottlenecks, conflicts, or failure points?
9. What feedback loops reinforce or balance behavior?
10. What controls reduce risk?
11. How do we know the system is healthy?
12. What trade-offs shape the design?
13. How can the system evolve safely?

## Translation table

Do not use software words when they obscure the domain.

| Software concept | Domain-neutral equivalent |
|---|---|
| Component/service | Capability, role, process, unit, device |
| API/interface | Handoff, contract, channel, interaction boundary |
| Database/state | Record, inventory, knowledge, resource, system state |
| Queue | Backlog, waiting line, work-in-progress buffer |
| Authentication/authorization | Identity, eligibility, access, decision rights |
| Observability | Measurement, sensing, reporting, feedback |
| Deployment | Rollout, implementation, introduction into operation |
| Rollback | Reversal, contingency, return to prior operating state |
| Reliability | Resilience, continuity, consistency of outcome |
| Scaling | Capacity growth, replication, throughput expansion |
| Technical debt | Structural/process debt, accumulated workaround cost |

## Domain-specific quality attributes

Choose what matters rather than applying every software quality attribute.

Potential qualities include:
- effectiveness
- safety
- fairness
- speed/latency
- throughput/capacity
- reliability/continuity
- quality/accuracy
- cost
- accessibility/usability
- privacy/confidentiality
- compliance
- adaptability
- maintainability
- sustainability
- employee/customer experience
- learning effectiveness

Make important qualities measurable where meaningful.

## Feedback loops and unintended consequences

For human, organizational, operational, and physical systems, explicitly inspect feedback:

- **reinforcing loops** amplify behavior (for example, backlog → pressure → errors → rework → larger backlog);
- **balancing loops** stabilize behavior (for example, rising demand → added capacity → lower wait time);
- delays can make a good intervention appear ineffective or cause over-correction;
- local optimization can damage the whole system.

When feedback is important, use a causal/feedback map in addition to a linear process flow.

## Human systems require incentive and decision-right analysis

When people or organizations are central, ask:
- Who makes each consequential decision?
- Who is accountable for the outcome?
- What information do they have at decision time?
- What incentives could produce behavior different from the intended process?
- Where do informal workarounds arise and why?
- Which steps require judgment rather than standardization?

Do not assume a process diagram describes actual behavior.

## Existing non-software systems

Evidence can include:
- policies and SOPs
- interviews/user-provided observations
- process maps
- forms/templates
- reports/metrics
- schedules
- contracts
- physical layouts
- system/device inventories
- tickets/cases
- financial or operational records

Reconstruct the **as-is system** from evidence before proposing a target system. Preserve useful existing behavior and improve incrementally.

## Architecture decisions become system decisions

ADRs can still be used, but rename them when appropriate (for example, System Decision Record or Operating Model Decision). Keep the same core structure: context, options, decision, rationale, consequences, and reconsideration trigger.

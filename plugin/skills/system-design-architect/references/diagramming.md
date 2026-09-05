# System Visualization and Diagramming Guidance

Visual models are first-class system-design artifacts. Use them to expose structure, flow, causality, state, responsibility, risk, and change.

Read `references/visual-first.md` for the default visual-first response protocol.

## Choose the view by the question

### System context / boundary
Use to show:
- system purpose/scope;
- primary actors/stakeholders;
- system in scope;
- external dependencies/environment;
- labeled boundary crossings.

### End-to-end process / value stream / sequence
Use to show:
- trigger/input;
- major stages;
- handoffs/interfaces;
- decisions;
- waiting/queues;
- output/outcome.

### Service blueprint
Use for services with visible customer/user experience and backstage work. Separate, when useful:
- customer journey;
- frontstage interaction;
- backstage activity;
- supporting teams/systems;
- data/policy/legislation/resources.

### Responsibility / swimlane map
Use when ownership and handoffs are central. Make the owner of each action and transition visible.

### Decision map
Use when branching, authority, eligibility, approval, or escalation shapes the system.

### State machine
Use when lifecycle transitions and legal/illegal state changes matter.

### Capacity / queue / bottleneck view
Use when demand, throughput, WIP, staffing, inventory, or delays drive system behavior.

### Causal-loop diagram
Use when feedback, incentives, delayed effects, recurring workarounds, or unintended consequences drive behavior. Mark reinforcing/balancing relationships where useful.

### Stock-and-flow / resource map
Use when accumulated state, inventory, money, materials, energy, or capacity changes over time.

### Failure / recovery map
Use when resilience is central. Show failure point, containment, degraded mode, recovery, verification, and escalation.

### Current → transition → target
Use for change. Keep current, transitional, and future states visually distinct.

### Adaptive operating loop
Use for operating systems expected to stay healthy:
Desired state → Sense → Detect → Diagnose → Decide/Authorize → Respond → Recover → Verify → Learn → Adapt.

## Software-specific views

Use C4-style abstraction to avoid mixed-level boxes and lines.

### System Context
Show users/roles, system, external systems, and relationships. Do not show internal frameworks.

### Container
Show major deployable/runtime units and data stores: web/mobile app, API/backend, worker, workflow engine, database, object store, model gateway, etc. Label technology only when it matters to a decision.

### Component
Use only when internal responsibility boundaries within a container matter.

### Dynamic / sequence
Use for critical runtime paths such as side effects, authentication, async processing, retrieval/model/tool execution, and failure/reconciliation.

### Deployment
Use when zones, regions, networks, edge placement, isolation, or HA topology materially affects the design.

## Visual layering

Do not force the full system into one graph. Layer complexity:
1. boundary and actors;
2. major capabilities;
3. end-to-end flow;
4. decisions/state/resources;
5. dependencies/interfaces;
6. capacity/controls/failure overlay;
7. feedback/health;
8. transition/target.

## Evidence and state

For existing-system work, distinguish visually where possible:
- Observed;
- Assumed;
- Unknown;
- Proposed.

Always label AS-IS and TARGET explicitly. Do not make a proposal look like an observed fact.

## Diagram quality checklist

- question/title/scope clear;
- consistent abstraction level;
- every node has a meaningful role;
- relationships labeled with verbs/transfers;
- external vs internal clear;
- current vs target clear;
- important handoffs visible;
- trust/control boundaries visible where relevant;
- queues/bottlenecks/failures placed at their actual location;
- no unexplained acronyms;
- no decorative infrastructure or decorative arrows;
- readable without a long prose translation.

Prefer a small set of focused, evolving views over a single comprehensive but unreadable diagram.
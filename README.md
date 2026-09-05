# System Design Architect

A vendor-neutral **Agent Skill** for designing, reviewing, explaining, and evolving complex systems before implementation or change.

It began as a software-architecture skill. From v1.2 it is intentionally broader: a **system** can be software, an AI agent, a business process, an operating model, a service, a smart environment, a supply chain, a learning system, or another network of interacting parts organized around an outcome.

## What makes it different

System Design Architect combines three independent choices:

### Lifecycle mode
- **New System Design** — start from an idea or desired outcome.
- **Existing System Review** — reconstruct the as-is system from evidence before recommending change.
- **Change Design** — understand the relevant current system before adding a new capability.

### Domain lens
- **Software / digital** — services, APIs, data, identity, infrastructure, reliability, deployment.
- **General systems** — actors, handoffs, resources, decision rights, capacity, controls, feedback, resilience, outcomes.

### Presentation mode
- **Architect Mode** — produce the design/review efficiently.
- **Teaching Mode** — progressively unfold a system graph so the learner understands why every major part exists.

## Teaching Mode

Instead of showing a dense final diagram first, Teaching Mode unfolds the system in stages:

```text
Purpose / outcome
      ↓
Actors / stakeholders
      ↓
Boundary / environment
      ↓
Inputs, resources, outputs
      ↓
Core flow
      ↓
Rules / decisions
      ↓
Dependencies / interfaces
      ↓
Failure modes / constraints
      ↓
Feedback / measurement
      ↓
Options / trade-offs
      ↓
Target system
      ↓
Transition / implementation
```

At each stage the skill preserves the previous graph, adds only the new layer, explains **why it matters**, gives an example, identifies a common failure, and connects the stage to the next design question.

For existing systems, it unfolds the **as-is graph first**, then the findings, then the **target graph**. Observed and proposed state are never silently mixed.

See [`references/teaching-mode.md`](references/teaching-mode.md).

## Beyond software

The same systems discipline applies across many fields when the vocabulary is adapted correctly.

Examples:
- employee onboarding and People Operations
- organizational operating models
- customer-service operations
- restaurant or hospitality service flow
- logistics and supply chains
- smart-home / building systems
- manufacturing or physical operations
- learning and education systems
- finance or approval processes
- public/service-delivery workflows

The skill does **not** force APIs, databases, microservices, or software security concepts onto these problems. It translates them into the domain's real building blocks: roles, capabilities, handoffs, records/resources, queues, decision rights, controls, capacity, failure recovery, measurement, and feedback loops.

See [`references/domain-neutral-systems.md`](references/domain-neutral-systems.md).

## Why this exists

AI tools make it extremely easy to jump from an idea to a solution before the purpose, system boundary, ownership, failure modes, feedback loops, trust/control boundaries, or trade-offs are understood.

System Design Architect inserts disciplined reasoning between **idea/current system** and **implementation/change**:

```text
Idea / Existing System
        ↓
Purpose + Boundary
        ↓
Actors + Requirements
        ↓
State / Resources + Flows
        ↓
Dependencies + Risks
        ↓
Options + System Views
        ↓
Controls + Resilience
        ↓
Feedback + Measurement
        ↓
Decisions + Fitness Checks
        ↓
Implementation / Transition
```

The skill is intentionally opinionated about **simplicity**. It challenges unnecessary infrastructure, automation, handoffs, approvals, agents, process ceremony, and organizational complexity when the requirements do not justify them.

## Core principles

- Start with the outcome, not the technology or fashionable framework.
- Distinguish **Observed / Assumed / Proposed**.
- Establish the system boundary.
- Make ownership and decision rights explicit.
- Map flows, handoffs, state/resources, dependencies, and exception paths.
- Treat dependencies as fallible.
- Design controls and recovery, not only the happy path.
- Examine capacity, bottlenecks, and failure propagation.
- Make feedback loops and measures explicit.
- Prefer reversible, evolutionary change.
- Record significant decisions and trade-offs.
- Test important architectural/system claims with fitness checks.
- For AI: models can interpret and propose; deterministic controls must enforce critical permissions and side effects.

## Example prompts

### Software
```text
Use System Design Architect. I want to build a family budget app that imports bank CSVs and categorizes expenses with AI.
```

### Existing repository
```text
Review this repository. Reconstruct the current architecture from evidence first, identify the highest-risk issues, then give me the smallest useful evolutionary target architecture.
```

### Teaching Mode
```text
Use Teaching Mode. Teach me how this marketplace works by unfolding the system graph one stage at a time. Do not show me the finished architecture first.
```

### Business process
```text
Design our employee onboarding operating system. Treat People Ops, IT, payroll, managers and new hires as actors in a business system. Do not assume this is primarily a software problem.
```

### Existing non-software system
```text
Review our restaurant dinner-service operation. Reconstruct the as-is flow, queues and handoffs first, then teach me why the bottlenecks happen and progressively show the target system.
```

## Methodology

The skill combines:
- systems thinking and feedback-loop analysis
- Well-Architected quality lenses
- C4-style software architecture views where applicable
- Architecture/System Decision Records
- evidence-grounded existing-system discovery
- data consistency and transaction reasoning
- reliability/resilience and failure-mode design
- security/privacy/governance controls
- AI/agent grounding, autonomy, tool mediation and evals
- architecture/system fitness checks
- progressive teaching

See [`references/sources.md`](references/sources.md).

## Important references

- [`references/process.md`](references/process.md)
- [`references/domain-neutral-systems.md`](references/domain-neutral-systems.md)
- [`references/teaching-mode.md`](references/teaching-mode.md)
- [`references/discovery.md`](references/discovery.md)
- [`references/data-systems.md`](references/data-systems.md)
- [`references/reliability.md`](references/reliability.md)
- [`references/security.md`](references/security.md)
- [`references/ai-systems.md`](references/ai-systems.md)
- [`references/architecture-fitness.md`](references/architecture-fitness.md)

## Examples

- [`examples/new-ai-hr-assistant.md`](examples/new-ai-hr-assistant.md)
- [`examples/existing-agent-review.md`](examples/existing-agent-review.md)
- [`examples/non-software-employee-onboarding-system.md`](examples/non-software-employee-onboarding-system.md)

## Templates

- [`templates/DESIGN.md`](templates/DESIGN.md)
- [`templates/ARCHITECTURE_REVIEW.md`](templates/ARCHITECTURE_REVIEW.md)
- [`templates/ADR.md`](templates/ADR.md)
- [`templates/THREAT_MODEL.md`](templates/THREAT_MODEL.md)
- [`templates/FITNESS_CHECKS.md`](templates/FITNESS_CHECKS.md)

## Validation and evals

Run the local project validator:

```bash
python scripts/validate_skill.py
```

CI also runs the Agent Skills reference validator and validates `evals/evals.json`.

The eval suite tests, among other behaviors, whether the skill:
- avoids unjustified distributed architecture;
- recognizes when high-scale event infrastructure is justified;
- protects privileged AI actions;
- avoids unnecessary RAG/vector databases;
- teaches progressively rather than dumping an unexplained final graph;
- uses domain-appropriate language for non-software systems;
- reconstructs existing non-software systems before proposing change.

## License

Apache License 2.0. See [`LICENSE`](LICENSE).

## Contributing

Contributions are welcome, particularly new domain lenses, progressive-teaching examples, system-review cases, failure-mode patterns, and eval scenarios. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Versioning

The project follows semantic versioning for skill behavior and methodology. See [`CHANGELOG.md`](CHANGELOG.md).

# System Design Architect

A vendor-neutral **Agent Skill** that forces good system design *before coding* and helps existing systems evolve toward stronger architecture without reflexive rewrites.

It is designed for:
- new software/product ideas
- existing architecture reviews
- AI and agent systems
- APIs and integrations
- workflow/automation systems
- distributed systems
- sensitive business systems

## Why this exists

AI coding tools make it extremely easy to move from idea to implementation before the problem, trust boundaries, data ownership, failure semantics, or operational model are understood.

System Design Architect inserts an architecture discipline between **idea** and **build**:

```text
Idea / Existing System
        ↓
Requirements + Constraints
        ↓
Risk + Data + Domain
        ↓
Architecture Options
        ↓
Security + Reliability + AI Gates
        ↓
Trade-offs + ADRs
        ↓
Implementation / Migration Slices
        ↓
Build
```

The skill is intentionally opinionated about **simplicity**. It challenges unnecessary microservices, queues, event buses, vector databases, multi-agent systems, and other infrastructure when the requirements do not justify them.

## Methodology

The skill synthesizes four complementary bodies of practice:

1. **Well-Architected quality lenses** — operational excellence, security, reliability, performance, cost, sustainability.
2. **C4-style architecture communication** — context, container, component, dynamic, and deployment views only when useful.
3. **Architecture Decision Records (ADRs)** — explicit decisions, alternatives, consequences, and reconsideration triggers.
4. **AI/agent design controls** — model necessity, grounding, tool mediation, least privilege, prompt-injection boundaries, human approval, evals, and durable state ownership.

See [`references/sources.md`](references/sources.md).

## Install / use

Agent Skills-compatible tools can install or point to this directory as a skill. The required file is [`SKILL.md`](SKILL.md).

For tools that do not implement Agent Skills, copy the `SKILL.md` instructions into the tool's reusable-agent/instructions mechanism and keep the `references/` directory available.

### Example prompts

```text
Use System Design Architect. I want to build a family budget app that imports bank CSVs and categorizes expenses with AI.
```

```text
Use System Design Architect to review this repository. Reconstruct the current architecture first, identify the highest-risk issues, then give me an evolutionary target architecture. Do not rewrite it just for cleanliness.
```

```text
Use System Design Architect in Change Design mode. I want to add autonomous employee onboarding actions to this existing HR platform.
```

## What it produces

Depending on complexity:
- problem/scope definition
- functional and non-functional requirements
- evidence ledger: Observed / Assumed / Proposed
- criticality and risk classification
- domain/data ownership model
- architecture options and recommendation
- C4-style diagrams
- critical sequence/data flows
- API/tool/event boundary guidance
- security/privacy review
- failure and reliability design
- scale/performance/cost analysis
- AI grounding/tool/eval design
- ADR candidates
- implementation/migration slices
- architecture readiness gate

## Existing systems

The skill uses an **as-is -> risks -> smallest target -> migration** approach. It explicitly avoids “rewrite syndrome.” Working behavior is preserved unless a rewrite is backed by evidence.

## AI systems

The skill enforces several architectural principles:

- An LLM is not a source of truth.
- Prompt text is not an authorization system.
- Critical rules should be deterministic.
- Privileged operations should pass through narrow tools/domain services.
- Durable workflow state should live outside model context.
- RAG is used only when retrieval is actually needed.
- Multi-agent architecture must justify its added complexity.
- Evals are part of system design, not a launch-afterthought.

## Templates

- [`templates/DESIGN.md`](templates/DESIGN.md)
- [`templates/ARCHITECTURE_REVIEW.md`](templates/ARCHITECTURE_REVIEW.md)
- [`templates/ADR.md`](templates/ADR.md)
- [`templates/THREAT_MODEL.md`](templates/THREAT_MODEL.md)
- [`templates/FITNESS_CHECKS.md`](templates/FITNESS_CHECKS.md)

Create a new design dossier:

```bash
python scripts/scaffold.py "My Product" --out ./architecture
```

## Validation

A dependency-free repository sanity check is included:

```bash
python scripts/validate_skill.py
```

CI also runs the official Agent Skills reference validator and validates `evals/evals.json`. The eval set intentionally checks that the skill avoids unjustified microservices, Kafka/event infrastructure, RAG/vector databases, and unsafe direct agent writes—and recognizes when those patterns are actually justified.

For implementations that use the Agent Skills reference validator, you can additionally run the standard `skills-ref validate` command against the skill directory.

## Contributing

Contributions are welcome, especially:
- architecture review examples
- failure-mode patterns
- AI/agent eval patterns
- security review improvements
- clearer lightweight workflows

Please see [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

Apache License 2.0. See [`LICENSE`](LICENSE).

## Architecture fitness

A design is not considered good merely because every section is filled in. For consequential requirements, the skill maps **requirement → architecture mechanism → verification → pass condition**. This turns architectural intent into something teams can test and preserve.

## Versioning

The project follows semantic versioning for the skill metadata. See `CHANGELOG.md` for behavior and methodology changes.

## Security

See `SECURITY.md` for vulnerability-reporting guidance.

# System Design Architect

An open-source AI skill that grounds new and existing software systems in rigorous system design before implementation.

System Design Architect helps an AI coding assistant act like a disciplined software architect before it acts like an implementer. It can design greenfield systems, review existing architectures, evaluate proposed changes, challenge unnecessary complexity, and produce implementation-ready architecture decisions.

## Why this exists

AI coding tools are very good at turning ideas into code quickly. That speed can also make it easy to skip the architectural work that should happen first: clarifying requirements, identifying system boundaries, deciding what must be deterministic, defining trust boundaries, planning failure modes, and understanding trade-offs.

This skill inserts a lightweight but rigorous architecture process before implementation.

It is designed to be:

- **Evidence-grounded** — distinguishes what is observed, assumed, and proposed.
- **Complexity-aware** — applies only as much architecture as the system needs.
- **AI-aware** — explicitly reviews agent autonomy, tool access, grounding, evaluation, and human approval.
- **Security-aware** — treats authorization, trust boundaries, auditability, and least privilege as architecture concerns.
- **Pragmatic** — prefers the simplest architecture that satisfies the requirements.
- **Incremental** — improves existing systems without demanding unnecessary rewrites.
- **Vendor-neutral** — works across clouds, frameworks, languages, and AI stacks.

## What it does

The skill supports three modes.

### 1. New System Design

Use when starting from an idea or requirements.

Typical flow:

1. Frame the problem.
2. Identify actors, use cases, requirements, constraints, and assumptions.
3. Calibrate architecture depth.
4. Model the system context and critical flows.
5. Define data ownership and system boundaries.
6. Explore credible architecture options.
7. Select and document the recommended architecture.
8. Review security, reliability, operability, performance, cost, and AI-specific risks.
9. Record significant decisions as ADRs.
10. Produce implementation slices and a readiness decision.

### 2. Existing System Review

Use when a system or repository already exists.

The skill reconstructs the as-is architecture from evidence, identifies concrete weaknesses, defines the smallest useful target architecture, and creates an incremental migration path.

### 3. Change Design

Use when adding a significant capability to an existing system.

It first understands the relevant current architecture, then determines how the new capability should fit without destabilizing the system or creating unnecessary new infrastructure.

## Core principles

- Start with the problem, not the technology.
- Prefer the simplest architecture that satisfies current requirements.
- Separate domain logic from orchestration.
- Treat external dependencies as unreliable.
- Make failure paths explicit.
- Treat security boundaries as architectural, not prompt-based.
- Require authorization, validation, auditability, and idempotency for side effects where appropriate.
- Let LLMs interpret; let deterministic systems enforce invariants.
- Give agents narrow tools rather than broad production credentials.
- Do not introduce infrastructure without explaining the requirement it satisfies.
- Record important trade-offs and architecture decisions.
- Evolve existing systems incrementally where possible.

## Repository structure

```text
system-design-architect/
├── SKILL.md
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── references/
│   ├── process.md
│   ├── ai-systems.md
│   ├── security.md
│   ├── diagramming.md
│   ├── review-matrix.md
│   └── sources.md
├── templates/
│   ├── DESIGN.md
│   ├── ARCHITECTURE_REVIEW.md
│   └── ADR.md
├── examples/
│   ├── new-ai-hr-assistant.md
│   └── existing-agent-review.md
├── scripts/
│   ├── scaffold.py
│   └── validate_skill.py
└── .github/workflows/
    └── validate.yml
```

## Quick start

The core skill is `SKILL.md`. Install or copy this repository into any AI environment that supports the Agent Skills format.

To create a local architecture dossier for a new system:

```bash
python scripts/scaffold.py "My Product" --out ./architecture
```

Validate the repository structure with:

```bash
python scripts/validate_skill.py
```

## Example prompts

```text
I want to build a global employee onboarding platform with AI assistance.
Design the system before we write code.
```

```text
Review this repository as an existing system. Reconstruct its architecture from evidence,
identify the highest-risk weaknesses, and propose the smallest useful migration plan.
```

```text
We want to add an autonomous remediation agent to this platform.
Design how it should fit into the existing architecture and define its safety boundaries.
```

## Design foundations

The methodology is informed by established architecture and AI-risk practices, including:

- AWS Well-Architected Framework
- Google Cloud Well-Architected Framework
- C4 model for software architecture visualization
- Architecture Decision Records (ADRs)
- NIST AI Risk Management Framework
- OWASP guidance for LLM and agentic systems
- The open Agent Skills specification

See `references/sources.md` for source notes and links.

## License

Apache License 2.0. See `LICENSE`.

## Contributing

Contributions are welcome. See `CONTRIBUTING.md`.

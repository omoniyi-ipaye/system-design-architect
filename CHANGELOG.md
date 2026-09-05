# Changelog

## 2.0.0 - 2026-09-05
- Make domain-neutral systems design the core identity of the skill rather than an extension to software architecture.
- Add a universal lifecycle: purpose → design → verify/validate → operate → sense → detect → diagnose → respond → recover → verify → learn → adapt.
- Add Mode D: Adaptive Operation / System Health for already-running systems.
- Make verification vs validation explicit across all domains.
- Add outcome hierarchy: activity, output, outcome, and system health.
- Add multi-flow analysis for work, information, authority/decision, state, money/material/resource flows.
- Treat handoffs/interfaces as contracts with ownership, acknowledgement, timing, failure behavior, and escalation.
- Add capacity, queue, backlog, bottleneck, and demand-vs-processing analysis as first-class system design.
- Add operability maturity: Observable, Recoverable, Adaptive, and Self-Healing Within Bounds.
- Formalize bounded self-healing with autonomy levels L0-L3 and an explicit adaptation envelope.
- Prohibit silent autonomous changes to purpose, critical policy, authority model, safety boundaries, or sources of truth.
- Add `templates/SYSTEM_HEALTH.md` for live system-health assessments.
- Upgrade design and review templates to include verification, validation, feedback, recovery, adaptation, and operability gates.
- Upgrade `scripts/scaffold.py` with `--mode design|review|health|adaptive`.
- Expand the review matrix to cover whole-system outcomes, ownership, flows, capacity, incentives, sensing, recovery, adaptation governance, and AI safety.
- Expand evals to cover verification-vs-validation, capacity constraints, system drift, bounded self-healing, and refusal of uncontrolled autonomous redesign.
- Ground the methodology more explicitly in systems engineering, NIST resilience, SRE, service/process design, and software/AI architecture practices.

## 1.2.0 - 2026-09-05
- Expand System Design Architect from software-only architecture into domain-neutral systems design.
- Add independent lifecycle, domain-lens, and presentation-mode selection.
- Add Teaching Mode with a progressively unfolding system graph.
- Add domain-neutral mappings for business processes, organizations, services, physical/smart environments, supply chains, and learning systems.
- Add feedback-loop, decision-right, incentive, handoff, capacity, and resource-flow analysis for non-software systems.
- Add teaching and non-software eval scenarios.
- Add a non-software employee-onboarding system example.

## 1.1.0 - 2026-09-05
- Add existing-system discovery protocol.
- Add data consistency, transaction, schema-evolution, and reconciliation guidance.
- Add reliability guidance for backpressure, overload, quotas, and blast radius.
- Add architecture fitness checks that map requirements to verification.
- Expand threat-model and fitness-check templates.
- Add Agent Skills eval scenarios for overengineering, event scale, privileged agents, and unnecessary RAG.
- Strengthen validation and CI guidance.
- Replace abbreviated license file with the complete Apache License 2.0 text.
- Add security policy and broaden examples.

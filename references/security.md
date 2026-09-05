# Security and Privacy Architecture Review

Use this as a practical architecture-level review, not a compliance certification.

## Trust boundaries
- Identify users, services, agents, networks, third parties, and data stores.
- Mark where identity, privilege, or data sensitivity changes.

## Identity and authorization
- Authenticate at an appropriate trusted boundary.
- Enforce authorization server-side/domain-side.
- Prefer least-privilege scoped credentials.
- Separate human identity, service identity, and agent/tool identity.
- Avoid ambient broad credentials for autonomous components.

## Data
- Classify sensitive data.
- Minimize collection and propagation.
- Define source of truth, retention, deletion, backup, and residency requirements.
- Encrypt in transit and at rest where appropriate.
- Avoid logging secrets or unnecessary personal data.

## Inputs and integrations
- Validate inputs at trust boundaries.
- Treat third-party and model outputs as untrusted.
- Verify webhook authenticity and replay protections where relevant.
- Pin/monitor dependencies proportionally to supply-chain risk.

## Privileged actions
For every high-impact write, define:
- who/what may request it
- who/what authorizes it
- what validation is deterministic
- whether approval is required
- idempotency/replay behavior
- audit record
- rollback/compensating action

## AI-specific
- Never treat prompt text as an authorization mechanism.
- Isolate untrusted retrieved content from privileged tool control.
- Give tools narrow schemas and scoped credentials.
- Log/trace high-impact tool requests and outcomes.

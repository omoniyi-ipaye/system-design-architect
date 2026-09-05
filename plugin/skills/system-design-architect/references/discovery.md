# Existing-System Discovery Protocol

Use this when reviewing a repository or deployed system. The goal is to reconstruct architecture from evidence before recommending change.

## Inspect in this order
1. Repository tree and workspace/package boundaries.
2. Application entry points and runtime processes.
3. Dependency manifests and lockfiles.
4. Environment/configuration and feature flags.
5. Authentication and authorization middleware/policies.
6. API routes, RPC/tool contracts, schemas, and public interfaces.
7. Database schemas, migrations, ORM models, and data access boundaries.
8. Background jobs, queues, schedulers, webhooks, and event consumers.
9. External integrations and credential boundaries.
10. Cache/session/state stores.
11. Infrastructure-as-code, containers, orchestration, networking, and deployment topology.
12. CI/CD, release, rollback, and migration automation.
13. Logging, metrics, tracing, alerting, and runbooks.
14. Tests and architecture-sensitive fixtures.
15. AI prompts, model gateways, retrieval, tools, memory, evals, and approval paths.

## Evidence map
For every architectural claim record:
- **Observed**: file/path/config/log/doc that proves it.
- **Assumed**: plausible but not yet verified.
- **Unknown**: material area with no evidence.
- **Proposed**: recommendation, never mixed with as-is facts.

Prefer file paths and concrete artifacts over vague summaries.

## Critical-flow tracing
Trace at least one representative path for each applicable category:
- read path
- write/side-effect path
- authentication/authorization path
- async/background path
- external integration path
- AI/tool execution path
- failure/recovery path

For each step capture caller, callee, data, auth context, state mutation, retries, timeout, and failure handling.

## Stop conditions
Do not require exhaustive repo archaeology. Stop discovery when enough evidence exists to answer the architectural question safely and identify the highest-impact unknowns.

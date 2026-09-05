# Architecture Review Matrix

Rate only where evidence exists: **Strong / Adequate / Needs attention / Critical / Unknown**.

| Dimension | Review questions |
|---|---|
| Problem fit | Does architecture directly support the actual user/business problem? |
| Simplicity | Is every major component justified by a requirement? |
| Boundaries | Are domain, orchestration, presentation, and integrations separated coherently? |
| Data ownership | Is each important datum's source of truth and lifecycle clear? |
| Security | Are identity, authorization, secrets, trust boundaries, and privileged actions enforced? |
| Privacy | Is sensitive data minimized, retained intentionally, and prevented from unnecessary propagation? |
| Reliability | Are critical failures, partial success, retries, idempotency, backup/recovery handled? |
| Performance | Are hot paths and scale assumptions explicit and measured where possible? |
| Operability | Can operators detect, diagnose, mitigate, rollback, and recover? |
| Evolvability | Can important changes occur without broad rewrites or brittle coupling? |
| Cost | Are expensive components justified and observable? |
| AI necessity | Is AI used only where probabilistic capability adds value? |
| AI grounding | Are authoritative sources, retrieval, provenance, and conflicts handled? |
| AI action safety | Are tool permissions narrow and high-impact actions validated/audited/approved? |
| AI evaluation | Are representative and adversarial evals part of the lifecycle? |

Every `Needs attention` or `Critical` rating must include evidence and a proposed treatment.

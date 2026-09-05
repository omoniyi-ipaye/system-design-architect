# AI and Agent System Design

## 1. Model necessity test

Use AI when the task benefits from probabilistic interpretation, synthesis, language understanding, multimodal understanding, flexible planning, or fuzzy classification.

Prefer deterministic code for:
- authorization
- financial/entitlement calculations
- invariant enforcement
- exact transformations
- workflow state transitions
- destructive action policy
- schema validation
- access control

A hybrid design is often best: model proposes or interprets; deterministic services validate and execute.

## 2. Grounding model

Define authoritative sources and retrieval semantics.

Ask:
- What information is authoritative?
- Is it structured, unstructured, or both?
- Does retrieval need semantic search, lexical search, filters, SQL/API lookup, or a hybrid?
- How fresh must information be?
- How will conflicting sources be handled?
- Can responses cite/provenance-link the evidence?

Do not add RAG merely because an LLM is present.

## 3. Tool boundary

Preferred privileged-action path:

User -> Agent/Model -> Narrow Tool Contract -> Authorization/Policy -> Deterministic Domain Service -> External System

The tool contract should expose the minimum operation and minimum data necessary.

## 4. Prompt injection and untrusted context

Treat retrieved text, emails, webpages, documents, tool output, and user-provided files as potentially untrusted instructions.

Architectural controls may include:
- data/instruction separation
- allowlisted tools
- scoped credentials
- argument validation
- policy enforcement outside the model
- explicit confirmation for high-impact side effects
- output encoding/sanitization at execution boundaries
- audit of tool calls and approvals

## 5. Agent state and memory

Separate:
- conversation context
- workflow state
- durable domain state
- user preference memory
- retrieval corpus

Do not hide business-critical state only inside model context. Durable process state belongs in a deterministic store with explicit schema/lifecycle.

## 6. Evals

AI systems need pre-production and regression evaluations. Evaluate the system, not only the base model.

Potential dimensions:
- task success
- groundedness / citation correctness
- tool selection
- argument correctness
- authorization adherence
- refusal/approval behavior
- prompt-injection resistance
- recovery from tool failures
- latency
- cost

Use representative scenarios, edge cases, adversarial cases, and previously observed production failures.

## 7. Human oversight

Require human approval when the combination of impact, uncertainty, and reversibility warrants it. Examples can include privileged account changes, money movement, employment-impacting decisions, legal submissions, deletion, or broad external communication.

Human-in-the-loop is not a substitute for authorization, validation, and audit.

## 8. Multi-agent test

Before adding multiple agents, prove that role separation creates a benefit that cannot be achieved cleanly by a single orchestrator with tools/workflows.

Multi-agent systems add:
- more nondeterminism
- more state coordination
- higher latency/cost
- harder debugging/evals
- broader security surface

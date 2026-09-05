# Methodology Sources

System Design Architect is an original synthesis. These sources are used as discipline and quality lenses, not as vendor-specific prescriptions or claims of certification.

| Source | Document / version | Principles used here | Last verified |
|---|---|---|---|
| INCOSE | Systems Engineering Handbook / systems engineering resources | domain-neutral system definition, lifecycle thinking, interfaces, requirements, verification/validation, transdisciplinary design | 2026-09 |
| NIST | SP 800-160 Vol. 2 Rev. 1 | cyber-resiliency concepts: anticipate, withstand, recover, adapt; engineered resilience and governance | 2026-09 |
| Google SRE | Site Reliability Engineering / SRE Workbook concepts | measurable service objectives, monitoring, incident learning, error-budget-style operational feedback | 2026-09 |
| Agent Skills | Specification + evaluating skills guidance | skill structure, progressive disclosure, official validation, eval-driven iteration | 2026-09 |
| AWS | Well-Architected Framework / Reliability Pillar | reliability, operations, monitoring, failure recovery, adapting to demand | 2026-09 |
| Google Cloud | Well-Architected Framework | reliability, security, operations, performance, cost, sustainability | 2026-09 |
| Microsoft Azure | Well-Architected Framework | reliability, security, cost, operations, performance | 2026-09 |
| C4 model | Current C4 documentation | context/container/component/dynamic/deployment views for software systems | 2026-09 |
| MADR / ADR community | Architecture Decision Records | decision context, options, rationale, consequences, reconsideration | 2026-09 |
| NIST | AI RMF + Generative AI Profile | AI risk, governance, measurement, trustworthiness | 2026-09 |
| OWASP GenAI Security Project | Top 10 for Agentic Applications 2026 + Agent Control resources | agent privilege, tool misuse, untrusted context, identity, control boundaries | 2026-09 |
| Model Context Protocol | Current specification | tool/resource boundaries and interoperability context | 2026-09 |
| Service blueprint practice | Public-service and service-design blueprint methods | frontstage/backstage/supporting-system views, current/target service flow | 2026-09 |

## How the synthesis is used

### Systems thinking / systems engineering
Provides the domain-neutral foundation: purpose, boundary, stakeholders, requirements, interfaces, lifecycle, verification, validation, and whole-system optimization.

### Reliability / resilience
Provides the discipline to anticipate failure, sense degradation, recover safely, and adapt using evidence rather than treating launch as the end of design.

### Process / service / operating-model design
Extends interface, state, queue, capacity, decision-right, and feedback concepts to human and organizational systems.

### Software architecture
C4 and Well-Architected frameworks provide software-specific views and quality lenses when the domain is digital.

### AI / agents
NIST AI RMF, OWASP, and tool-boundary practices add model uncertainty, grounding, autonomy, prompt-injection, tool permission, state, and evaluation concerns.

## Links
- INCOSE Systems Engineering Handbook: https://www.incose.org/resources-publications/technical-publications/se-handbook/
- INCOSE systems engineering overview: https://www.incose.org/about-systems-engineering/
- NIST SP 800-160 Vol. 2 Rev. 1: https://csrc.nist.gov/pubs/sp/800/160/v2/r1/final
- Google SRE books: https://sre.google/books/
- Agent Skills: https://agentskills.io/specification
- Agent Skills eval guidance: https://agentskills.io/skill-creation/evaluating-skills
- AWS Well-Architected: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- Google Cloud Well-Architected: https://docs.cloud.google.com/docs/get-started/well-architected-framework
- Azure Well-Architected: https://learn.microsoft.com/azure/well-architected/
- C4: https://c4model.com/
- MADR: https://adr.github.io/madr/
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
- NIST Generative AI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- OWASP Agentic Top 10 2026: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- MCP: https://modelcontextprotocol.io/

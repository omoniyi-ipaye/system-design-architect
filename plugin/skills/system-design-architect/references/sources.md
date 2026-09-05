# Methodology Sources

System Design Architect is an original synthesis. These sources are used as discipline and quality lenses, not as vendor-specific prescriptions or claims of certification.

| Source | Document / version | Principles used here | Last verified |
|---|---|---|---|
| INCOSE | Systems Engineering Handbook / systems-engineering guidance | domain-neutral systems lifecycle, stakeholder needs, interfaces, verification/validation, lifecycle thinking | 2026-09 |
| INCOSE MBSE Patterns WG | Current working-group guidance | reusable model patterns across needs, requirements, design, failure modes, production and sustainment | 2026-09 |
| UK Government Office for Science | Systems Thinking Toolkit for Civil Servants | system mapping, causal-loop diagrams, feedback, leverage points, testing maps with stakeholders | 2026-09 |
| HM Treasury | Test and Learn / complexity guidance | actor mapping, observation, system mapping, learning from real operation | 2026-09 |
| Digital NSW | Service Blueprint guidance | visual end-to-end current/target/future service mapping across users, teams, systems, process, legislation and data | 2026-09 |
| NIST | SP 800-160 Vol. 2 Rev. 1 | cyber resilience concepts: anticipate, withstand, recover, adapt; engineered resilience | 2026-09 |
| Google SRE | Site Reliability Engineering / workbook principles | SLOs, monitoring, error-budget thinking, incident learning, operational feedback | 2026-09 |
| AWS | Well-Architected Framework / Reliability Pillar | reliability, operations, monitoring, recovery, adapting to demand | 2026-09 |
| Google Cloud | Well-Architected Framework | reliability, security, operations, performance, cost, sustainability | 2026-09 |
| Microsoft Azure | Well-Architected Framework | reliability, security, cost, operational excellence, performance | 2026-09 |
| C4 model | Current documentation | software context/container/component/dynamic/deployment visual views | 2026-09 |
| MADR / ADR community | Architecture Decision Records | decision context, drivers, options, rationale, consequences, reconsideration | 2026-09 |
| NIST | AI RMF + Generative AI Profile | AI risk, governance, measurement, trustworthiness | 2026-09 |
| OWASP GenAI Security Project | Agentic Top 10 / AI agent guidance | agent privilege, tool misuse, untrusted context, identity and control boundaries | 2026-09 |
| Model Context Protocol | Current specification | tool/resource boundaries and interoperability context | 2026-09 |
| Agent Skills | Specification + evaluation guidance | skill structure, progressive disclosure, validation, eval-driven iteration | 2026-09 |

## Links

- INCOSE: https://www.incose.org/resources-publications/technical-publications/se-handbook/
- INCOSE MBSE Patterns Working Group: https://www.incose.org/group/mbse-patterns-working-group/
- UK Systems Thinking Toolkit: https://www.gov.uk/government/publications/systems-thinking-for-civil-servants/toolkit
- Digital NSW Service Blueprint: https://www.digital.nsw.gov.au/delivery/digital-service-toolkit/activities-and-templates/service-blueprint
- NIST SP 800-160 Vol. 2 Rev. 1: https://csrc.nist.gov/pubs/sp/800/160/v2/r1/final
- Google SRE: https://sre.google/
- AWS Well-Architected: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- Google Cloud Well-Architected: https://docs.cloud.google.com/docs/get-started/well-architected-framework
- Azure Well-Architected: https://learn.microsoft.com/azure/well-architected/
- C4: https://c4model.com/
- MADR: https://adr.github.io/madr/
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
- NIST Generative AI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- OWASP Agentic Top 10: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- MCP: https://modelcontextprotocol.io/
- Agent Skills: https://agentskills.io/specification
- Agent Skills evaluation: https://agentskills.io/skill-creation/evaluating-skills

## Why visual modeling is first-class

System maps are used because complex relationships, feedback loops, boundaries and end-to-end service dependencies are difficult to hold in prose alone. The UK systems-thinking toolkit explicitly uses causal-loop diagrams to reveal dynamics and leverage points, while service-blueprint guidance maps current, target and future service states across the user experience and the enabling teams, systems, processes, legislation and data.

System Design Architect therefore treats visual models as reasoning artifacts, not presentation decoration.
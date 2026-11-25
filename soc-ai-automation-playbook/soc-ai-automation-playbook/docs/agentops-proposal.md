# AI Agent Governance and Productivity Framework (AgentOps proposal)

An enterprise-oriented Agent Operations Center combining Claude agents, productivity automation, NIST-based governance, security enforcement, reproducible testing and measurable ROI. The code is in `../agentops/` (v0.2). It must not present simulated productivity as actual savings, or claim NIST compliance because it references NIST.

## Scope

| Component | Purpose | Status in v0.2 |
| --- | --- | --- |
| Agent Operations Center | Dashboard for monitoring agent tasks | Implemented (local) |
| Claude agents | Research, documentation, code review, governance, reporting | One Messages API call per task; no tools |
| Governance engine | Permissions and approved workflows | Roles, separation of duties, approval states |
| NIST integration | Machine-readable standards and evaluation | Planned: CAPORDINO, OSCAL, Dioptra, evaluation probes |
| Evaluation engine | Accuracy, reliability, policy adherence | Planned (see `embedding-poc-roi.md`, `nist-github-survey.md`) |
| ROI engine | Measured time recovered and operating cost | Implemented: reviewer-entered minutes plus estimated API cost |
| Audit engine | Actions, approvals, evaluation results | Implemented: actor on every event, hash chain, verify endpoint |
| Documentation | Zensical site | Config and content included |
| Tests | Function, security, governance | 21 automated tests |

## About the dashboard mock-ups

The original proposal showed an ROI simulator (2,500 hours, $212,500 gross, $200,500 net, 1,671% ROI) and an Operations Center (1,284 tasks, 214 hours saved, 98.2% governance tests passed). Both are illustrations: the simulator multiplies assumed inputs (10 employees x 60 minutes x 250 days x $85, $12,000 cost) and the Operations Center figures are labeled synthetic. The app computes neither. The multi-agent flow image (manager, research, analysis and writing agents with faithfulness, completeness and sufficiency probes) describes the NIST [agentic-research-evaluation-probes](https://github.com/usnistgov/agentic-research-evaluation-probes) pipeline, not AgentOps.

## Roadmap (six weeks)

| Week | Deliverable | Acceptance |
| --- | --- | --- |
| 1 | Local prototype | Tests pass; approval flow works with three separate users |
| 2 | Claude API pilot | Synthetic tasks reviewed; cost recorded from real usage |
| 2 | Productivity baseline | 30 paired tasks with a reviewer rubric |
| 3 | CAPORDINO and OSCAL | Catalog output validated with oscal-cli |
| 4 | Claude Agent SDK | Read-only tools, deny-by-default hooks, independent tests |
| 5 | Dioptra and probes | Reproducible evaluation on a held-out dataset; probes validated against human labels |
| 6 | Enterprise hardening | Entra SSO, RBAC, DLP, external audit store, secrets manager, budgets, rollback |

Before production: threat model, privacy review, dependency scan and SBOM, penetration test, accessibility review, incident runbook, change ticket, stakeholder sign-off. The fit recommendation is to fold the approval, audit and ROI engine into Dash rather than ship a separate tool.

## Official references

[NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) · [AI 100-1](https://doi.org/10.6028/NIST.AI.100-1) · [CAPORDINO](https://github.com/usnistgov/capordino) · [OSCAL docs](https://pages.nist.gov/OSCAL/) · [OSCAL schema reference](https://pages.nist.gov/OSCAL/reference/) · [oscal-content](https://github.com/usnistgov/oscal-content) · [Dioptra docs](https://pages.nist.gov/dioptra/) · [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) · [Claude API](https://platform.claude.com/docs/en/api/overview) · [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python) · [Apache ECharts](https://echarts.apache.org/) · [Zensical](https://zensical.org/docs/) · [pytest](https://docs.pytest.org/)

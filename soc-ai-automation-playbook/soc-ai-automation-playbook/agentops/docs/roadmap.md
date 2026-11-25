# Roadmap and release gates
| Phase | Deliverable | Acceptance | Owner |
|---|---|---|---|
| Day 1 | Local setup and demo | Tests pass, approval flow works | Engineer |
| Day 2 | Approved Claude pilot | Synthetic task reviewed, cost recorded | Engineer / AI platform owner |
| Days 3-4 | Baseline study | 30 paired tasks, reviewer rubric | SOC lead |
| Week 2 | Catalog integration | CAPORDINO output validated against OSCAL schema | Governance owner |
| Week 3 | Agent SDK migration | Read-only tools, deny-by-default hooks, independent tests | Security engineer |
| Week 4 | Dioptra and probes | Reproducible evaluation with held-out dataset | QA |
| Weeks 5-6 | Enterprise hardening | SSO, RBAC, DLP, protected audit, secrets, budget and rollback | IAM / security / platform |

Before production: threat model, privacy review, dependency scan and SBOM, penetration test, accessibility review, incident runbook, approved change ticket and stakeholder sign-off. Start with documentation and research; no containment or production changes. React/ECharts dashboard and MCP integrations are future work, not dependencies of the local pilot.

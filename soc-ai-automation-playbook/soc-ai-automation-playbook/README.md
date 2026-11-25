# SOC AI and Automation Playbook

Projects, code and evidence for AI automation in a security operations center: cost savings, compliance automation, AI agent security and measurable ROI. Every item links to official sources, has build steps, tests and metrics, and maps to proposed controls that a control owner must confirm.

> Nothing here claims NIST compliance because it references NIST. Use synthetic data only until a security review approves real data. Simulated figures are labeled as simulated.

## Contents

| Path | What it is |
| --- | --- |
| [docs/playbook.md](docs/playbook.md) | The playbook: about 30 items (Sentinel cost, OSCAL/SCAP, Automata, Mythos red teaming, Dash grounding, SOC operations, SDLC) with sources, steps, tests, ROI metrics and controls |
| [docs/nist-github-survey.md](docs/nist-github-survey.md) | Which of the roughly 1,459 NIST GitHub repositories help SOC AI work, and how they fit VCC (Dash) |
| [docs/oscal-hub-plan.md](docs/oscal-hub-plan.md) | How to make several tools follow OSCAL through a git hub and adapters |
| [docs/embedding-poc-roi.md](docs/embedding-poc-roi.md) | Measuring an embedding retrieval POC: metrics, formulas, benchmark design, acceptance criteria |
| [docs/agentops-proposal.md](docs/agentops-proposal.md) | AI Agent Governance and Productivity Framework proposal and roadmap |
| [docs/vcc-dash-architecture.md](docs/vcc-dash-architecture.md) | VCC (Dash) architecture map and where playbook items plug in |
| [docs/mitre-universe-nist-sources-brief.md](docs/mitre-universe-nist-sources-brief.md) | Research brief for adding NIST sources to MITRE Universe |
| [docs/security-scan-report.md](docs/security-scan-report.md) | Scan results and the AgentOps v0.1 to v0.2 fixes |
| [docs/source-documents.md](docs/source-documents.md) | Every supplied document, its copyright status and hash |
| [agentops/](agentops/) | Agent Operations Center v0.2: approval, separation of duties, hash-chained audit, ROI (Python, standard library, 21 tests) |
| [tools/embedding-roi/](tools/embedding-roi/) | `metrics.py`: cost, ROI, retrieval metrics, trec_eval export, peak-memory measurement, evidence records (9 tests) |
| [tools/kql/](tools/kql/) | Sentinel queries: billable volume by table, agent new-destination alert, agent token spike |
| [oscal-hub/](oscal-hub/) | Folder skeleton for the OSCAL hub |
| [sources/nist/](sources/nist/) | Public-domain NIST PDFs: SP 1353 ipd, IR 8621, SP 1038 |

## Quick start

```bash
# AgentOps
cd agentops
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py new-user alice submitter
python app.py new-user bob approver,reviewer
python app.py            # http://127.0.0.1:8765

# Tests for everything
pip install psutil
pytest agentops/tests tools/embedding-roi
```

## Before pushing to GitHub

1. Decide on a license. NIST-sourced PDFs are public domain in the US; your own code and docs need a license of your choosing (none is set here).
2. If any content describes your employer's internal systems, use a private repository or remove those details first.
3. Enable Dependabot alerts, secret scanning and push protection in the repository settings.
4. Pin the GitHub Actions in `.github/workflows/ci.yml` to commit SHAs if your org requires it.

# Source documents

Every file supplied for this project, what it is, and whether it is in this repository. Public-domain US government works are included. Copyrighted works are listed but not committed: a public GitHub repository would redistribute them.

## Included (public domain, `../sources/nist/`)

| File | What it is | Key points used here | SHA-256 |
| --- | --- | --- | --- |
| [NIST.SP.1353.ipd.pdf](https://doi.org/10.6028/NIST.SP.1353.ipd) | CSF 2.0 Quick-Start Guide for using AI for CSF analysis and reporting, initial public draft, Aug 2026 | Three notional use cases: review policies against CSF governance, draft a Current State Profile, draft a Target State Profile. Prompts follow the CO-STAR framework. Warns to check access privileges and confidentiality terms before putting sensitive information into an AI tool. Used in playbook item P4 | 5a37e092598ad56eab83b015efd499f55a6f4a755de0a97494fc6a9fd8ff0759 |
| [NIST.IR.8621.pdf](https://doi.org/10.6028/NIST.IR.8621) | NIST Workshop on SI Incident Management (400+ experts) | Two incident domains: attacks on AI systems, and harm from AI misuse, anomalous behavior or malfunction. Traditional deterministic IR life cycles fall short for probabilistic, autonomous systems. Needs: reasoning-layer telemetry, non-human identity governance, authorization-scoped containment, evidentiary and reporting schemas, shared responsibility across the AI value chain. Used in S8, A1, A4 | e68f116e80916af661cb181c187be1b098250ac83b8bf93c192bacc2fe508303 |
| NIST.SP.1038.pdf | The International System of Units (SI): Conversion Factors for General Use, May 2006 (Weights and Measures Division) | Not a security publication; "SI" here means the metric system, not super intelligence. Kept for completeness only | 3457e3bee90a5ca91b5fa37ab2925050f4710c1fb4f89d886c38f694af8b1366 |

## Referenced, not included (copyright held by others)

| Document | Owner and status | Relevance | SHA-256 of supplied copy |
| --- | --- | --- | --- |
| STIX introduction handout | MITRE; no reuse license in the file | STIX and TAXII for sharing threat intel; relevant to S4 and MITRE Universe | 257bd0b076486eada1286bde5bb04ac36a2c76c06416af46b2c2f87ec9822e9a |
| MITRE Insider Threat Research and Solutions two-pager (case 26-1701) | MITRE, All Rights Reserved; approved for public release. Source: [insiderthreat.mitre.org](https://insiderthreat.mitre.org) | Behavioral, data and cyber science approach to insider risk, malicious and non-malicious | 1c983c1b18747fe51cecb07db154295d6e6f9adc01846442b43e5b745960b631 |
| PIVOT (Platform Independent Vectors of Techniques) overview (case 25-02548-2) | MITRE Labs, All Rights Reserved; approved for public release | Connects ATT&CK Enterprise, Mobile, ICS and the Embedded System Threat Matrix to find pivot points in systems of systems. A strong candidate layer for MITRE Universe | 6dc7b12987b28b1777df37bbc084868ff0a27c941e665181ec0b8bb5a7819a74 |
| *Agentic AI for Cybersecurity* (Omar Santos) | Commercial book | Reference reading | not recorded |
| *AI Security Engineering: Securing Agentic Systems in Production* (Dan Borges, David Campbell) | Commercial book | Reference reading for A1 to A4 | not recorded |
| *AI for Everyday Automation* (Dipankar Sarkar) | Commercial book | Reference reading | not recorded |
| *Mathematics in Cybersecurity* (A. Basta, 2026) | Commercial book | Reference reading | not recorded |

The four books were supplied as copies from an unofficial download site. They are not committed, and they should not be stored in any repository. Cite them by title and edition, and use licensed copies (publisher, O'Reilly, library).

## Supplied text, now in `docs/`

| Supplied material | Location |
| --- | --- |
| AgentOps v0.1 project (agentops.zip, SHA-256 a297c2f2360401666f356098f192b4354080839e5b8ad33dde0bf5a23c875d86) | `../agentops/`, hardened to v0.2 |
| AgentOps proposal and dashboard mock-ups | `agentops-proposal.md` |
| Embedding POC ROI write-up (including the truncated `metrics.py` snippet) | `embedding-poc-roi.md`, completed code in `../tools/embedding-roi/` |
| NIST GitHub survey, VCC fit and OSCAL questions (from a VCC session) | `nist-github-survey.md`, `oscal-hub-plan.md` |
| VCC (Dash) architecture map | `vcc-dash-architecture.md` |
| MITRE Universe sources brief | `mitre-universe-nist-sources-brief.md` |
| CSRC news list (Aug 2025 to Nov 2026) | Used for `playbook.md` watch list and governance baseline |

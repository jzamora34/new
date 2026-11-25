# SOC AI and Automation Playbook

Nov 25, 2026 · @Josh

Every Dash (VCC), Automata and CVS SOC idea from our sessions, each with official sources, build steps, tests, ROI metrics and the governance control it satisfies.

## Bottom line

Lead with Sentinel cost reduction: it is the only item with hard dollar savings and it is mostly configuration. Follow with continuous AI red teaming, which NIST's June 2026 proof gives a peer-reviewed justification for.

| Rank | Project | ROI type | Effort | First proof point |
| --- | --- | --- | --- | --- |
| 1 | Sentinel ingestion and retention reduction | Hard dollars | Low | Top 10 tables by billed GB from the `Usage` table |
| 2 | Continuous AI red teaming (Mythos attacks, Automata detects) | Risk reduction, audit evidence | Medium | Jailbreaks found internally before production, per month |
| 3 | OSCAL + CPRT + SCAP compliance automation | Labor hours | Medium | Hours per audit evidence request, before and after |
| 4 | NSRL known-file filtering in IR and hunting | Analyst hours | Low | Percent of files eliminated per case |
| 5 | Vulnerability triage and owner routing (NVD, KEV, EPSS) | Time to remediate | Low to medium | Median days to fix KEV-listed CVEs |
| 6 | Dash answer grounding (NIST evaluation probes + trec\_eval) | Quality, trust | Medium | Unsupported-claim rate in Dash answers |

Rules for every item below: nothing claims NIST compliance by referencing NIST. A control owner signs off on each mapping. Synthetic data only until security review approves real data. Every metric gets a baseline before the build.

## ROI method

ROI is annual benefit minus annual cost, divided by annual cost. Benefit is counted in three separate buckets, reported in this order because finance trusts them in this order.

```latex
\text{ROI} = \frac{B_{\text{hard}} + B_{\text{labor}} + B_{\text{risk}} - C}{C}
```

| Bucket | How to compute | Where the number comes from |
| --- | --- | --- |
| Hard savings | Spend that stops (ingestion GB x price, licenses, vendor fees) | Azure Cost Management, invoices |
| Labor savings | Hours saved x fully loaded hourly rate | Time study baseline; loaded rate from finance (typically 1.3 to 1.4 x base pay) |
| Risk reduction | Annualized loss expectancy before minus after (single loss x yearly frequency) | Risk register framed per [NIST IR 8286r1](https://csrc.nist.gov/pubs/ir/8286/r1/final) |
| Cost | Build hours + run cost (compute, tokens, licenses) + upkeep hours | Timesheets, [Claude Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api), Azure billing |

Measurement protocol, the same for every project:

1. Record a baseline for 2 to 4 weeks before building anything.
2. Pick 2 or 3 metrics per project, defined in writing before the pilot.
3. Re-measure at 30, 60 and 90 days with the same method and the same person or query.
4. Count failed runs and rework time against the project, not only successes.
5. Report a conservative and an expected value; lead with the conservative one.
6. Keep the raw data, query text and dates as audit evidence.

Recovered hours are capacity, not cash, unless headcount, contractor spend or overtime actually drops. Say so in every pitch. The AgentOps simulator's 1,671% figure (10 people x 60 minutes a day) is an input assumption, not a measurement; see the AgentOps review below.

## Governance and audit baseline

Every project below maps to these sources; finals carry authority, drafts are labeled and re-checked when they finalize.

| Source | Status | Use it for |
| --- | --- | --- |
| [NIST AI RMF 1.0 (AI 100-1)](https://www.nist.gov/itl/ai-risk-management-framework) | Final | Govern, Map, Measure, Manage structure for every AI item |
| [NIST AI 600-1, Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1) | Final | GenAI-specific risks and actions for Dash, agents, Mythos |
| [NIST CSF 2.0](https://www.nist.gov/cyberframework) | Final | Governance language for leadership reporting |
| [Cybersecurity and Privacy Reference Tool (CPRT)](https://csrc.nist.gov/projects/cprt) | Live | Machine-readable CSF 2.0, SP 800-53, SSDF, AI RMF |
| [OLIR crosswalks](https://csrc.nist.gov/projects/olir) | Live | Official framework-to-framework mappings |
| [SP 800-61r3, Incident Response](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | Final | IR playbooks and SOAR automations |
| [IR 8286r1, Cybersecurity and ERM](https://csrc.nist.gov/pubs/ir/8286/r1/final) | Final | Risk register format for ROI pitches |
| [SSDF project (SP 800-218, 218A, 218r1)](https://csrc.nist.gov/projects/ssdf) | 1.1 final; [1.2 draft](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd) | Pipeline and intake gates; 218A covers GenAI |
| [IR 8596, Cyber AI Profile](https://csrc.nist.gov/pubs/ir/8596/iprd) | Draft | AI-specific CSF outcomes for the intake redesign |
| [SP 800-53 control overlays for AI (COSAiS)](https://csrc.nist.gov/projects/cosais) | In development | Ready-made AI controls instead of writing your own |
| [SP 2400-102e2026, Adversarial ML Taxonomy](https://csrc.nist.gov/pubs/sp/2400/102/e2026/ipd) | Draft, comments to Dec 18, 2026 | Shared attack vocabulary, agentic attack index |
| [NIST Godel proof on AI guardrails](https://www.nist.gov/news-events/news/2026/06/nist-mathematical-proof-supports-transition-continuous-monitor-and-update) ([paper DOI](https://doi.org/10.1109/MSEC.2026.3678214)) | Peer reviewed, May 2026 | Justifies continuous red teaming and monitoring budget |
| [SP 1353, AI for CSF analysis and reporting](https://csrc.nist.gov/News/2026/using-ai-for-csf-2-analysis-reporting-draft-qsg) | Draft | How to make AI-generated CSF reports defensible |
| [SP 800-92r1, Log Management Planning](https://csrc.nist.gov/pubs/sp/800/92/r1/ipd) | Draft since 2023 | What logs to keep; neutral backing for Sentinel tiering |

Evidence pack every project must produce before go-live:

- [ ] Control mapping table (control ID, how satisfied, evidence location, owner sign-off)
- [ ] Data classification decision and approver
- [ ] Model name and version, prompt and config hashes, for every AI component
- [ ] Test plan, test results and the date they ran
- [ ] Baseline and post-change metric exports with query text
- [ ] Change ticket (Jira) and approval record
- [ ] Audit log location and retention period
- [ ] Rollback procedure, tested once

## Cost-savings projects

These six items cut spend directly; Sentinel tiering is the fastest, pipelines and compression pay off only at large volume.

### C1. Sentinel ingestion and tiering

Goal: pay analytics-tier prices only for data that detections actually use.

Sources: [Plan costs and billing](https://learn.microsoft.com/en-us/azure/sentinel/billing) · [Reduce costs](https://learn.microsoft.com/en-us/azure/sentinel/billing-reduce-costs) · [Manage and monitor costs](https://learn.microsoft.com/en-us/azure/sentinel/billing-monitor-costs) · [Ingestion-time transformations](https://learn.microsoft.com/en-us/azure/sentinel/data-transformation) · [Filter and split](https://learn.microsoft.com/en-us/azure/sentinel/transformation-filter-split) · [Sentinel data lake](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-overview) · [KQL jobs](https://learn.microsoft.com/en-us/azure/sentinel/datalake/kql-jobs) · [Summary rules](https://learn.microsoft.com/en-us/azure/sentinel/summary-rules) · [SP 800-92r1 draft](https://csrc.nist.gov/pubs/sp/800/92/r1/ipd)

Steps:

1. Baseline billed volume per table for 30 days (query below); export to CSV with the run date.
2. For each top table, list every analytics rule, hunting query and workbook that reads it (export rules from the Sentinel API or your rules repo and search for the table name).
3. Label each table: detection-critical (stays analytics), investigation-only (data lake), compliance-only (long-term retention).
4. Write the required retention per table from policy and legal, with the policy citation.
5. Apply data collection rule transformations to drop unused columns and noise rows; move investigation-only tables to the data lake.
6. Use summary rules or KQL jobs to push small aggregates from the lake back into analytics where a detection needs them.
7. Change one table at a time through a change ticket, with rollback noted.

```kusto
Usage
| where TimeGenerated > ago(30d) and IsBillable == true
| summarize BilledGB = sum(Quantity) / 1000.0 by DataType
| top 20 by BilledGB desc
```

Tests: run every retained analytics rule over the same 7-day window before and after and compare alert counts (target: zero rules broken); replay the Purple Team top techniques and confirm detection; confirm an investigation query against the lake returns within agreed time.

Metrics: billed GB per day, dollars per month, rules broken (must be 0), mean time to detect unchanged.

Controls: SP 800-53 AU-4, AU-6, AU-11; CSF DE.CM. Check the billing page for current tier names before pitching; Microsoft is steering long-term data toward the data lake.

### C2. Duplicate logs and over-retention

Goal: stop paying to store the same events in several tools, or for longer than required.

Sources: [Reduce costs](https://learn.microsoft.com/en-us/azure/sentinel/billing-reduce-costs) · [SP 800-92r1 draft](https://csrc.nist.gov/pubs/sp/800/92/r1/ipd)

Steps: inventory each log source and every destination it flows to (Sentinel, CrowdStrike, storage archive); mark the system of record for each; remove secondary copies that no detection or legal hold needs; set retention to the documented requirement, not the default.

Test: for each removed copy, confirm no rule, report or legal hold references it; restore test from the system of record.

Metrics: GB stored per source across all tools; storage dollars per month.

Controls: AU-11, SI-12.

### C3. Unused cloud resources (Resource Discovery)

Goal: find provisioned-but-idle resources, which cost money and are often unmonitored.

Steps: query Azure resources with no activity or metrics for 30+ days; cross-check against Sentinel and Defender coverage; route each to its owner tag for keep or delete.

Test: sample 20 flagged resources manually; target 90% precision before automating.

Metrics: monthly cost of flagged resources; resources with no SOC coverage, before and after.

Controls: CM-8 (inventory), RA-5, SI-4.

### C4. Security license cleanup

Goal: reclaim unused seats and overlapping tools.

Sources: [Entra ID Governance](https://learn.microsoft.com/en-us/entra/id-governance/identity-governance-overview) · [Entra licensing](https://learn.microsoft.com/en-us/entra/fundamentals/licensing)

Steps: join license assignments with sign-in activity; flag seats unused for 90 days and tools whose function duplicates Defender or CrowdStrike; hand the list to procurement.

Metrics: seats reclaimed, annual license dollars avoided.

### C5. Log template compression (experimental)

Goal: collapse repetitive events into templates with counts before ingestion; keep raw data in cheap storage.

Sources: [Drain3 log template miner](https://github.com/logpai/Drain3)

Steps: run Drain3 on a 24-hour sample; keep one example per template plus count and unusual fields; send only templates that are not seen often, plus aggregates, to analytics. Use embeddings only on events that fit no template.

Tests: plant known-bad canary events in the sample and confirm every one survives compression; compare detection results on raw versus compressed data.

Metrics: compression ratio; canary recall (must be 100%).

### C6. Security data pipeline and OCSF

Goal: filter, reshape and route logs before any tool bills for them, in a vendor-neutral format.

Sources: [OCSF](https://ocsf.io/) · [OCSF schema browser](https://schema.ocsf.io/classes)

Steps: pick 2 high-volume sources; normalize to OCSF classes; route full data to the lake and filtered data to Sentinel. Commercial pipelines (Cribl) or open-source tools both fit; compare their cost against C1's savings first.

Metrics: ingestion dollars, time to onboard a new source.

## Compliance automation

OSCAL turns audit evidence from screenshots into machine-readable files; SCAP checks the settings, OSCAL reports the controls.

### P1. OSCAL evidence automation

Goal: generate audit evidence packages automatically from Sentinel, CrowdStrike and Entra state.

Sources: [OSCAL models](https://github.com/usnistgov/OSCAL) · [OSCAL content (800-53 rev 5 catalog and baselines)](https://github.com/usnistgov/oscal-content) · [oscal-cli](https://github.com/usnistgov/oscal-cli) · [liboscal-java](https://github.com/usnistgov/liboscal-java) · [CAPORDINO](https://github.com/usnistgov/capordino) · [CPRT](https://csrc.nist.gov/projects/cprt) · [OLIR](https://csrc.nist.gov/projects/olir) · [CTID ATT&CK to 800-53 mappings](https://center-for-threat-informed-defense.github.io/mappings-explorer/external/nist/) ([project page](https://ctid.mitre.org/projects/nist-800-53-control-mappings/))

CAPORDINO (verified README) converts CPRT datasets into OSCAL catalogs for CSF 2.0, SP 800-171r3, SSDF 1.1, SP 800-66r2, SP 800-172/172A and AI RMF 1.0. It needs Java and Maven 3.9 or later. It generates catalogs; it does not enforce controls.

Steps:

1. Pull the SP 800-53 rev 5 catalog from oscal-content and pin the commit hash.
2. Generate CSF 2.0 and AI RMF catalogs with CAPORDINO.
3. Map each Sentinel analytics rule to its ATT&CK technique, then to 800-53 controls with the CTID mappings.
4. Write an OSCAL component definition per tool (Sentinel, CrowdStrike, Entra) listing the controls it implements.
5. Emit OSCAL assessment results from automated checks (rule enabled, last fired, config state) with UUIDs and timestamps.
6. Validate every file with oscal-cli before publishing.
7. Store outputs in git with signed commits so the history is the audit trail.

Tests: oscal-cli validation passes on every file; an auditor or GRC partner reviews 10 sampled controls against the generated evidence; diff against the last manual evidence package.

Metrics: hours per audit cycle; percent of evidence requests filled automatically; audit findings per cycle.

Controls: CA-2, CA-7, PM-31 (continuous monitoring strategy).

### P2. SCAP configuration compliance

Goal: replace manual hardening checks with scheduled, machine-readable scans.

Sources: [SCAP project (SCAP 1.4)](https://csrc.nist.gov/projects/security-content-automation-protocol) · [National Checklist Program publications (SP 800-70r5)](https://csrc.nist.gov/Projects/national-checklist-program/publications)

Steps: confirm which licensed scanner is SCAP-validated; load NCP checklists for the OS baselines in scope; schedule scans; export results in the Asset Reporting Format; map checklist rules to 800-53 so results feed P1.

Tests: scan a known-noncompliant test host and confirm every planted misconfiguration is flagged.

Metrics: hours per scan cycle; drift findings per month; mean time to fix drift.

Controls: CM-6, CM-7, CA-7.

### P3. macOS baselines (only if there is a meaningful Mac fleet)

Sources: [macOS Security Compliance Project](https://github.com/usnistgov/macos_security) · [SP 800-219r2 draft](https://csrc.nist.gov/News/2026/draft-sp-800-219r2-available-for-public-comment)

Steps: generate the baseline matching your policy; deploy profiles through MDM; collect compliance results. Metric: hours per baseline build; percent of Macs compliant.

### P4. AI-generated CSF reporting

Sources: [SP 1353 draft, AI for CSF analysis and reporting](https://csrc.nist.gov/News/2026/using-ai-for-csf-2-analysis-reporting-draft-qsg)

Use it as the checklist when Dash or any agent drafts CSF status reports: human review, source traceability, version of the model used. Metric: hours per CSF report; corrections per report.

## AI agent security

NIST's June 2026 proof shows no fixed guardrail set stops every adversarial prompt, so the defensible design is a loop: attack continuously, monitor deterministically, patch, repeat. A1 to A3 form that loop; A4 to A8 support it.

### A1. Automata, the deterministic agent monitor

Goal: compare what each agent should do with what it did, using rules, not another AI.

Sources: [NIST Godel proof](https://www.nist.gov/news-events/news/2026/06/nist-mathematical-proof-supports-transition-continuous-monitor-and-update) · [NIST AI 800-4, Challenges to monitoring deployed AI systems](https://www.nist.gov/publications/challenges-monitoring-deployed-ai-systems-center-ai-standards-and-innovation) · [SP 2400-102e2026 draft](https://csrc.nist.gov/pubs/sp/2400/102/e2026/ipd)

Steps:

1. Write a policy file per agent: allowed tools, allowed data sources, allowed destinations, maximum actions per hour, actions that need human approval.
2. Collect actual behavior from tool-call logs, the API gateway (A4) and network logs (A2) into Sentinel.
3. Express each policy line as a KQL rule or a deterministic check; any mismatch raises an alert.
4. Feed alerts to Dash as an "agent behavior" panel.

Tests: replay the attack corpus from A3 in a sandbox; every successful hijack must raise an alert. Run 1,000 normal tasks to measure false positives.

Metrics: hijack detection rate (target 100% of the replayed corpus); false positives per 1,000 runs; mean time to detect.

Controls: SI-4, AU-6, AC-6; AI RMF Measure and Manage functions.

### A2. Agent network baseline (saved idea)

Goal: catch a hijacked agent sending data somewhere new.

Steps: record each agent's normal destinations for 14 days; alert when an agent reaches a domain or IP outside its baseline; require an approved change to add a destination.

Test: from a sandboxed agent, call an unlisted test domain; the alert must fire within the agreed window.

Metrics: new-destination alerts per week; true-positive share after triage.

Controls: SC-7, SI-4.

### A3. Continuous AI red teaming with Mythos

Goal: find the prompts that break your agents before attackers do, as NIST's proof recommends: continuous red teaming, continuous guardrail updates, and resilience that limits impact.

Sources: [Anthropic Cyber Verification Program](https://support.claude.com/en/articles/14604842-cyber-verification-program) · [Claude Mythos 5.2 docs](https://platform.claude.com/docs/en/models/mythos-5-2/overview) · [Claude Mythos](https://www.anthropic.com/claude/mythos) · [SP 2400-102e2026 draft](https://csrc.nist.gov/pubs/sp/2400/102/e2026/ipd)

Steps:

1. Request Mythos access under CVS's contract through the Cyber Verification Program.
2. Stand up a sandbox copy of each agent (Dash, intake agents) with synthetic data only.
3. Have Mythos generate direct and indirect prompt injection, tool misuse and memory-poisoning attempts, labeled with the SP 2400-102 attack categories.
4. Run each attack; record success, and whether Automata (A1) caught it.
5. Fix the guardrail or permission; add the attack to a regression suite that runs on every agent change.

Tests: the regression suite passes before any agent release.

Metrics: attack success rate per month (should fall); share of successful attacks Automata caught; time from discovery to fix.

Controls: CA-8 (penetration testing), RA-5, SI-4; AI 600-1 information security risks.

### A4. Agent identity and the Claude gateway

Goal: every AI call is attributable to one registered agent; company-wide, not only your own agents.

Sources: [Claude Workspaces](https://platform.claude.com/docs/en/manage-claude/workspaces) · [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api) · [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api) · [Entra Agent ID](https://learn.microsoft.com/en-us/entra/agent-id/what-is-microsoft-entra-agent-id) · [Agent identities](https://learn.microsoft.com/en-us/entra/agent-id/what-are-agent-identities) · [Governing agent identities](https://learn.microsoft.com/en-us/entra/id-governance/agent-id-governance-overview) · [APIM AI gateway](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities) · [llm-token-limit policy](https://learn.microsoft.com/en-us/azure/api-management/llm-token-limit-policy) · [IR 8587, protecting tokens](https://csrc.nist.gov/pubs/ir/8587/final)

Steps:

1. One workspace and one API key per agent; register each agent in Entra Agent ID where supported.
2. Route all Claude traffic through an API Management gateway that tags requests with the agent name and enforces token limits.
3. Block direct egress to the Anthropic API at the proxy so the gateway is the only path.
4. Send gateway logs to Sentinel; alert on token spikes and off-hours use.
5. Run secret scanning on repos to find stray keys; network logs catch anyone still calling the API directly.

Tests: a direct call from a test host is blocked; a gateway call shows up in Sentinel with the agent tag within minutes.

Metrics: percent of AI calls attributable to a registered agent (target 100%); stray keys found and revoked; cost per agent per month.

Controls: IA-2, IA-9, AC-6, AU-2, AU-12.

### A5. Dash answer grounding

Goal: prove Dash's answers to Van are supported by Jira, SharePoint and Teams data.

Sources: [NIST agentic research evaluation probes](https://github.com/usnistgov/agentic-research-evaluation-probes) · [NIST probes project page](https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai) · [trec\_eval](https://github.com/usnistgov/trec_eval)

The NIST repository (verified README) runs three LM-judge probes on every citation: faithfulness (source supports the claim), completeness (no cherry-picking) and sufficiency (enough evidence for the claim). It is built on the OpenAI Agents SDK and works with any OpenAI-compatible endpoint; confirm Claude endpoint compatibility in Anthropic's docs before relying on it. NIST notes the probes still need validation.

Steps:

1. Build a gold set of 50 Dash questions with known correct answers and source documents.
2. Score Dash's retrieval with trec\_eval (precision, recall, nDCG) and record the baseline.
3. Port the three probe rubrics to Dash's answer pipeline; store probe scores with each answer.
4. Flag or withhold answers that score below threshold; show the citation to Van.
5. Validate the probes against 50 human-labeled answers before trusting their scores.

Metrics: unsupported-claim rate; retrieval nDCG; human agreement with probe scores.

Controls: AI RMF Measure function; AI 600-1 confabulation risk; AU-10.

### A6. Mythos secure code review gate

Goal: every pull request is checked by an agent that proves findings with a working test, not a guess.

Sources: [Mythos 5.2 docs](https://platform.claude.com/docs/en/models/mythos-5-2/overview) · [Anthropic research on vulnerability discovery](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude) · [Juliet C/C++ 1.3](https://samate.nist.gov/SARD/test-suites/112) · [Juliet Java 1.3](https://samate.nist.gov/SARD/test-suites/111) · [Juliet C# 1.3](https://samate.nist.gov/SARD/test-suites/110) · [SSDF](https://csrc.nist.gov/projects/ssdf)

Steps:

1. Benchmark first: run the reviewer on a Juliet subset with known flaws; record detection and false-positive rates.
2. Trigger on each pull request; give the agent read access to the repo and a network-isolated sandbox.
3. Require a reproducing test for every finding; post severity, proof and fix on the PR.
4. Block merge on critical findings; log every review for audit.

Metrics: Juliet detection and false-positive rates; vulnerabilities caught before merge; cost per PR.

Controls: SA-11, RA-5; SSDF PW.7 and PW.8 (review and test code).

### A7. Multi-agent lessons loop

Goal: cut repeat findings and Mythos spend over time. Models do not learn from each other; the memory lives outside them.

Sources: [Semgrep](https://github.com/semgrep/semgrep)

Steps: a builder agent on a cheaper model writes code; Mythos attacks it; the builder fixes; each confirmed finding (flaw, bad pattern, fix) goes into a lessons store; the builder retrieves relevant lessons before writing; a flaw seen 3 or more times becomes a Semgrep rule that runs free.

Metrics: repeat-finding rate; Mythos calls per PR; Semgrep rules created.

### A8. Shadow AI discovery

Goal: find unsanctioned AI tools and sensitive data sent to them.

Sources: [Purview: discover AI apps](https://learn.microsoft.com/en-us/purview/deploymentmodels/depmod-data-leak-shadow-ai-step1) · [Discover AI apps and data](https://learn.microsoft.com/en-us/security/security-for-ai/discover) · [Global Secure Access shadow AI discovery](https://learn.microsoft.com/en-us/entra/global-secure-access/concept-shadow-ai-discovery) · [Purview DSPM](https://learn.microsoft.com/en-us/purview/data-security-posture-management-learn-about)

Steps: turn on AI app discovery; review the top apps by users and data volume; sanction, block or monitor each; add DLP policies for sensitive data going to unsanctioned apps.

Metrics: unsanctioned AI apps in use; sensitive-data events per month.

Controls: CM-7, SC-7, AC-4.

## SOC operations

These items save analyst hours; vulnerability routing and NSRL filtering are the quickest to prove.

### S1. Vulnerability triage and owner routing

Goal: rank by real exploitation, send each fix straight to the owner.

Sources: [NVD vulnerability API](https://nvd.nist.gov/developers/vulnerabilities) · [NVD start here (API keys)](https://nvd.nist.gov/developers/start-here) · [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [EPSS data](https://www.first.org/epss/data) · [EPSS overview](https://www.first.org/epss/)

Steps:

1. Pull open findings from the scanner already in use (Defender or CrowdStrike).
2. Enrich each CVE: KEV listed (yes/no), EPSS score, CVSS, asset criticality.
3. Resolve the owner from the asset's tag or CMDB record.
4. Create the ticket on the owner's queue with an SLA set by CVS policy (KEV first).
5. Re-check daily; close when the scanner confirms the fix.

Tests: 50 historical findings routed by the tool versus by hand; owner match rate target 95%.

Metrics: median days to fix KEV-listed CVEs; percent auto-routed; reassignments per ticket.

Controls: RA-5, SI-2; CSF ID.RA.

### S2. False-positive reduction in detections

Goal: fewer hours closing harmless alerts.

Steps: rank analytics rules by alerts closed as benign over 90 days; for the top 10, find the shared pattern (account, host, process); propose a KQL exclusion; Purple Team replays the rule's technique to prove it still fires.

Metrics: benign-closure rate per rule; analyst minutes per alert; detection still firing on replay (must be yes).

Controls: SI-4, IR-4.

### S3. Phishing report triage tuning

Goal: auto-close safe reported emails, escalate real threats.

Steps: measure the current split of reported emails (malicious, spam, safe); tune the existing Microsoft Defender automated investigation first; automate only what it misses; keep a human check on every auto-close for the first 30 days.

Metrics: analyst minutes per report; missed-malicious count (must be 0 in the sampled audit).

### S4. Threat intel to detections, mapped to MITRE

Goal: turn new threat reports into deployable Sentinel detections faster.

Sources: [ATT&CK STIX data](https://github.com/mitre-attack/attack-stix-data) · [Azure Sentinel content repo](https://github.com/Azure/Azure-Sentinel) · [CTID mappings](https://center-for-threat-informed-defense.github.io/mappings-explorer/external/nist/)

Steps: extract techniques from each report; check existing coverage in the rules repo; draft KQL for gaps (AI-assisted, human-reviewed); Purple Team validates; tag every rule with technique and 800-53 control (feeds P1).

Metrics: days from report to deployed detection; ATT&CK technique coverage percent.

### S5. NSRL known-file filtering

Goal: drop known software files from investigations so analysts look only at unknowns.

Sources: [National Software Reference Library](https://www.nist.gov/itl/csd/secure-systems-and-applications/national-software-reference-library-nsrl) · [Current RDS hash sets](https://www.nist.gov/itl/ssd/software-quality-group/national-software-reference-library-nsrl/nsrl-download/current-rds)

Steps: download the current RDS; load it into the forensic tool or a hash lookup service; hash files collected in an investigation; mark matches as known. Caution: NIST states the RDS includes some tools that may be considered malicious, so "known" is not "safe"; filter by product category, not by presence alone.

Tests: run on a past case; confirm no file tied to the incident was filtered out.

Metrics: percent of files eliminated per case; analyst hours per forensic case.

Controls: IR-4.

### S6. Stale accounts and non-human identities

Goal: remove access nobody uses, including service accounts and agents.

Sources: [Entra ID Governance](https://learn.microsoft.com/en-us/entra/id-governance/identity-governance-overview) · [Governing agent identities](https://learn.microsoft.com/en-us/entra/id-governance/agent-id-governance-overview)

Steps: report accounts and service principals unused for 90 days and admin rights never exercised; run access reviews with owners; disable, wait 30 days, delete.

Metrics: stale accounts removed; standing admin roles removed.

Controls: AC-2, AC-6.

### S7. Firewall rule cleanup (weaker ROI)

Goal: remove unused and overly open rules; cut manual review time.

Steps: compare each rule with 90 days of traffic logs; flag rules with zero hits or far broader scope than used; AI drafts a plain-English summary per rule for the reviewer.

Metrics: rules removed; engineer hours per periodic review (PCI DSS requires periodic ruleset reviews).

Controls: SC-7, CM-6.

### S8. AI incident response playbooks

Goal: a written playbook for attacks on AI, misuse and malfunction.

Sources: [SP 800-61r3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) · IR 8621, SI Incident Management workshop (listed on [CSRC news](https://csrc.nist.gov/news), Nov 2, 2026)

Steps: add AI-specific triggers (Automata alerts, A3 findings, Dash grounding failures) to IR playbooks; define kill switch per agent (revoke its key in A4); tabletop once per quarter.

Metrics: time to contain an agent incident in tabletop.

Controls: IR-4, IR-8.

## SDLC and ML assurance

These items make Green Team automations and in-house models defensible in review; scanner benchmarking also has a license-dollar angle.

### D1. SSDF gates on AI intake and pipelines

Sources: [SSDF project](https://csrc.nist.gov/projects/ssdf) · [SP 800-218 v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) · [SP 800-218r1 v1.2 draft](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd)

Steps: map each AI intake question to an SSDF practice; require pinned dependencies, an SBOM, secret scanning and the A6 review before approval; record the gate result on the intake item.

Metrics: percent of automations passing the gate first time; vulnerabilities found before versus after deployment.

### D2. Benchmark security scanners with SARD and Juliet

Goal: hard data on which scanners earn their license.

Sources: [SARD test suites](https://samate.nist.gov/SARD/test-suites) · [NIST IR 8561, the SARD](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8561.pdf)

Steps: pick the Juliet suite matching your main language; run each scanner (and the A6 reviewer); score detection and false positives per CWE.

Metrics: detection and false-positive rate per tool; license dollars per true finding.

### D3. Dioptra for in-house ML models

Goal: reproducible, NIST-aligned robustness evidence for classic ML models (fraud, anomaly classifiers).

Sources: [Dioptra repository](https://github.com/usnistgov/dioptra) · [Dioptra docs](https://pages.nist.gov/dioptra/)

Verified from the README: release 1.1.0; supports the AI RMF Measure function; runs as Docker containers with PyTorch and TensorFlow workers; access controls are listed as coming soon. It fits classic ML, not LLM agents; use A3 and A5 for those.

Steps: deploy per the install guide on an isolated host; run the Hello World tutorial; register one in-house model; run evasion and poisoning experiments; export results to the governance record.

Metrics: models assessed with reproducible evidence; robustness score before and after hardening.

Controls: AI RMF Measure function; SI-7.

### D4. Bugs Framework (watch, do not build on yet)

Sources: [Bugs Framework site](https://pages.nist.gov/BF/) · [SP 800-231](https://doi.org/10.6028/NIST.SP.800-231) · [BF repository](https://github.com/usnistgov/BF)

BF gives precise root-cause labels for weaknesses. Its Services Dashboard link is still a placeholder and login is marked coming soon; the worked CVE examples number about 20. Revisit when the dashboard goes live, as a labeling layer for A6 findings.

### D5. API and token hardening for Dash and the IAM enrollment API

Sources: [SP 800-228, API protection for cloud-native systems](https://csrc.nist.gov/pubs/sp/800/228/final) · [IR 8587, protecting tokens and assertions](https://csrc.nist.gov/pubs/ir/8587/final) · [IR 8611, m-NGAC (Aug 2026)](https://csrc.nist.gov/publications/ir)

Steps: inventory every API Dash and the enrollment API expose or call; apply SP 800-228 controls (authentication, authorization per call, rate limits, logging); apply IR 8587 token lifetime and binding guidance to Entra tokens; use attribute-based rules for agent least privilege.

Metrics: API findings per review; tokens with lifetime above policy.

Controls: AC-3, IA-5, SC-23.

## NIST GitHub repositories

Of the roughly 1,459 repositories in the [usnistgov organization](https://github.com/orgs/usnistgov/repositories), about a dozen matter for SOC AI and automation work. Pages 1 to 5 of that listing are sorted by most recent push, so they are mostly lab science (flow cytometry, thermodynamics, microcalorimetry) with no SOC use. All repositories below were confirmed to exist on Nov 25, 2026.

| Repository | What it is | Benefit to you | Used in |
| --- | --- | --- | --- |
| [OSCAL](https://github.com/usnistgov/OSCAL) + [oscal-content](https://github.com/usnistgov/oscal-content) | Machine-readable control formats; 800-53 rev 5 catalog and baselines | Automated audit evidence; highest labor ROI | P1 |
| [oscal-cli](https://github.com/usnistgov/oscal-cli) / [liboscal-java](https://github.com/usnistgov/liboscal-java) | Validate and convert OSCAL | Proves generated evidence is well-formed | P1 |
| [capordino](https://github.com/usnistgov/capordino) | Converts CPRT datasets (CSF 2.0, SSDF, AI RMF, others) to OSCAL | AI RMF and CSF as machine-readable catalogs for governance | P1, AgentOps |
| [agentic-research-evaluation-probes](https://github.com/usnistgov/agentic-research-evaluation-probes) | Deep-research agent plus faithfulness, completeness and sufficiency probes | Grounding checks and audit trail for Dash answers | A5 |
| [trec\_eval](https://github.com/usnistgov/trec_eval) | Standard retrieval scoring | Measures Dash search quality; justifies a cheaper embedding model | A5 |
| [dioptra](https://github.com/usnistgov/dioptra) | ML test platform, release 1.1.0 | Robustness evidence for classic in-house ML models | D3 |
| [macos\_security](https://github.com/usnistgov/macos_security) | Mac compliance baselines | Only if there is a Mac fleet | P3 |
| [BF](https://github.com/usnistgov/BF) | Bugs Framework | Root-cause labels; watch until the dashboard is live | D4 |
| [ACVP](https://github.com/usnistgov/ACVP) | Crypto algorithm validation | Only for the later post-quantum work | Watch list |
| swid-tools | Software ID tags | Superseded by SBOM formats; skip | none |

Related non-NIST repositories used above: [ATT&CK STIX data](https://github.com/mitre-attack/attack-stix-data), [ATLAS data](https://github.com/mitre-atlas/atlas-data), [CTID Mappings Explorer](https://github.com/center-for-threat-informed-defense/mappings-explorer), [Azure Sentinel content](https://github.com/Azure/Azure-Sentinel), [Drain3](https://github.com/logpai/Drain3), [Semgrep](https://github.com/semgrep/semgrep), [CBOMkit](https://github.com/IBM/cbomkit) (crypto inventory, for later post-quantum work).

## More NIST repositories, OSCAL hub and embedding POC

A keyword pass over the full NIST GitHub list added these; each was confirmed to exist on Nov 25, 2026.

| Repository | Use | Playbook item |
| --- | --- | --- |
| [caisi-cyber-evals](https://github.com/usnistgov/caisi-cyber-evals) | CAISI agentic cyber benchmarks on Inspect (CVE-Bench, Cybench, pwn.college) | A3, A6: measure Mythos before trusting it |
| [lm-text-property-eval](https://github.com/usnistgov/lm-text-property-eval) | Calibrated LLM-as-judge with a 5-level rubric | A5: check Dash rules 4, 5 and 12 on each model or prompt change |
| [trojai-baseline-pruning](https://github.com/usnistgov/trojai-baseline-pruning) | Backdoor detection in AI models | D3 |
| [AVIATOR](https://github.com/usnistgov/AVIATOR), [VTSG](https://github.com/usnistgov/VTSG) | Vulnerable and fixed code pairs | D2, A6 benchmarks |
| [ml\_uncertainty\_py](https://github.com/usnistgov/ml_uncertainty_py) | Prediction uncertainty | When automation hands off to an analyst |
| [policy-machine-core](https://github.com/usnistgov/policy-machine-core) | NGAC reference implementation | A4, D5 agent least privilege |
| [SCAP](https://github.com/usnistgov/SCAP), [scapval](https://github.com/usnistgov/scapval), [sctools](https://github.com/usnistgov/sctools), [linux\_security](https://github.com/usnistgov/linux_security) | SCAP tooling and Linux baselines | P2, P3 |
| [nccoe-ai-identity](https://github.com/usnistgov/nccoe-ai-identity) | Empty; NCCoE identity-for-AI project to watch | A4 |

OSCAL hub: keep OSCAL in one git repository and translate each tool's native data with adapters, rather than making tools speak OSCAL. Order: catalog, profile, one component definition per tool, SSP, automated assessment results, POA&M synced to Jira. Tools: [compliance-trestle](https://github.com/oscal-compass/compliance-trestle), [oscal-cli](https://github.com/usnistgov/oscal-cli), [compliance-to-policy](https://github.com/oscal-compass/compliance-to-policy), [Lula](https://github.com/defenseunicorns/lula), [oscal-xslt](https://github.com/usnistgov/oscal-xslt). For a team not using OSCAL yet, start by taking exact control IDs from oscal-content and tagging detections with them.

Embedding POC: compare four configurations (native PDFs, full text, keyword retrieval, embeddings) on 20 questions x 3 repetitions, with the same model. Embeddings must beat keyword retrieval, not just full text. The write-up's figures (96.9% fewer input tokens, $62,123 annual savings) are simulated at assumed $3 and $15 per million token rates; measure before presenting. VCC fit: the assistant is deterministic over mock data today, so these evaluations become the acceptance gate when the Copilot Studio adapter (flag phase 3) goes live.

## AgentOps v0.1 review

The attached project is a sound, honest local prototype: I re-ran its tests (6 of 6 pass) and its docs correctly say it is not NIST-compliant and that recovered hours are not cash. The dashboard numbers in your screenshots are illustrative, not measured.

What it actually does (from the source, 92 lines of Python):

- Local web server on 127.0.0.1:8765, SQLite storage, one shared access token, strict security headers, 25 KB request limit.
- Five allowlisted agent roles; a task must be declared synthetic; Claude calls are off unless `ALLOW_CLAUDE=1`.
- Flow: submit, approve execution, run (demo text or one Claude Messages API call, no tools), human review, audit event per step.
- ROI counts only reviewed Claude runs: accepted runs add baseline minus human minutes; rejected runs subtract human minutes. Demo runs are excluded.

What the screenshots show versus reality:

| Screenshot | Status |
| --- | --- |
| ROI simulator: 2,500 hours, $200,500 net, 1,671% ROI | Arithmetic on assumed inputs (10 people x 60 minutes a day x 250 days x $85, $12,000 cost); not a measurement |
| Operations Center: 1,284 tasks, 214 hours, 98.2% governance pass | Labeled "illustrative prototype, synthetic data"; the app does not compute these |
| Manager, research, analysis and writing agents with NIST probes | Describes the NIST probes repository's own pipeline; not implemented in AgentOps |

Gaps to fix before anyone outside your team sees it, in priority order:

- [ ] Separation of duties: one token means the submitter, approver and reviewer can be the same person. Add per-user identity (Entra SSO) and block self-approval (AC-5).
- [ ] Audit log records no user and can be edited in SQLite. Add actor identity and a hash chain or append-only export to Sentinel (AU-3, AU-9).
- [ ] Record model name, prompt hash and settings on every run; today the model lives only in an environment variable.
- [ ] Pin dependency versions in requirements.txt (anthropic, zensical, pytest) and generate an SBOM (SSDF PW.4).
- [ ] A run stuck in "running" after a crash never recovers; add a timeout that marks it failed.
- [ ] Price tokens automatically from the Usage and Cost API instead of typing cost by hand.
- [ ] Replace the illustrative dashboard with numbers from real pilot runs, or label every number "assumed".

Where it fits: AgentOps's approval, audit and ROI engine overlaps Dash and Automata. Fold it into Dash as the governance backend rather than shipping a fourth tool; Automata stays the deterministic monitor beside it. Its planned integrations map to sections here: CAPORDINO and OSCAL (P1), evaluation probes (A5), Dioptra (D3).

Update Nov 25, 2026: the GitHub package's `agentops/` (v0.2) fixes all seven gaps above: per-user hashed tokens with roles, separation of duties with an audited demo override, hash-chained audit with a verify endpoint, model and prompt hash per run, pinned dependencies, stale-run recovery and estimated API cost from operator-set prices. It also adds Host-header checks, failed-login throttling and safer logging. Tests went from 6 to 21, all passing; details are in `docs/security-scan-report.md`.

## Watch list and open comment periods

One substantive public comment on the adversarial ML taxonomy's agentic attack index, drawn from Automata, puts your name in NIST's public record for a few hours of work.

| Item | Status as of Nov 25, 2026 | Action |
| --- | --- | --- |
| [SP 2400-102e2026, Adversarial ML Taxonomy](https://csrc.nist.gov/pubs/sp/2400/102/e2026/ipd) | Comments due Dec 18, 2026 | Comment on the agentic index; adopt its terms in A3 |
| SP 800-221r1, ICT risk programs ([draft list](https://csrc.nist.gov/publications/draft-pubs)) | Comments due Dec 7, 2026 | Optional; relevant to ROI framing |
| [SSDF 1.2 (SP 800-218r1)](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd) | Draft | Re-map D1 when final |
| [Cyber AI Profile (IR 8596)](https://csrc.nist.gov/pubs/ir/8596/iprd) | Draft | Re-map intake when final |
| [COSAiS AI control overlays](https://csrc.nist.gov/projects/cosais) | In development | Adopt overlays when published |
| [SP 800-92r1, log management](https://csrc.nist.gov/pubs/sp/800/92/r1/ipd) | Draft since 2023 | Cite as draft in C1 |
| [IR 8547, post-quantum transition](https://csrc.nist.gov/pubs/ir/8547/final) | Final | Parked; revisit with a hybrid ML-KEM pilot and [CBOMkit](https://github.com/IBM/cbomkit) inventory |
| SP 800-52 TLS guidelines | NIST announced a revision Nov 19, 2026 | Parked with post-quantum work |
| [Bugs Framework dashboard](https://pages.nist.gov/BF/info/bf-service/bf-dashboard/) | Placeholder link, login coming soon | Recheck quarterly |
| [NIST evaluation probes](https://github.com/usnistgov/agentic-research-evaluation-probes) | Research code; NIST says probes need validation | Validate against human labels before relying on scores |

## Verification log and sources

Every link above was checked on Nov 25, 2026; the few items that could not be confirmed are listed here instead of being linked as fact.

| What | How it was verified |
| --- | --- |
| All GitHub repositories linked | `git ls-remote` succeeded for each; a made-up repository name failed, confirming the check works |
| CAPORDINO and NIST evaluation probes | Cloned and READMEs read; capabilities quoted from them |
| Dioptra, Bugs Framework, Software Security Group, NSRL, SCAP pages, NIST Godel proof article | Pages opened and read in full this session |
| NIST CSRC, Microsoft Learn, Anthropic, CISA, FIRST, NVD links | Returned as live official pages by search on Nov 25, 2026 |
| AgentOps v0.1 | Source read line by line; tests re-run, 6 of 6 pass |

Not confirmed, so not linked or flagged in place:

- Direct publication pages for IR 8621 and SP 800-221r1 (both appear on the CSRC news list you pasted).
- Azure resource-idle queries (C3) and Defender automated investigation docs (S3): use the Microsoft Learn search for current pages.
- Whether the NIST probes run against Claude through an OpenAI-compatible endpoint: check Anthropic's docs before building A5.
- Control IDs (800-53, SSDF) next to each item are proposed mappings. A control owner must confirm each one before it appears in audit evidence.
- Microsoft Sentinel tier names change often; re-read the billing page before quoting prices.

Corrections to earlier answers in our chats: SP 2400-102e2026 was published Nov 9, 2026, not Nov 12. NIST AI 800-4 (monitoring deployed AI) is from March 2026. Retirement of Sentinel's Basic tier came from a blog, not Microsoft docs, so treat it as unconfirmed.

Key sources: [NIST CSRC](https://csrc.nist.gov/) · [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) · [Microsoft Sentinel billing](https://learn.microsoft.com/en-us/azure/sentinel/billing) · [Claude Platform docs](https://platform.claude.com/docs/en/api/overview) · [NIST GitHub](https://github.com/orgs/usnistgov/repositories) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

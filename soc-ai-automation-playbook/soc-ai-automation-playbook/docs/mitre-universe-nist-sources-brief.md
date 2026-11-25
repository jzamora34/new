# MITRE Universe: NIST and Related Data Sources Brief

Prepared: November 24, 2026
Purpose: Give the MITRE Universe project an independent research task. Evaluate which NIST and related data sources should become layers in MITRE Universe, reach your own decision, then compare it to the reference recommendation in Section 6 before finalizing.

---

## 1. Instructions for the Claude reading this

1. Read Sections 2 through 5 first. **Do not read Section 6 until you have written your own recommendation.** It holds a prior recommendation, and reading it first will anchor your analysis.
2. Verify every source in Section 4 with live research: confirm it exists, it's current, its format, its license, and how it can be machine-loaded (STIX, JSON, XML, CSV, API).
3. Score each source using the criteria in Section 5.
4. Produce your own ranked list, a build order, and the graph schema additions (node and edge types) for each accepted source.
5. Then read Section 6 and produce a comparison table: where you agree, where you differ, and why. Resolve each difference with evidence, not preference.
6. Flag anything in this brief that turned out to be wrong or outdated.

---

## 2. MITRE Universe project context

- **Goal:** an open, first-of-its-kind project combining all MITRE frameworks, maps and tools (ATT&CK, ATLAS, D3FEND, CTID projects, and complementary ones) into one large interactive data visualization.
- **Core idea:** compose frameworks like DAX queries to create new graphs and surface hidden gaps. Map every possible link and find what's missing.
- **Audience:** beginner-friendly, so new analysts, senior analysts and non-technical people can use it with no learning curve. Others should be able to extend it.
- **Rule:** keep every possible chart and remove none.
- **Tech:** open to anything (D3, Plotly, ECharts, Neo4j and other knowledge graphs, GPU graphs, Tableau, Unity, Unreal, Blender). Prefers starting from Jupyter to keep it simple. Draws on IEEE VIS and VizSec research.
- **Current scope:** mostly MITRE frameworks, now extending to the vulnerability layer (CVE, CWE, CVSS, NVD, CPE). Snyk was considered as another source.
- **Out of scope:** anything specific to an employer or workplace. Judge sources only on their value to MITRE Universe as data or as build tooling.

---

## 3. The core question

Which NIST (and closely related) sources add **new nodes, new edges, or new gap views** to MITRE Universe, and in what order should they be integrated?

A source qualifies if it either:
- **adds data,** meaning new entities or relationships that can be visualized, or
- **helps build or validate** the graph (parsing, conversion, search quality).

Tools you run against systems but that produce no mappable data, such as model-testing platforms, generally don't qualify.

---

## 4. Candidate sources to research

### 4A. Control and governance layer

| Source | Location (verify) | What it may provide |
|---|---|---|
| NIST OSCAL models | https://github.com/usnistgov/OSCAL | Schemas for machine-readable control catalogs, profiles and assessments in XML, JSON and YAML |
| NIST OSCAL content | https://github.com/usnistgov/oscal-content | SP 800-53 rev 5 catalog and SP 800-53B baselines as OSCAL JSON, XML and YAML. Controls and families become nodes. |
| CTID Mappings Explorer | https://center-for-threat-informed-defense.github.io/mappings-explorer/ and https://github.com/center-for-threat-informed-defense/mappings-explorer | ATT&CK technique ↔ 800-53 control mappings, plus other mappings (cloud platforms, CVE, VERIS). Check which versions are current. |
| NIST CPRT (Cybersecurity and Privacy Reference Tool) | https://csrc.nist.gov/projects/cprt | Machine-readable exports of CSF 2.0, 800-53, SSDF, Privacy Framework and others. Confirm the export formats and whether there's an API. |
| NIST OLIR (Online Informative References) | https://csrc.nist.gov/projects/olir | NIST's official crosswalks between frameworks. These are possible edges like CSF 2.0 ↔ 800-53 ↔ others. |
| NIST CSF 2.0 | https://www.nist.gov/cyberframework | Functions, categories and subcategories. A governance-language layer for non-technical viewers. |

### 4B. Vulnerability and weakness layer

| Source | Location (verify) | What it may provide |
|---|---|---|
| NVD API 2.0 | https://nvd.nist.gov/developers | CVE records with CVSS, CWE and CPE references. An API key is recommended for rate limits. |
| NVD CPE dictionary | https://nvd.nist.gov/products/cpe | Product identifiers, linking vulnerabilities to products |
| MITRE CWE | https://cwe.mitre.org/data/downloads.html | Weakness hierarchy and its relationships to CAPEC |
| MITRE CAPEC | https://capec.mitre.org/data/downloads.html | Attack patterns linked to CWE and to ATT&CK techniques |
| NIST SARD and Juliet test suites | https://samate.nist.gov/SARD | Test cases organized by CWE. A possible "has test coverage" attribute per weakness. |

The chain to confirm is **CPE → CVE → CWE → CAPEC → ATT&CK.** Verify that every hop exists in the current data, and how complete each one is.

### 4C. AI and adversarial ML layer

| Source | Location (verify) | What it may provide |
|---|---|---|
| MITRE ATLAS data | https://github.com/mitre-atlas/atlas-data | AI attack tactics, techniques and case studies |
| NIST SP 2400-102 (2026 edition), *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations*, initial public draft | csrc.nist.gov (search for "SP 2400-102 2026") | Attack classes for predictive, generative and **agentic** AI. Includes a new index of agent-specific attacks. Published around November 9, 2026, with comments due December 18, 2026. It's a draft, so it may change. |
| NIST AI RMF 1.0 | https://www.nist.gov/itl/ai-risk-management-framework | Govern, Map, Measure, Manage functions and subcategories |
| NIST AI 600-1 (Generative AI Profile) | https://doi.org/10.6028/NIST.AI.600-1 | Generative AI risk categories and suggested actions |

### 4D. Core MITRE sources (assumed already in scope; confirm versions)

| Source | Location (verify) |
|---|---|
| ATT&CK (STIX 2.1) | https://github.com/mitre-attack/attack-stix-data |
| D3FEND | https://d3fend.mitre.org |
| CTID projects | https://github.com/center-for-threat-informed-defense |

### 4E. Build and validation tooling

| Source | Location (verify) | Possible use |
|---|---|---|
| oscal-cli | https://github.com/usnistgov/oscal-cli | Validate and convert OSCAL content before loading it into the graph |
| liboscal-java | https://github.com/usnistgov/liboscal-java | Programmatic OSCAL processing in Java |
| trec_eval | https://github.com/usnistgov/trec_eval | Scores search quality (precision, recall, nDCG). Only relevant if Universe gets a search or "ask the graph" feature. |

### 4F. Evaluated and likely excluded (confirm or overturn)

| Source | Reason it may not fit |
|---|---|
| Dioptra (https://github.com/usnistgov/dioptra) | A testing platform for ML models (PyTorch/TensorFlow). It produces test results, not mappable framework data. |
| NIST agentic evaluation probes (repo believed to be usnistgov/agentic-research-evaluation-probes) | Tooling for grading AI agent outputs. Not framework data. |
| macOS Security Compliance Project (usnistgov/macos_security) | Platform hardening baselines. Only indirectly linked to 800-53. |
| ACVP | Cryptographic algorithm validation. No mapping to MITRE frameworks. |
| swid-tools | Software identification tags, largely superseded by SBOM formats |
| SSDF (SP 800-218 / 800-218A) | Possibly useful as a control layer via CPRT. Decide whether its practices add meaningful edges to ATT&CK or CWE. |

---

## 5. Decision criteria

Score each source 1 to 5 on each criterion:

1. **New links:** does it add relationships that don't already exist in the graph?
2. **Gap-finding power:** does it enable a new "what's missing" view? Example: techniques with no mitigating control.
3. **Machine-readability:** is it available as STIX, JSON, XML or an API, with little manual cleanup?
4. **Authority and stability:** official source, maintained, versioned. Lower the score for drafts.
5. **Beginner value:** does it translate technical data into language non-technical viewers understand?
6. **Integration effort:** is the effort low relative to the value? Score high for low effort.
7. **Novelty:** is this link rarely or never visualized elsewhere? This supports the first-of-its-kind goal.

Output: a ranked list, a build order, proposed node and edge types for each accepted source, and an explicit list of rejected sources with reasons.

---

## 6. Reference recommendation (read only after writing your own)

### Accepted sources, ranked
1. **oscal-content (800-53 rev 5) plus CTID ATT&CK ↔ 800-53 mappings.** Adds the technique → control link. This is the strongest gap-finder: techniques with no mitigating control, and controls that cover no technique.
2. **CWE → CAPEC → ATT&CK chain, plus NVD/CVE and CPE.** Completes the path from vulnerable product → weakness → attack pattern → adversary technique. This extends the vulnerability layer already in scope.
3. **CPRT and OLIR crosswalks (CSF 2.0 ↔ 800-53).** Chains ATT&CK → 800-53 → CSF 2.0, so a technique can be read in governance language. High beginner value.
4. **NIST SP 2400-102 (2026 draft) ↔ ATLAS.** Maps NIST's adversarial ML attack classes, including the new agentic index, onto ATLAS techniques. High novelty, but it's a draft, so tag it as provisional and plan to re-sync after the final version.
5. **AI RMF and AI 600-1 ↔ ATLAS.** AI risk categories linked to known AI attack paths.
6. **SARD and Juliet by CWE.** A per-weakness "has test cases" attribute that enables a test coverage gap view.

### Tooling accepted
- oscal-cli and liboscal-java, to validate and convert OSCAL before ingestion.
- trec_eval, only if a search or question-answering feature is added.

### Rejected
- Dioptra, evaluation probes, mSCP, ACVP and swid-tools. These are things you run, not data to map.
- SSDF is undecided, pending whether it adds meaningful edges.

### Build order
1. ATT&CK ↔ 800-53 (via oscal-content plus CTID mappings)
2. CWE / CAPEC / CVE / CPE chain
3. CSF 2.0 via OLIR and CPRT
4. ATLAS ↔ NIST AML taxonomy, then AI RMF and AI 600-1
5. SARD coverage attributes

Rationale: each step adds a new layer of gaps on top of the previous one, and the earliest steps use the most stable, machine-readable data.

### Known uncertainties in this reference
- Exact export formats and API availability for CPRT and OLIR were not verified.
- The CTID mapping versions and how fully they cover the current ATT&CK release were not verified.
- The SP 2400-102 draft's exact categories and agentic index were not read in full. Only NIST's summary and news coverage were reviewed.
- The evaluation probes repository name was inferred from a fork and not confirmed.
- The NIST GitHub organization has about 1,459 repositories. Only a subset was reviewed, so other relevant repositories may exist.

---

## 7. Required output format

1. Verification results for each source in Section 4 (exists, format, license, current version)
2. Scoring table using the Section 5 criteria
3. Your ranked list and build order
4. Graph schema additions (node and edge types) for each accepted source
5. Comparison table against Section 6: agree, differ, reason, resolution
6. Final decision and the corrections to this brief

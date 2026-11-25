# NIST GitHub survey for SOC AI and automation work

As of November 25, 2026. The [usnistgov organization](https://github.com/orgs/usnistgov/repositories) holds about 1,459 repositories. Most are materials science, robotics, genomics, biometrics and old training-workshop sites. About 30 matter for SOC, AI governance and automation work. None is a SOC tool in the usual sense (no detection rules, playbooks or SIEM content); NIST provides evaluation harnesses, machine-readable controls and hardening baselines. Most NIST-authored code is not subject to copyright in the US (17 U.S.C. 105); check each repository's LICENSE before use.

Every repository below was confirmed to exist with `git ls-remote` on Nov 25, 2026. The org listing was pulled from the public GitHub API and filtered by keyword, so repositories with no description may be missing.

## Start with these

| Repository | What it does for you | Fit |
| --- | --- | --- |
| [OSCAL](https://github.com/usnistgov/OSCAL), [oscal-content](https://github.com/usnistgov/oscal-content), [oscal-cli](https://github.com/usnistgov/oscal-cli), [liboscal-java](https://github.com/usnistgov/liboscal-java) | SP 800-53 rev 5 and baselines as JSON, XML, YAML; validation and conversion | Map detections to controls; generate evidence. See `oscal-hub-plan.md` |
| [capordino](https://github.com/usnistgov/capordino) | Converts CPRT datasets to OSCAL: CSF 2.0, SP 800-171r3, SSDF 1.1, SP 800-66r2, SP 800-172/172A, AI RMF 1.0. Java + Maven 3.9 | AI RMF and CSF as machine-readable catalogs |
| [dioptra](https://github.com/usnistgov/dioptra) | ML test platform (release 1.1.0): evasion, poisoning, extraction experiments; supports AI RMF Measure. Docker, MLflow, PyTorch/TensorFlow workers; access controls listed as coming soon | Only for ML models you train (phishing classifiers, UEBA). Not for hosted LLMs |
| [caisi-cyber-evals](https://github.com/usnistgov/caisi-cyber-evals) | CAISI's agentic cyber benchmarks on the Inspect framework: CVE-Bench (7 tasks), Cybench, pwn.college dojo conversion | Measure what a model can actually do on security tasks before trusting it with triage or code review (Mythos benchmark) |
| [agentic-research-evaluation-probes](https://github.com/usnistgov/agentic-research-evaluation-probes) | Deep-research agent with faithfulness, completeness and sufficiency probes per citation. OpenAI Agents SDK; any OpenAI-compatible endpoint; NIST says probes need validation | Grounding checks for Dash assistant answers |
| [lm-text-property-eval](https://github.com/usnistgov/lm-text-property-eval) | Calibrated LLM-as-judge: builds a 5-level rubric from samples, then scores every text chunk with structured output | Score AI-written triage summaries and Dash drafts; catch regressions on prompt or model changes |
| [trec_eval](https://github.com/usnistgov/trec_eval) | Standard retrieval scoring (precision, recall, MRR, nDCG) | Score RAG retrieval; `tools/embedding-roi/metrics.py` writes its run and qrels files |
| [macos_security](https://github.com/usnistgov/macos_security), [linux_security](https://github.com/usnistgov/linux_security) | Hardening baselines, compliance scripts, MDM profiles | Scheduled checks with drift sent to the SIEM |

## Useful for specific needs

| Repository | Use |
| --- | --- |
| [trojai-baseline-pruning](https://github.com/usnistgov/trojai-baseline-pruning) | Backdoor (trojan) detection in AI models; check third-party models before deployment |
| [AVIATOR](https://github.com/usnistgov/AVIATOR), [VTSG](https://github.com/usnistgov/VTSG) | Generate vulnerable and fixed code pairs; benchmark AI code reviewers and scanners alongside SARD/Juliet |
| [test_code_eval](https://github.com/usnistgov/test_code_eval) | NIST GenAI code for scoring and validating generated test code |
| [ml_uncertainty_py](https://github.com/usnistgov/ml_uncertainty_py) | Prediction uncertainty; decide when automation acts alone and when it hands off to an analyst |
| [MediScore](https://github.com/usnistgov/MediScore) | Media-forensics scoring; compare deepfake detectors for vishing and BEC cases |
| [dmarc-tester](https://github.com/usnistgov/dmarc-tester) | SPF, DKIM, DMARC test reflector; validate phishing-triage logic and mail posture |
| [mobile-threat-catalogue](https://github.com/usnistgov/mobile-threat-catalogue), [IoT-Device-Cybersecurity-Requirement-Catalogs](https://github.com/usnistgov/IoT-Device-Cybersecurity-Requirement-Catalogs) | Structured threat and requirement lists for alert tagging |
| [SCAP](https://github.com/usnistgov/SCAP), [scapval](https://github.com/usnistgov/scapval), [sctools](https://github.com/usnistgov/sctools) | SCAP specifications, validation, baseline tailoring and overlay tools |
| [policy-machine-core](https://github.com/usnistgov/policy-machine-core) | NGAC reference implementation; a model for per-agent tool and data permissions |
| [SDNist](https://github.com/usnistgov/SDNist) | Synthetic data quality; only useful when you have real data to compare against |
| [nccoe-migration-post-quantum-cryptography](https://github.com/usnistgov/nccoe-migration-post-quantum-cryptography) | Crypto inventory for the later post-quantum work |
| [oscal-xslt](https://github.com/usnistgov/oscal-xslt), [metaschema](https://github.com/usnistgov/metaschema) | Render OSCAL as HTML for auditors; the modeling language behind OSCAL |
| [ACVP](https://github.com/usnistgov/ACVP) | Crypto algorithm validation protocol; post-quantum work only |
| [BF](https://github.com/usnistgov/BF) | Bugs Framework (SP 800-231); dashboard not live yet |

## Worth watching

- [nccoe-ai-identity](https://github.com/usnistgov/nccoe-ai-identity): empty today; the name points to an NCCoE project on identity for AI systems, directly relevant to agent identities.
- [ai-technology-evaluation](https://github.com/usnistgov/ai-technology-evaluation), [NIST-AI-Consortium](https://github.com/usnistgov/NIST-AI-Consortium): early AI evaluation work and consortium documents.

## How they help VCC (Dash)

The current VCC assistant is deterministic code over mock data (`tier1.ts`: "Deterministic and derived only from mock data; never invents facts"), so existing Vitest tests already cover it better than an evaluation tool. The tools become valuable when the live adapter connects the assistant to Copilot Studio and answers come from a real LLM:

1. **trec_eval** scores whether retrieval returns the right Jira, ServiceNow and SharePoint items (and the TF-IDF matcher in `similarRequests.ts`). Score retrieved context and generated answer separately, because either can cause a wrong answer.
2. **lm-text-property-eval** checks VCC rules 4 (every claim cites a timestamped source), 5 (AI never invents delay reasons) and 12 (refuse questions that evaluate people) on every model or prompt change. Results feed the Agents Drift tab's eval pass rate (`AgentEvalRuns` in `04-DATA-MODEL.md`), which today has no real suite behind it.
3. **oscal-content** supplies exact SP 800-53 control IDs and wording for `SECURITY-CONTROLS.md`, independent of the backend.

Not useful for VCC: dioptra and trojai-baseline-pruning (VCC trains no models), SDNist (rule 8 forbids real data, so nothing to compare), policy-machine-core (VCC access comes from SharePoint and Power Platform permissions), macos/linux_security, caisi-cyber-evals and dmarc-tester (endpoints, model capability and mail, not a web frontend).

Recommendation: add trec_eval and the LLM judge as an acceptance step in the phase that wires up Copilot Studio (flag phase 3, `orchestratorClient`). They live in `measurement/` as developer tooling, run against mock data, and never ship in `src/`, so `scrub.py` can export them safely to the public Dash copy.

# Security scan report

Scanned November 25, 2026, before the first commit. Scope: all code and docs in this repository. Result: **no open findings**. Eleven issues found by manual review of AgentOps v0.1 are fixed in v0.2; the four automated findings below are false positives.

## Tools and results

| Tool | Version | Scope | Result |
| --- | --- | --- | --- |
| Bandit (Python SAST) | 1.9.4 | `agentops/`, `tools/` (tests excluded) | 0 findings. v0.1 showed only B101 `assert` in tests, which is expected in pytest |
| pip-audit (known CVEs in dependencies) | latest | `agentops/requirements.txt` (anthropic 2.14.0, zensical 0.1.3, pytest 9.2.0) | No known vulnerabilities |
| Semgrep 1.187.0 with [semgrep-rules](https://github.com/semgrep/semgrep-rules) (python, javascript, html, generic/secrets) | 1.187.0 | Whole repository | 4 findings, all false positives (below) |
| detect-secrets | latest | Whole repository, all files | No secrets |
| Manual code review | n/a | `agentops/app.py`, `static/`, schema | 11 issues, fixed (below) |
| pytest | 9.2.0 | `agentops/tests` (21), `tools/embedding-roi` (9) | 30 of 30 pass |

The Semgrep registry (semgrep.dev) was unreachable from the scan environment, so the community rules were cloned from GitHub and run locally. GitHub CI (`.github/workflows/ci.yml`) re-runs Bandit, pip-audit and the tests on every push.

## False positives

| Finding | Location | Why it is not a vulnerability |
| --- | --- | --- |
| `jquery-insecure-selector` (x2) | `agentops/static/dashboard.js` lines 3 and 4 | `$` is a one-line alias for `document.getElementById`, not jQuery, and every argument is a constant element ID. All untrusted text is inserted with `textContent`, never `innerHTML` |
| `return-not-in-function` (x2) | `tools/embedding-roi/metrics.py` dataclass fields | The rule misreads `lambda` default factories inside `field(...)` |

## AgentOps v0.1 to v0.2 fixes (manual review)

| # | Issue in v0.1 | Risk | Fix in v0.2 | Control |
| --- | --- | --- | --- | --- |
| 1 | One shared token for everyone | No identity; anyone with the token is everyone | Per-user tokens with roles; only SHA-256 hashes stored (`users.json`, git-ignored, mode 0600) | IA-2, AC-2 |
| 2 | Submitter could approve and review own run | No separation of duties | Blocked; demo override via env var is written to the audit log | AC-5 |
| 3 | Audit rows had no actor | Cannot tell who did what | Actor on every event; submitted_by, approved_by, reviewed_by on each run | AU-3 |
| 4 | Audit log editable without trace | Tampering undetectable | SHA-256 hash chain, `/api/audit/verify`, IMMEDIATE transactions so concurrent writes cannot fork the chain | AU-9, AU-10 |
| 5 | Model and prompt not recorded | Results not reproducible | Model ID and system-prompt SHA-256 per run | AU-3, AI RMF Measure |
| 6 | Unpinned dependencies | Unreviewed upgrades, supply-chain risk | Exact versions; Dependabot plus pip-audit in CI | SA-12, SSDF PW.4 |
| 7 | Crash left runs stuck in `running` | Silent loss; inaccurate metrics | Timeout recovery marks them failed and audits it | SI-11 |
| 8 | Non-object JSON body (`[]`) crashed the handler | Unhandled exception per request | Body must be an object; AttributeError handled; returns 400 | SI-10 |
| 9 | No Host-header check | DNS-rebinding exposure of a localhost service | Only `127.0.0.1` and `localhost` accepted; others get 421 | SC-7 |
| 10 | Unlimited token guessing | Brute force | 10 failures per address per 5 minutes, then 429 | AC-7 |
| 11 | Server header leaked Python version; default request logging | Fingerprinting; risk of logging sensitive data | Generic server header; logs exclude headers and bodies; `Referrer-Policy: no-referrer`; stricter CSP (`base-uri`, `form-action`) | SC-8, SI-11 |

Also added: estimated API cost per run from operator-set prices (no hardcoded prices), `autocomplete="off"` on the token field.

## Remaining risks, accepted for a local synthetic-data pilot

- A database administrator can rebuild the whole hash chain. Production needs export to an append-only store such as Sentinel.
- No enterprise SSO, DLP or prompt-injection detection. The synthetic-data checkbox is a declaration, not a control.
- Task, source and output are stored in plaintext SQLite.
- Claude mode trusts the model provider; review data-handling terms before any non-synthetic use.

These match the "not enforced" list in `agentops/docs/governance.md`.

## Content review

- No credentials, tokens, internal hostnames or employee data are committed.
- Copyrighted books and MITRE all-rights-reserved PDFs are excluded (see `source-documents.md`).
- The `.gitignore` files exclude databases, `users.json`, `.env` and virtual environments.

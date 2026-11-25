# Security policy

## Reporting

Report suspected vulnerabilities privately through GitHub's "Report a vulnerability" (private vulnerability reporting) on this repository. Do not open public issues for security problems.

## Scope

- `agentops/`: a local pilot that binds to 127.0.0.1 and is meant for synthetic data only. Exposing it on a network is out of scope and unsupported.
- `tools/`: offline measurement scripts.

## Practices

- Every push runs tests, Bandit and pip-audit in CI; Dependabot proposes dependency updates.
- Dependencies are pinned to exact versions.
- Secrets (API keys, user tokens, `users.json`, `.env`) must never be committed; `.gitignore` excludes them.
- The latest scan is in `docs/security-scan-report.md`.

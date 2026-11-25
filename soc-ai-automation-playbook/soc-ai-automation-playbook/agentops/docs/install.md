# Installation from scratch

1. Install Python 3.11 or newer (https://www.python.org/downloads/) and VS Code (https://code.visualstudio.com/).
2. Open the `agentops` folder in VS Code and open a terminal.
3. Create a virtual environment and install the pinned dependencies.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

4. Create users. Each command prints a token once; store it in a password manager. Tokens are never saved, only their SHA-256 hashes in `users.json` (git-ignored).

```powershell
.\.venv\Scripts\python.exe app.py new-user alice submitter
.\.venv\Scripts\python.exe app.py new-user bob approver
.\.venv\Scripts\python.exe app.py new-user carol reviewer
```

Separation of duties blocks a submitter from approving or reviewing their own run. For a one-person demo only, set `$env:AGENTOPS_ALLOW_SELF_APPROVAL = "1"`; every override is written to the audit log.

5. Start the server and open http://127.0.0.1:8765. Paste your token.

```powershell
.\.venv\Scripts\python.exe app.py
```

6. Run the tests: `.\.venv\Scripts\python.exe -m pytest -q`
7. Build the docs: `.\.venv\Scripts\zensical.exe build` (preview with `serve`).
8. Optional Claude mode, only after enterprise approval: set `ALLOW_CLAUDE=1`, `CLAUDE_MODEL` to the approved model ID and `ANTHROPIC_API_KEY` from your approved secret store. Set `PRICE_INPUT_PER_MTOK` and `PRICE_OUTPUT_PER_MTOK` from https://platform.claude.com/docs/en/about-claude/pricing to record estimated cost per run. Never commit credentials.

Linux/macOS: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`, then the same `python app.py ...` commands.

Upgrading from v0.1: delete the old `agentops.db`; the v0.2 schema adds identity and audit-chain columns.

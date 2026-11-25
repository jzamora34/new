# Operations and troubleshooting

- Identity: per-user tokens with roles (submitter, approver, reviewer). Rotate a token by running `new-user` again for that name. Remove a user by deleting their entry in `users.json` and restarting.
- Throttling: 10 failed token attempts from one address within 5 minutes returns HTTP 429 until the window passes.
- Audit integrity: `GET /api/audit/verify` (with a token) recomputes the hash chain and reports the first broken sequence number. Export audit rows to Sentinel or another append-only store for production; a database administrator could rebuild the whole chain locally.
- Crash recovery: runs stuck in `running` longer than `AGENTOPS_RUN_TIMEOUT_S` (default 300) are marked failed with error `Timeout` and an audit event.
- Data: SQLite stores task, source and output in plaintext; the database and users file are created with owner-only permissions on POSIX systems. Use synthetic data only.
- Network: binds to 127.0.0.1 and rejects requests whose Host header is not local. Do not expose it on a shared interface.
- Logs: request logs never include headers or bodies.
- Port in use: set `AGENTOPS_PORT`.
- API failures: check model availability, authorization, network policy and credentials. Errors are stored as exception type names only.

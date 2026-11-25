# Governance and architecture
Browser -> localhost API -> role allowlist and classification declaration -> pending approval -> demo or Claude Messages API -> human review -> SQLite audit and metrics.

Enforced (v0.2): per-user hashed tokens with roles, separation of duties between submitter, approver and reviewer (audited override for demos), hash-chained audit log with verification endpoint, actor on every audit event, model and system-prompt SHA-256 recorded per run, estimated API cost from operator-set prices, role allowlist, declared synthetic classification, explicit Claude opt-in, bounded input and output, approval state transitions, stale-run recovery, Host-header check, failed-auth throttling, no agent tools. Not enforced: automatic DLP, enterprise SSO (Entra), semantic prompt-injection detection, externally anchored audit (a database admin can rebuild the chain), budget limits. A classification checkbox is not DLP.

Proposed NIST AI RMF mapping (not an assessment): GOVERN: ownership and approval; MAP: task inventory and data classification; MEASURE: labeled evaluation and human review; MANAGE: release gates, rollback and incident response. Obtain control owner sign-off and exact catalog IDs before claiming alignment.

Schema: schemas/database.sql defines run and audit tables. Status transitions pending -> running -> review/failed -> accepted/rejected. API POST /api/submit accepts role, task, source, mode, classification; /api/execute accepts id; /api/review accepts id, decision, baseline, human, cost. GET /api/state returns runs, audit and metrics. All API calls require X-AgentOps-Token.

OSCAL integration plan: import official catalogs, validate against matching published schema, map approved control IDs to evidence artifacts, export assessment results with UUIDs and timestamps. The local database is not OSCAL. CAPORDINO generates catalogs; it does not enforce controls.

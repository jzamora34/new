-- Agent Operations Center schema (v0.2). Delete an older agentops.db before first run; v0.1 tables are incompatible.
CREATE TABLE IF NOT EXISTS runs(
  id TEXT PRIMARY KEY,
  role TEXT NOT NULL,
  task TEXT NOT NULL,
  source TEXT NOT NULL,
  mode TEXT NOT NULL CHECK(mode IN ('demo','claude')),
  status TEXT NOT NULL CHECK(status IN ('pending','running','review','failed','accepted','rejected')),
  created REAL NOT NULL,
  started REAL,
  submitted_by TEXT NOT NULL,
  approved_by TEXT,
  reviewed_by TEXT,
  model TEXT DEFAULT '',
  prompt_sha256 TEXT DEFAULT '',
  output TEXT DEFAULT '',
  tokens INTEGER DEFAULT 0,
  input_tokens INTEGER DEFAULT 0,
  output_tokens INTEGER DEFAULT 0,
  est_cost REAL,
  seconds REAL DEFAULT 0,
  error TEXT DEFAULT '',
  baseline REAL DEFAULT 0,
  human REAL DEFAULT 0,
  cost REAL DEFAULT 0
);
-- Hash-chained audit log: hash = sha256([prev_hash, ts, event, actor, data]). Verify with GET /api/audit/verify.
CREATE TABLE IF NOT EXISTS audit(
  seq INTEGER PRIMARY KEY AUTOINCREMENT,
  ts REAL NOT NULL,
  event TEXT NOT NULL,
  actor TEXT NOT NULL,
  data TEXT NOT NULL,
  prev_hash TEXT NOT NULL,
  hash TEXT NOT NULL UNIQUE
);

import io
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app  # noqa: E402
import pytest  # noqa: E402

ALL = {"submitter", "approver", "reviewer"}


@pytest.fixture(autouse=True)
def db(tmp_path, monkeypatch):
    monkeypatch.setattr(app, "DB", tmp_path / "test.db")
    monkeypatch.setattr(app, "USERS_FILE", tmp_path / "users.json")
    monkeypatch.setenv("AGENTOPS_ALLOW_SELF_APPROVAL", "1")
    for k in ("ALLOW_CLAUDE", "PRICE_INPUT_PER_MTOK", "PRICE_OUTPUT_PER_MTOK"):
        monkeypatch.delenv(k, raising=False)
    app._failed.clear()
    app.init()


def task(**kw):
    return dict(role="research", task="Summarize", source="Synthetic example", classification="synthetic", **kw)


# ---- original v0.1 behaviour, kept
def test_roi():
    assert app.roi(1, 60, 85, 12000)["net"] == 9250


def test_zero_cost():
    assert app.roi(1, 60, 85, 0)["roi_pct"] is None


def test_flow():
    i = app.submit(task())
    app.execute(i)
    app.review(i, dict(decision="accepted", baseline=30, human=5, cost=0))
    s = app.snapshot()
    assert s["runs"][0]["status"] == "accepted"
    assert s["metrics"]["hours_saved"] == 0  # demo runs are excluded from measured savings
    events = [e["event"] for e in s["audit"]]
    assert events.count("submitted") == 1 and events.count("reviewed") == 1
    with pytest.raises(ValueError):
        app.execute(i)


def test_denied_classification():
    d = task()
    d["classification"] = "internal"
    with pytest.raises(ValueError):
        app.submit(d)


def test_claude_disabled():
    with pytest.raises(ValueError):
        app.submit(task(mode="claude"))


def test_invalid_review():
    i = app.submit(task())
    app.execute(i)
    with pytest.raises(ValueError):
        app.review(i, dict(decision="accepted", human=float("nan")))


# ---- new controls
def test_separation_of_duties(monkeypatch):
    monkeypatch.delenv("AGENTOPS_ALLOW_SELF_APPROVAL")
    i = app.submit(task(), "alice", ALL)
    with pytest.raises(PermissionError):
        app.execute(i, "alice", ALL)
    app.execute(i, "bob", {"approver"})
    with pytest.raises(PermissionError):
        app.review(i, dict(decision="accepted"), "alice", ALL)
    app.review(i, dict(decision="accepted"), "carol", {"reviewer"})
    run = app.snapshot()["runs"][0]
    assert (run["submitted_by"], run["approved_by"], run["reviewed_by"]) == ("alice", "bob", "carol")


def test_self_approval_override_is_audited():
    i = app.submit(task(), "alice", ALL)
    app.execute(i, "alice", ALL)
    assert "sod_override" in [e["event"] for e in app.snapshot()["audit"]]


def test_roles_enforced():
    with pytest.raises(PermissionError):
        app.submit(task(), "viewer", {"reviewer"})


def test_audit_chain_detects_tampering():
    i = app.submit(task())
    app.execute(i)
    assert app.verify_audit()["ok"]
    with app.connect() as c:
        c.execute("UPDATE audit SET data='{}' WHERE seq=1")
    result = app.verify_audit()
    assert not result["ok"] and result["broken_at_seq"] == 1


def test_audit_chain_detects_deletion():
    i = app.submit(task())
    app.execute(i)
    with app.connect() as c:
        c.execute("DELETE FROM audit WHERE seq=2")
    assert not app.verify_audit()["ok"]


def test_stale_run_recovered():
    i = app.submit(task())
    with app.connect() as c:
        c.execute("UPDATE runs SET status='running', started=? WHERE id=?", (time.time() - 10_000, i))
    assert app.recover_stale() == 1
    run = app.snapshot()["runs"][0]
    assert run["status"] == "failed" and run["error"] == "Timeout"


def test_cost_estimate(monkeypatch):
    assert app.estimate_cost(1000, 1000) is None
    monkeypatch.setenv("PRICE_INPUT_PER_MTOK", "3")
    monkeypatch.setenv("PRICE_OUTPUT_PER_MTOK", "15")
    assert app.estimate_cost(1_000_000, 100_000) == pytest.approx(4.5)
    monkeypatch.setenv("PRICE_INPUT_PER_MTOK", "-1")
    with pytest.raises(ValueError):
        app.estimate_cost(1, 1)


def test_users_store_only_hashes():
    token = app.new_user("alice", ["submitter"])
    raw = app.USERS_FILE.read_text()
    assert token not in raw
    assert app.identify(token, app.load_users()) == ("alice", {"submitter"})
    assert app.identify("wrong", app.load_users()) is None
    assert app.identify("", app.load_users()) is None


def test_new_user_rejects_bad_roles():
    with pytest.raises(SystemExit):
        app.new_user("mallory", ["admin"])


# ---- HTTP handler
class FakeHandler(app.Handler):
    def __init__(self, method, path, token="", body=b"", host="127.0.0.1:8765"):
        self.rfile, self.wfile = io.BytesIO(body), io.BytesIO()
        self.client_address = ("127.0.0.1", 5000)
        self.request_version, self.command, self.path = "HTTP/1.1", method, path
        self.requestline = f"{method} {path} HTTP/1.1"
        self.headers = {"Host": host, "X-AgentOps-Token": token, "Content-Length": str(len(body))}

    def status(self):
        return int(self.wfile.getvalue().split(b" ", 2)[1])


@pytest.fixture
def token():
    t = app.new_user("alice", ["submitter", "approver", "reviewer"])
    app.Handler.users = app.load_users()
    return t


def run(method, path, token="", body=b"", host="127.0.0.1:8765"):
    h = FakeHandler(method, path, token, body, host)
    getattr(h, "do_" + method)()
    return h


def test_http_requires_token(token):
    assert run("GET", "/api/state").status() == 401
    assert run("GET", "/api/state", token).status() == 200


def test_http_rejects_foreign_host(token):
    assert run("GET", "/api/state", token, host="evil.example:8765").status() == 421


def test_http_non_object_body(token):
    assert run("POST", "/api/submit", token, b"[1,2]").status() == 400


def test_http_submit_and_verify(token):
    body = json.dumps(task()).encode()
    assert run("POST", "/api/submit", token, body).status() == 200
    h = run("GET", "/api/audit/verify", token)
    assert h.status() == 200 and b'"ok": true' in h.wfile.getvalue()


def test_http_throttles_failed_auth(token):
    for _ in range(app.FAIL_LIMIT):
        run("GET", "/api/state", "bad")
    assert run("GET", "/api/state", token).status() == 429


def test_static_served_without_token(token):
    h = run("GET", "/")
    assert h.status() == 200 and b"Content-Security-Policy" in h.wfile.getvalue()

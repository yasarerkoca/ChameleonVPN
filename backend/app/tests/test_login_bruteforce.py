from fastapi import FastAPI, Response
from starlette.testclient import TestClient
import app.middleware.login_bruteforce as lb


def test_bypass_non_auth_route(monkeypatch):
    called = False

    def fake_sessionlocal():
        nonlocal called
        called = True
        raise RuntimeError("SessionLocal should not be called for non-auth routes")

    monkeypatch.setattr(lb, "SessionLocal", fake_sessionlocal)

    app = FastAPI()
    app.add_middleware(lb.LoginBruteForceMiddleware)

    @app.get("/non-auth")
    def non_auth():
        return {"ok": True}

    client = TestClient(app)
    resp = client.get("/non-auth")
    assert resp.status_code == 200
    assert called is False


def test_login_attempt_success_clears_attempts(monkeypatch):
    events = []

    class DummyDB:
        def close(self):
            events.append("close")

    def fake_sessionlocal():
        events.append("session")
        return DummyDB()

    def fake_count(db, ip):
        events.append("count")
        return 0

    def fake_clear(db, ip):
        events.append("clear")

    def fake_log(db, ip, email):
        events.append("log")

    monkeypatch.setattr(lb, "SessionLocal", fake_sessionlocal)
    monkeypatch.setattr(lb, "count_recent_failed_attempts", fake_count)
    monkeypatch.setattr(lb, "clear_failed_attempts", fake_clear)
    monkeypatch.setattr(lb, "log_failed_attempt", fake_log)

    app = FastAPI()
    app.add_middleware(lb.LoginBruteForceMiddleware)

    @app.post("/auth/2fa/login-totp")
    def login_success():
        return {"ok": True}

    client = TestClient(app)
    resp = client.post("/auth/2fa/login-totp", json={"email": "a@example.com"})
    assert resp.status_code == 200
    assert events == ["session", "count", "clear", "close"]


def test_login_attempt_failure_logs(monkeypatch):
    events = []

    class DummyDB:
        def close(self):
            events.append("close")

    def fake_sessionlocal():
        events.append("session")
        return DummyDB()

    def fake_count(db, ip):
        events.append("count")
        return 0

    def fake_clear(db, ip):
        events.append("clear")

    def fake_log(db, ip, email):
        events.append("log")

    monkeypatch.setattr(lb, "SessionLocal", fake_sessionlocal)
    monkeypatch.setattr(lb, "count_recent_failed_attempts", fake_count)
    monkeypatch.setattr(lb, "clear_failed_attempts", fake_clear)
    monkeypatch.setattr(lb, "log_failed_attempt", fake_log)

    app = FastAPI()
    app.add_middleware(lb.LoginBruteForceMiddleware)

    @app.post("/auth/2fa/login-totp")
    def login_fail():
        return Response(status_code=401)

    client = TestClient(app)
    resp = client.post("/auth/2fa/login-totp", json={"email": "a@example.com"})
    assert resp.status_code == 401
    assert events == ["session", "count", "log", "close"]

import importlib
import time

import pytest
from fastapi import FastAPI, HTTPException
from starlette.testclient import TestClient


def test_session_hijack_respects_ttl_expiry(monkeypatch):
    monkeypatch.setenv("SESSION_CACHE_TTL", "1")
    sh = importlib.reload(importlib.import_module("app.middleware.session_hijack"))

    app = FastAPI()
    app.add_middleware(sh.SessionHijackMiddleware)

    @app.get("/protected")
    async def root():
        return {"ok": True}

    client = TestClient(app)
    client.cookies.set("session_id", "abc")

    r1 = client.get("/protected", headers={"user-agent": "ua1"})
    assert r1.status_code == 200

    with pytest.raises(HTTPException):
        client.get("/protected", headers={"user-agent": "ua2"})

    time.sleep(1.1)

    r3 = client.get("/protected", headers={"user-agent": "ua2"})
    assert r3.status_code == 200

import os
import sys
import time
import types
import importlib.util
from pathlib import Path

from fastapi import FastAPI, HTTPException
from starlette.testclient import TestClient
import pytest


def _load_session_hijack_module() -> types.ModuleType:
    module_dir = Path(__file__).resolve().parent / "app" / "middleware"
    app_pkg = types.ModuleType("app")
    app_pkg.__path__ = [str(module_dir.parent.parent)]
    sys.modules.setdefault("app", app_pkg)

    middleware_pkg = types.ModuleType("app.middleware")
    middleware_pkg.__path__ = [str(module_dir)]
    sys.modules["app.middleware"] = middleware_pkg

    spec = importlib.util.spec_from_file_location(
        "app.middleware.session_hijack", module_dir / "session_hijack.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_session_hijack_respects_ttl_expiry():
    os.environ["SESSION_CACHE_TTL"] = "1"
    sh = _load_session_hijack_module()

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

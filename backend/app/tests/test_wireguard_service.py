import os
import sys
from pathlib import Path
import subprocess
import types

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure required environment variables for app config
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "x" * 32)
os.environ.setdefault("SESSION_SECRET_KEY", "y" * 32)
os.environ.setdefault("PASSWORD_RESET_URL", "https://example.com/reset")
os.environ.setdefault("EMAIL_VERIFY_URL", "https://example.com/verify")

# Allow import of `app` package
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Provide a minimal FastAPI HTTPException stub so tests run without FastAPI installed
fastapi_stub = types.ModuleType("fastapi")


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


fastapi_stub.HTTPException = HTTPException
sys.modules.setdefault("fastapi", fastapi_stub)

from app.config.database import Base
from app.models.vpn.vpn_server import VPNServer
from app.models.vpn.vpn_key import VPNKey
from app.models.vpn.vpn_peer import VPNPeer
from app.services.wireguard_service import allocate_peer, revoke_peer


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def _setup_server_and_key(db):
    server = VPNServer(name="srv", ip_address="1.2.3.4", type="wireguard")
    db.add(server)
    db.commit()
    db.refresh(server)
    key = VPNKey(
        server_id=server.id,
        public_key="pubkey",
        private_key="privkey",
        ip_address="10.0.0.2",
    )
    db.add(key)
    db.commit()
    db.refresh(key)
    return server, key


def test_allocate_peer_configures_wireguard(monkeypatch, db):
    server, key = _setup_server_and_key(db)
    captured = {}

    def fake_run(cmd, check):
        captured["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    peer, _ = allocate_peer(db, user_id=1, server_id=server.id)

    assert captured["cmd"] == [
        "wg",
        "set",
        "wg0",
        "peer",
        key.public_key,
        "allowed-ips",
        f"{key.ip_address}/32",
    ]
    assert peer.ip_address == key.ip_address
    assert db.query(VPNPeer).count() == 1


def test_allocate_peer_failure_rolls_back(monkeypatch, db):
    server, key = _setup_server_and_key(db)

    def fake_run(cmd, check):
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(HTTPException):
        allocate_peer(db, user_id=1, server_id=server.id)

    assert db.query(VPNPeer).count() == 0
    assert db.query(VPNKey).first().is_allocated is False


def _setup_peer(db):
    server, key = _setup_server_and_key(db)
    key.is_allocated = True
    peer = VPNPeer(user_id=1, server_id=server.id, key_id=key.id, ip_address=key.ip_address)
    db.add(peer)
    db.commit()
    db.refresh(peer)
    return peer, key


def test_revoke_peer_removes_from_wireguard(monkeypatch, db):
    peer, key = _setup_peer(db)
    captured = {}

    def fake_run(cmd, check):
        captured["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    revoke_peer(db, peer.id)

    assert captured["cmd"] == ["wg", "set", "wg0", "peer", key.public_key, "remove"]
    assert db.query(VPNPeer).count() == 0
    assert db.query(VPNKey).first().is_allocated is False


def test_revoke_peer_failure_rolls_back(monkeypatch, db):
    peer, key = _setup_peer(db)

    def fake_run(cmd, check):
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(HTTPException):
        revoke_peer(db, peer.id)

    assert db.query(VPNPeer).count() == 1
    assert db.query(VPNKey).first().is_allocated is True


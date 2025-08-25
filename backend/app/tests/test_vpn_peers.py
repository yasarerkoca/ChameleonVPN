import pytest
from fastapi import status

from app.utils.token import create_email_verification_token
from app.config.database import SessionLocal
from app.models.user.user import User
from app.models.vpn.vpn_server import VPNServer
from app.models.vpn.vpn_key import VPNKey


@pytest.mark.asyncio
async def test_peer_crud_flow(client):
    # register and verify user
    user_data = {
        "email": "peeruser@example.com",
        "password": "PeerPass123!",
        "full_name": "Peer User",
    }
    resp = await client.post("/auth/register", json=user_data)
    assert resp.status_code in (
        status.HTTP_201_CREATED,
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_409_CONFLICT,
    ), resp.text
    token = create_email_verification_token(user_data["email"])
    await client.get(f"/auth/verify-email?token={token}")
    login_resp = await client.post(
        "/auth/login",
        json={"email": user_data["email"], "password": user_data["password"]},
    )
    assert login_resp.status_code == status.HTTP_200_OK
    access_token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # setup server and key in DB
    db = SessionLocal()
    server = VPNServer(
        name="Test Server",
        ip_address="10.10.0.1",
        country_code="US",
        city="NY",
        load_ratio=0.0,
        is_blacklisted=False,
        type="wireguard",
        status="active",
        capacity=100,
    )
    db.add(server)
    db.commit()
    db.refresh(server)

    key = VPNKey(
        server_id=server.id,
        public_key="pubkey",
        private_key="privkey",
        ip_address="10.10.0.2",
        is_allocated=False,
    )
    db.add(key)
    db.commit()
    db.refresh(key)
    db.close()

    # create peer
    create_resp = await client.post(
        "/vpn/peers/",
        json={"server_id": server.id},
        headers=headers,
    )
    assert create_resp.status_code == status.HTTP_200_OK
    peer_id = create_resp.json()["id"]

    # list peers
    list_resp = await client.get("/vpn/peers/", headers=headers)
    assert list_resp.status_code == status.HTTP_200_OK
    peers = list_resp.json()
    assert any(p["id"] == peer_id for p in peers)

    # revoke peer
    del_resp = await client.delete(f"/vpn/peers/{peer_id}", headers=headers)
    assert del_resp.status_code == status.HTTP_200_OK

    # ensure peer removed
    list_resp = await client.get("/vpn/peers/", headers=headers)
    assert list_resp.status_code == status.HTTP_200_OK
    peers = list_resp.json()
    assert all(p["id"] != peer_id for p in peers)

import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_create_connection_history(client):
    # 1) Önce bir user register et (idempotent olsun)
    register_data = {
        "email": "yasarerkoca@gmail.com",
        "password": "Aa1!aa1!bb2@BB2@",
        "full_name": "yasar erkoca"
    }
    reg_resp = await client.post("/auth/register", json=register_data)
    print("REGISTER:", reg_resp.status_code, reg_resp.text)
    assert reg_resp.status_code in (status.HTTP_201_CREATED, status.HTTP_409_CONFLICT, status.HTTP_200_OK)

    # 2) Login ol
    login_data = {"email": register_data["email"], "password": register_data["password"]}
    login_resp = await client.post("/auth/login", json=login_data)
    print("LOGIN:", login_resp.status_code, login_resp.text)
    assert login_resp.status_code == 200

    login_json = login_resp.json()
    print("LOGIN RESPONSE:", login_json)
    token = login_json["access_token"]
    user_id = login_json["user_id"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3) Test için bir VPN server oluştur (Varsa atla, yoksa ekle)
    # NOT: Burayı testte DB'ye doğrudan ekleyebilirsin!
    from app.config.database import SessionLocal
    from app.models.vpn.vpn_server import VPNServer
    db = SessionLocal()
    server = db.query(VPNServer).first()
    if not server:
        server = VPNServer(
            name="Test VPN",
            ip_address="192.168.1.100",
            country_code="TR",
            city="Istanbul",
            load_ratio=0,
            is_blacklisted=False,
            type="premium",
            status="active",
            capacity=100
        )
        db.add(server)
        db.commit()
        db.refresh(server)
    server_id = server.id
    db.close()

    # 4) Bağlantı log kaydı at
    conn_data = {
        "user_id": user_id,
        "server_id": server_id,
        "ip": "192.168.1.1",
        "country_code": "TR",
        "duration": 3600,
        "success": True
    }
    conn_resp = await client.post("/vpn/connection/", json=conn_data, headers=headers)
    print("VPN CONNECTION:", conn_resp.status_code, conn_resp.text)
    assert conn_resp.status_code in (status.HTTP_201_CREATED, status.HTTP_200_OK), conn_resp.text

import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_register_and_login(client):
    data = {
        "email": "yasarerkoca@gmail.com",
        "password": "Aa1!aa1!bb2@BB2@",
        "full_name": "yasar erkoca"
    }
    resp = await client.post("/auth/register", json=data)
    print("REGISTER:", resp.status_code, resp.text)  # HATA DETAYI BURADA!
    assert resp.status_code in (status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT), resp.text

    login_data = {"email": "yasarerkoca@gmail.com", "password": "Aa1!aa1!bb2@BB2@"}
    resp = await client.post("/auth/login", json=login_data)
    print("LOGIN:", resp.status_code, resp.text)
    assert resp.status_code == 200
    token = resp.json().get("access_token")
    assert token is not None

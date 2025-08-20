import pytest
from fastapi import status
from app.utils.token import create_email_verification_token


@pytest.mark.asyncio
async def test_register_and_login(client):
    data = {
        "email": "verified@example.com",
        "password": "Aa1!aa1!bb2@BB2@",
        "full_name": "Verified User"
    }
    resp = await client.post("/auth/register", json=data)
    assert resp.status_code in (
        status.HTTP_201_CREATED,
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_409_CONFLICT,
    ), resp.text

    token = create_email_verification_token(data["email"])
    await client.get(f"/auth/verify-email?token={token}")
    login_data = {"email": data["email"], "password": data["password"]}
    resp = await client.post("/auth/login", json=login_data)
    assert resp.status_code == status.HTTP_200_OK
    token = resp.json().get("access_token")
    assert token is not None


@pytest.mark.asyncio
async def test_unverified_user_login_returns_403(client):
    data = {
        "email": "unverified@example.com",
        "password": "Aa1!aa1!bb2@BB2@",
        "full_name": "Unverified User",
    }
    resp = await client.post("/auth/register", json=data)
    assert resp.status_code in (
        status.HTTP_201_CREATED,
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_409_CONFLICT,
    ), resp.text

    login_data = {"email": data["email"], "password": data["password"]}
    resp = await client.post("/auth/login", json=login_data)
    assert resp.status_code == status.HTTP_403_FORBIDDEN

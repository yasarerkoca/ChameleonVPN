import pytest
from fastapi import status

from app.utils.token import create_email_verification_token
from app.config.database import SessionLocal
from app.models.user.user import User
from app.services.totp_service import generate_totp_secret

import pyotp


@pytest.mark.asyncio
async def test_password_hash_and_email_verification(client):
    data = {
        "email": "loginuser@example.com",
        "password": "TestPassword123!",
        "full_name": "Login User",
    }
    resp = await client.post("/auth/register", json=data)
    assert resp.status_code in (
        status.HTTP_201_CREATED,
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_409_CONFLICT,
    ), resp.text

    # wrong password should fail
    wrong = await client.post(
        "/auth/login",
        json={"email": data["email"], "password": "wrong"},
    )
    assert wrong.status_code == status.HTTP_401_UNAUTHORIZED

    # login before email verification should be forbidden
    unverified = await client.post(
        "/auth/login",
        json={"email": data["email"], "password": data["password"]},
    )
    assert unverified.status_code == status.HTTP_403_FORBIDDEN

    # verify email then login successfully
    token = create_email_verification_token(data["email"])
    await client.get(f"/auth/verify-email?token={token}")
    verified = await client.post(
        "/auth/login",
        json={"email": data["email"], "password": data["password"]},
    )
    assert verified.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_2fa_login_totp_flow(client):
    data = {
        "email": "twofa@example.com",
        "password": "StrongPass123!",
        "full_name": "Two FA",
    }
    resp = await client.post("/auth/register", json=data)
    assert resp.status_code in (
        status.HTTP_201_CREATED,
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_409_CONFLICT,
    ), resp.text
    token = create_email_verification_token(data["email"])
    await client.get(f"/auth/verify-email?token={token}")

    # prepare TOTP secret for the user
    db = SessionLocal()
    user = db.query(User).filter(User.email == data["email"]).first()
    generate_totp_secret(user, db)
    secret = user.totp_secret
    db.close()

    totp = pyotp.TOTP(secret).now()

    # correct TOTP code
    success = await client.post(
        "/auth/2fa/login-totp",
        json={"email": data["email"], "totp_code": totp},
    )
    assert success.status_code == status.HTTP_200_OK

    # wrong TOTP code
    failure = await client.post(
        "/auth/2fa/login-totp",
        json={"email": data["email"], "totp_code": "000000"},
    )
    assert failure.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_login_bruteforce_protection(client):
    data = {
        "email": "bruteforce@example.com",
        "password": "SomePass123!",
        "full_name": "Brute Force",
    }
    await client.post("/auth/register", json=data)

    # exceed brute force threshold
    for _ in range(5):
        resp = await client.post(
            "/auth/login",
            json={"email": data["email"], "password": "wrong"},
        )
        assert resp.status_code in (
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )
    resp = await client.post(
        "/auth/login",
        json={"email": data["email"], "password": "wrong"},
    )
    assert resp.status_code == status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.asyncio
async def test_rate_limit_endpoint(client):
    # endpoint limited to 5 requests per minute
    for _ in range(5):
        resp = await client.get("/test-limit")
        assert resp.status_code == status.HTTP_200_OK
    resp = await client.get("/test-limit")
    assert resp.status_code == status.HTTP_429_TOO_MANY_REQUESTS


"""Routes for two-factor authentication operations."""

from fastapi import APIRouter, Depends, Body, Response
from sqlalchemy.orm import Session

from app.utils.db.db_utils import get_db
from app.models.user.user import User
from app.schemas.user.user_base import TwoFactorVerifyRequest
from app.schemas.token.token_out import TokenOut
from app.utils.auth.auth_utils import get_current_user
from app.services.jwt_service import create_access_token, create_refresh_token
from app.services.totp_service import (
    generate_totp_secret,
    verify_twofa_code,
    verify_totp_code,
)

router = APIRouter(prefix="/auth/2fa", tags=["auth-2fa"])


@router.post("/verify", response_model=TokenOut, summary="E-posta ile gelen 2FA kodunu doğrula")
def two_factor_verify(
    data: TwoFactorVerifyRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    """E-posta/SMS ile gelen 2FA kodunu doğrula."""
    user = verify_twofa_code(db, email=data.email, code=data.code)
    response.set_cookie(key="remember_device", value="1", httponly=True)
    return {
        "access_token": create_access_token({"sub": user.email, "user_id": user.id}),
        "refresh_token": create_refresh_token({"sub": user.email, "user_id": user.id}),
        "token_type": "bearer",
    }


@router.post("/generate-totp-secret", summary="Kullanıcıya yeni TOTP secret üret (QR için)")
def generate_totp(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Yeni TOTP secret ve QR üretir, kullanıcıya döner."""
    return generate_totp_secret(current_user, db)


@router.post("/setup", summary="TOTP 2FA kurulum endpointi")
def setup_totp(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Yeni bir TOTP secret üretir ve kullanıcıya kaydeder."""
    return generate_totp_secret(current_user, db)


@router.post("/login-totp", response_model=TokenOut, summary="TOTP ile giriş yap (mobil uygulama/Google Auth)")
def login_totp(
    response: Response,
    email: str = Body(..., embed=True),
    totp_code: str = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    """Mobil TOTP (Google Authenticator) ile doğrulama."""
    user = verify_totp_code(db, email=email, totp_code=totp_code)
    response.set_cookie(key="remember_device", value="1", httponly=True)
    return {
        "access_token": create_access_token({"sub": user.email, "user_id": user.id}),
        "refresh_token": create_refresh_token({"sub": user.email, "user_id": user.id}),
        "token_type": "bearer",
    }

# ~/ChameleonVPN/backend/app/routers/auth/twofa.py

from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
from datetime import datetime
import pyotp

from app.utils.db.db_utils import get_db
from app.models.user.user import User
from app.models.security.two_factor_tokens import TwoFactorToken
from app.schemas.user.user_base import TwoFactorVerifyRequest
from app.schemas.token.token_out import TokenOut
from app.utils.auth.auth_utils import get_current_user
from app.utils.token import create_access_token, create_refresh_token

router = APIRouter(
    prefix="/auth/2fa",
    tags=["auth-2fa"]
)

@router.post("/verify", response_model=TokenOut, summary="E-posta ile gelen 2FA kodunu doğrula")
def two_factor_verify(
    data: TwoFactorVerifyRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    E-posta/SMS ile gelen 2FA kodunu doğrula. Başarılıysa is_2fa_verified=True yapar.
    """
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token_row = db.query(TwoFactorToken).filter(
        TwoFactorToken.user_id == user.id,
        TwoFactorToken.code == data.code,
        TwoFactorToken.expires_at > datetime.utcnow(),
        TwoFactorToken.used == False
    ).first()
    if not token_row:
        raise HTTPException(status_code=400, detail="Invalid or expired 2FA code")

    # 🔑 2FA başarılı: flag'i güncelle
    token_row.used = True
    user.is_2fa_verified = True
    db.commit()
    db.refresh(user)

    return {
        "access_token": create_access_token({"sub": user.email, "user_id": user.id}),
        "refresh_token": create_refresh_token({"sub": user.email, "user_id": user.id}),
        "token_type": "bearer"
    }

@router.post("/generate-totp-secret", summary="Kullanıcıya yeni TOTP secret üret (QR için)")
def generate_totp(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Yeni TOTP secret ve QR üretir, kullanıcıya döner.
    """
    secret = pyotp.random_base32()
    current_user.totp_secret = secret
    db.commit()
    otp_auth_url = pyotp.totp.TOTP(secret).provisioning_uri(
        name=current_user.email, issuer_name="ChameleonVPN"
    )
    return {"secret": secret, "otp_auth_url": otp_auth_url}

@router.post("/login-totp", response_model=TokenOut, summary="TOTP ile giriş yap (mobil uygulama/Google Auth)")
def login_totp(
    email: str = Body(..., embed=True),
    totp_code: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """
    Mobil TOTP (Google Authenticator) ile doğrulama. Başarılıysa is_2fa_verified=True yapar.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.totp_secret or not pyotp.TOTP(user.totp_secret).verify(totp_code):
        raise HTTPException(status_code=400, detail="Invalid 2FA code or user")

    # 🔑 TOTP başarılı: flag'i güncelle
    user.is_2fa_verified = True
    db.commit()
    db.refresh(user)

    return {
        "access_token": create_access_token({"sub": user.email, "user_id": user.id}),
        "refresh_token": create_refresh_token({"sub": user.email, "user_id": user.id}),
        "token_type": "bearer"
    }

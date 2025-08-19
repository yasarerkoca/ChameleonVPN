"""Utility helpers for TOTP-based two-factor authentication.

This module centralizes operations for generating TOTP secrets and verifying
both e-mail based one-time codes and TOTP codes. It also updates the related
database records such as marking tokens as used and setting the user's
``is_2fa_verified`` flag.
"""

from datetime import datetime
from typing import Dict

import pyotp
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user.user import User
from app.models.security.two_factor_tokens import TwoFactorToken


def generate_totp_secret(user: User, db: Session) -> Dict[str, str]:
    """Generate a new TOTP secret for ``user`` and persist it.

    Returns a dictionary containing the secret and a provisioning URL that can
    be used to generate a QR code for authenticator applications.
    """
    secret = pyotp.random_base32()
    user.totp_secret = secret
    db.commit()
    otp_auth_url = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.email, issuer_name="ChameleonVPN"
    )
    return {"secret": secret, "otp_auth_url": otp_auth_url}


def verify_twofa_code(db: Session, email: str, code: str) -> User:
    """Verify a single-use e-mail/SMS 2FA ``code`` for the given ``email``.

    The corresponding token is marked as used and the user's
    ``is_2fa_verified`` flag is set to ``True``.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token_row = db.query(TwoFactorToken).filter(
        TwoFactorToken.user_id == user.id,
        TwoFactorToken.code == code,
        TwoFactorToken.expires_at > datetime.utcnow(),
        TwoFactorToken.used == False,
    ).first()
    if not token_row:
        raise HTTPException(status_code=400, detail="Invalid or expired 2FA code")

    token_row.used = True
    user.is_2fa_verified = True
    db.commit()
    db.refresh(user)
    return user


def verify_totp_code(db: Session, email: str, totp_code: str) -> User:
    """Verify a TOTP code from an authenticator app for ``email``.

    On success the user's ``is_2fa_verified`` flag is updated.
    """
    user = db.query(User).filter(User.email == email).first()
    if (
        not user
        or not user.totp_secret
        or not pyotp.TOTP(user.totp_secret).verify(totp_code)
    ):
        raise HTTPException(status_code=400, detail="Invalid 2FA code or user")

    user.is_2fa_verified = True
    db.commit()
    db.refresh(user)
    return user


__all__ = ["generate_totp_secret", "verify_twofa_code", "verify_totp_code"]

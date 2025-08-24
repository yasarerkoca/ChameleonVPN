from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import pyotp

# Opsiyonel DB
try:
    from app.config.database import SessionLocal
    from app.models.user import User
except Exception:
    SessionLocal = None
    User = None

router = APIRouter(prefix="/auth/2fa", tags=["auth-2fa"])

class VerifyIn(BaseModel):
    email: EmailStr
    code: str

@router.post("/setup")
async def setup_2fa(email: EmailStr):
    secret = pyotp.random_base32()
    otpauth = pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name="ChameleonVPN")

    if SessionLocal and User:
        db = SessionLocal()
        try:
            u = db.query(User).filter(User.email == email).first()
            if not u:
                raise HTTPException(status_code=404, detail="User not found")
            u.mfa_secret = secret
            # Modeline mfa_enabled alanı eklediysen:
            if hasattr(u, "mfa_enabled"):
                u.mfa_enabled = True
            db.commit()
        finally:
            db.close()

    return {"secret": secret, "otpauth": otpauth}

@router.post("/verify")
async def verify_2fa(inp: VerifyIn):
    secret = None
    if SessionLocal and User:
        db = SessionLocal()
        try:
            u = db.query(User).filter(User.email == inp.email).first()
            if u:
                secret = getattr(u, "mfa_secret", None)
        finally:
            db.close()

    if not secret:
        raise HTTPException(status_code=400, detail="2FA not set")
    if not pyotp.TOTP(secret).verify(inp.code, valid_window=1):
        raise HTTPException(status_code=401, detail="Invalid 2FA code")

    return {"ok": True}

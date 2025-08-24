from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pyotp

try:
    from app.config.database import SessionLocal
    from app.models.user import User
except Exception:
    SessionLocal = None
    User = None

router = APIRouter(prefix="/auth/2fa", tags=["auth-2fa"])

class TotpVerifyIn(BaseModel):
    email: str
    code: str

@router.post("/setup")
async def setup_2fa(email: str):
    secret = pyotp.random_base32()
    otpauth = pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name="ChameleonVPN")

    if SessionLocal and User:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if user:
                user.mfa_secret = secret
                db.commit()
        finally:
            db.close()

    return {"secret": secret, "otpauth": otpauth}

@router.post("/verify")
async def verify_2fa(inp: TotpVerifyIn):
    secret = None
    if SessionLocal and User:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == inp.email).first()
            if user:
                secret = getattr(user, "mfa_secret", None)
        finally:
            db.close()

    if not secret:
        raise HTTPException(status_code=400, detail="2FA not configured")

    ok = pyotp.TOTP(secret).verify(inp.code, valid_window=1)
    if not ok:
        raise HTTPException(status_code=401, detail="Invalid 2FA code")

    return {"ok": True}

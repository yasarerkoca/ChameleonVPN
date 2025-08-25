from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from passlib.hash import bcrypt

from app.config.base import settings
from app.services.jwt_service import encode as jwt_encode, decode as jwt_decode
from app.services.email_verification_service import send_verification_email

# Opsiyonel DB
try:
    from app.config.database import SessionLocal
    from app.models.user import User
except Exception:
    SessionLocal = None
    User = None

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterIn(BaseModel):
    email: EmailStr
    password: str

def _base_url(req: Request) -> str:
    # APP_URL varsa onu kullan; yoksa proxy başlıklarıyla türet
    app_url = getattr(settings, "APP_URL", None)
    if app_url:
        return app_url.rstrip("/")
    scheme = req.headers.get("x-forwarded-proto", req.url.scheme)
    host = req.headers.get("host", req.url.netloc)
    return f"{scheme}://{host}"

@router.post("/register")
async def register(inp: RegisterIn, req: Request):
    token = jwt_encode({"sub": inp.email, "purpose": "email-verify"}, minutes=30)
    verify_url = f"{_base_url(req)}/auth/verify-email?token={token}"

    if SessionLocal and User:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == inp.email).first()
            if not user:
                hashed = bcrypt.hash(inp.password)
                # Modelinde password_hash alanı yoksa eklemelisin.
                user = User(
                    email=inp.email,
                    password_hash=hashed,
                    is_email_verified=False,
                )
                db.add(user)
                db.commit()
        finally:
            db.close()

    await send_verification_email(inp.email, verify_url)
    return {"ok": True}

@router.get("/verify-email")
async def verify_email(token: str):
    data = jwt_decode(token)
    if data.get("purpose") != "email-verify":
        raise HTTPException(status_code=400, detail="Invalid token")

    email = data.get("sub")
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")

    if SessionLocal and User:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if user:
                user.is_email_verified = True
                db.commit()
        finally:
            db.close()

    return {"ok": True, "email": email}

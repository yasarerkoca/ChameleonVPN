from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from app.config.base import settings

# DB importları (opsiyonel)
try:
    from app.config.database import SessionLocal
    from app.models.user import User
except Exception:
    SessionLocal = None
    User = None

# JWT servis
try:
    from app.services.jwt_service import encode as jwt_encode, decode as jwt_decode
except Exception:
    from jose import jwt
    def jwt_encode(payload: dict, minutes: int = 60):
        exp = datetime.utcnow() + timedelta(minutes=minutes)
        payload = {**payload, "exp": exp}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    def jwt_decode(token: str):
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register(inp: RegisterIn, req: Request):
    token = jwt_encode({"sub": inp.email, "purpose": "email-verify"}, minutes=30)
    verify_url = f"{req.url.scheme}://{req.url.netloc}/auth/verify-email?token={token}"

    if SessionLocal and User:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == inp.email).first()
            if not user:
                user = User(email=inp.email, is_email_verified=False)  # TODO: hash password
                db.add(user)
                db.commit()
        finally:
            db.close()

    # TODO: email_service ile gönderim
    return {"ok": True, "verify_url": verify_url}

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

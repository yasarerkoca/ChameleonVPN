from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.models.user.user import User
from app.services.jwt_service import create_access_token, create_refresh_token
from app.services.password_service import verify_password
from app.services.totp_service import verify_totp_code
from app.utils.db.db_utils import get_db


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    totp_code: str | None = None


router = APIRouter(prefix="/auth", tags=["auth-login"])


@router.post("/login", summary="Kullanıcı girişi (JWT ile)")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_email_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    if user.totp_secret:
        if not data.totp_code:
            raise HTTPException(status_code=400, detail="TOTP code required")
        verify_totp_code(db, email=user.email, totp_code=data.totp_code)

    token = create_access_token({"sub": user.email, "user_id": user.id})
    refresh = create_refresh_token({"sub": user.email, "user_id": user.id})
    return {
        "access_token": token,
        "refresh_token": refresh,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active,
    }


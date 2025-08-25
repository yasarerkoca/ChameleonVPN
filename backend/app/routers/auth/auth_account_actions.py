from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
import asyncio
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel, Field
from app.config.base import settings

from app.models.user.user import User
from app.schemas.user.user_base import UserCreate, UserLogin, UserOut
from app.schemas.token.token_refresh import TokenRefresh
from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import (
    is_strong_password,
    get_password_hash,
    verify_password,
)

from app.services.jwt_service import (
    create_access_token,
    create_refresh_token,
    create_email_verification_token,
    verify_email_verification_token,
    refresh_tokens,
)
from app.services.email_verification_service import send_verification_email

router = APIRouter(
    prefix="/auth",
    tags=["auth-account"]
)

@router.post(
    "/register",
    response_model=UserOut,
    dependencies=[Depends(RateLimiter(times=3, seconds=60))],
    summary="Yeni kullanıcı kaydı"
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None,
):
    # Eğer UserCreate'te ip isteniyorsa ekle, istemiyorsa kaldır.
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    is_strong_password(user.password)
    password_hash = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        password_hash=password_hash,
        full_name=user.full_name,
        is_active=True,
        is_email_verified=False,
        # register_ip eklemek istersen: register_ip=user.register_ip,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    verification_token = create_email_verification_token(new_user.email)
    verify_url = settings.EMAIL_VERIFY_URL + f"?token={verification_token}"
    if background_tasks:
        background_tasks.add_task(
            asyncio.create_task, send_verification_email(new_user.email, verify_url)
        )
    return new_user

@router.post("/login", summary="Kullanıcı girişi (JWT ile)")
def login(
    data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_email_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    token = create_access_token(data={"sub": user.email, "user_id": user.id})
    refresh = create_refresh_token(data={"sub": user.email, "user_id": user.id})
    return {
        "access_token": token,
        "refresh_token": refresh,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active
    }

@router.post("/logout", summary="Kullanıcı çıkışı")
def logout(data: TokenRefresh):
    """Refresh token'ı kara listeye ekleyerek çıkış yap."""
    revoke_refresh_token(data.refresh_token)
    return {"msg": "Logout successful"}

class RefreshTokenRequest(BaseModel):
    """Request body for token refresh."""

    refresh_token: str = Field(..., alias="refreshToken")

    class Config:
        allow_population_by_field_name = True

@router.post("/refresh", summary="Refresh access and refresh tokens")
def refresh_token_endpoint(payload: RefreshTokenRequest):
    tokens = refresh_tokens(payload.refresh_token)
    return tokens

@router.get("/verify-email", summary="E-posta doğrulamasını tamamla")
def verify_email(
    token: str,
    db: Session = Depends(get_db),
):
    email = verify_email_verification_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_email_verified = True
    db.commit()
    db.refresh(user)
    return {"msg": "Email verified successfully."}

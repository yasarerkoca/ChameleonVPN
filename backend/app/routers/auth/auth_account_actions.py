from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from app.models.user.user import User
from app.schemas.user.user_base import UserCreate, UserLogin, UserOut
from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import (
    is_strong_password,
    get_password_hash,
    verify_password,
)
from app.utils.token.token_utils import create_access_token, create_refresh_token

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
        is_email_verified=True,
        # register_ip eklemek istersen: register_ip=user.register_ip,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", summary="Kullanıcı girişi (JWT ile)")
def login(
    data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
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

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.db.db_utils import get_db
from app.models.user.user import User
from app.schemas.user.user_base import UserUpdate, PasswordChange, UserOut
from app.utils.auth.auth_utils import (
    verify_password,
    get_password_hash,
    is_strong_password,
    get_current_user
)

router = APIRouter(
    prefix="/auth/profile",
    tags=["auth-profile"]
)

@router.get("/me", response_model=UserOut, summary="Mevcut kullanıcı bilgilerini getir")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserOut, summary="Profil bilgilerini güncelle")
def update_me(
    update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if update.email:
        current_user.email = update.email
    if hasattr(update, "username") and update.username:
        current_user.username = update.username
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/change-password", summary="Şifreyi değiştir")
def change_password(
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    if not is_strong_password(data.new_password):
        raise HTTPException(status_code=400, detail="Weak new password")
    current_user.password_hash = get_password_hash(data.new_password)
    db.commit()
    return {"msg": "Password changed successfully."}

@router.delete("/me", summary="Hesabı devre dışı bırak")
def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.is_active = False
    db.commit()
    return {"msg": "Account deactivated."}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field

from app.models.user.user import User
from app.models.user.user_notification import UserNotification
from app.models.corporate.corporate_user_rights_history import CorporateUserRightsHistory
from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user

router = APIRouter(
    prefix="/admin/user-management",
    tags=["admin-user-management"]
)

def admin_required(current_user: User = Depends(get_current_user)):
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin yetkisi gerekli")
    return current_user

# --- Pydantic modelleri ---
class UserIdsRequest(BaseModel):
    user_ids: List[int] = Field(..., example=[1,2,3])

class AnnouncementRequest(BaseModel):
    message: str = Field(..., example="Sistem bakımı yapılacaktır.")
    target_user_ids: Optional[List[int]] = Field(None, example=[1,2,3])

# --- Kullanıcı Listele / Oluştur (opsiyonel) ---
@router.get("/users", summary="Tüm kullanıcıları listele")
def list_users(db: Session = Depends(get_db), _: User = Depends(admin_required)):
    return db.query(User).all()

# --- Kullanıcı Silme ---
@router.delete("/users/{user_id}", summary="Kullanıcıyı sil")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.add(CorporateUserRightsHistory(
        user_id=user.id,
        changed_by_admin_id=current_user.id,
        field_changed="deleted",
        old_value="active",
        new_value="deleted",
        note="Admin tarafından kullanıcı silindi"
    ))
    db.delete(user)
    db.commit()
    return {"msg": "User deleted"}

# --- MFA Zorunlu Kılma ---
@router.post("/enforce-mfa", summary="Kullanıcılarda MFA'yı zorunlu yap")
def enforce_mfa(
    payload: UserIdsRequest,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    enforced = []
    for user_id in payload.user_ids:
        user = db.query(User).get(user_id)
        if not user:
            continue
        user.mfa_enabled = True
        db.commit()
        enforced.append(user.email)
    return {"msg": f"MFA zorunlu kılındı: {enforced}"}

# --- Zorunlu Şifre Sıfırlama ---
@router.post("/force-password-reset", summary="Kullanıcılara zorunlu şifre sıfırlama uygula")
def force_password_reset(
    payload: UserIdsRequest,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    reset_required = []
    for user_id in payload.user_ids:
        user = db.query(User).get(user_id)
        if not user:
            continue
        user.reset_token = "FORCE_RESET"
        db.commit()
        reset_required.append(user.email)
    return {"msg": f"Şifre sıfırlama zorunlu kılındı: {reset_required}"}

# --- Global/Toplu Duyuru Gönderme ---
@router.post("/send-global-announcement", summary="Tüm/kısmi kullanıcılara duyuru gönder")
def send_global_announcement(
    payload: AnnouncementRequest,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    notified = []
    users = db.query(User).all() if not payload.target_user_ids else db.query(User).filter(User.id.in_(payload.target_user_ids)).all()
    for user in users:
        db.add(UserNotification(
            user_id=user.id,
            title="Sistem Duyurusu",
            message=payload.message,
            type="announcement",
            status="unread"
        ))
        notified.append(user.email)
    db.commit()
    return {"msg": f"{len(notified)} kullanıcıya duyuru gönderildi.", "users": notified}

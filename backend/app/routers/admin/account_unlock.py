from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List
from app.models.user import User
from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user_optional

router = APIRouter(
    prefix="/admin/account-unlock",
    tags=["admin-account-unlock"]
)

# 👮 Admin kontrolü
def admin_required(current_user: User = Depends(get_current_user_optional)):
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin yetkisi gerekli")
    return current_user

# 🔐 Giriş veri modeli
class UnlockRequest(BaseModel):
    user_ids: List[int] = Field(..., example=[1, 2, 3])

# 🔓 POST: Birden fazla hesabı aktif hale getir
@router.post("/", summary="Kullanıcı hesaplarını tekrar aktifleştir")
def unlock_accounts(
    payload: UnlockRequest,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    unlocked = []
    for user_id in payload.user_ids:
        user = db.query(User).get(user_id)
        if not user:
            continue
        user.status = "active"
        user.is_active = True
        db.commit()
        unlocked.append({"user_id": user.id, "email": user.email})

    return {
        "msg": f"{len(unlocked)} hesap tekrar aktifleştirildi.",
        "unlocked_users": unlocked
    }

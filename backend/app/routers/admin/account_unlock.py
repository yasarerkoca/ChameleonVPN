from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List
from app.models.user import User
from app.utils.db.db_utils import get_db
from app.deps import require_role

router = APIRouter(
    prefix="/admin/account-unlock",
    tags=["admin-account-unlock"]
)

# 🔐 Giriş veri modeli
class UnlockRequest(BaseModel):
    user_ids: List[int] = Field(..., example=[1, 2, 3])

# 🔓 POST: Birden fazla hesabı aktif hale getir
@router.post("/", summary="Kullanıcı hesaplarını tekrar aktifleştir")
def unlock_accounts(
    payload: UnlockRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin"))
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

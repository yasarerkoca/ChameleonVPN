from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field

from app.models.user.user import User
from app.models.security.limit import UserLimit
from app.models.corporate.corporate_user_group import CorporateUserGroup
from app.models.corporate.corporate_user_rights_history import CorporateUserRightsHistory
from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user_optional

router = APIRouter(
    prefix="/admin/quota",
    tags=["admin-quota"]
)

def admin_required(current_user: User = Depends(get_current_user_optional)):
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin yetkisi gerekli")
    return current_user

class QuotaRequest(BaseModel):
    quota_gb: int = Field(..., example=50, description="Kullanıcıya atanacak kota (GB)")

@router.get("/user-quotas", summary="Tüm kullanıcıların kota kayıtlarını getir")
def list_quotas(db: Session = Depends(get_db), _: User = Depends(admin_required)):
    return db.query(UserLimit).all()

@router.post("/user/{user_id}", summary="Bireysel kullanıcıya kota GB ata")
def set_user_quota(
    user_id: int,
    payload: QuotaRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    old_quota = user.proxy_quota_gb
    user.proxy_quota_gb = payload.quota_gb
    db.commit()
    db.add(CorporateUserRightsHistory(
        user_id=user.id,
        changed_by_admin_id=admin.id,
        field_changed="proxy_quota_gb",
        old_value=str(old_quota),
        new_value=str(payload.quota_gb),
        note="Kullanıcı kotası admin tarafından güncellendi"
    ))
    db.commit()
    return {"msg": f"Kullanıcı kotası {payload.quota_gb} GB olarak ayarlandı."}

@router.post("/group/{group_id}", summary="Bir gruptaki tüm kullanıcılara kota GB ata")
def set_group_quota(
    group_id: int,
    payload: QuotaRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):
    group = db.query(CorporateUserGroup).get(group_id)
    if not group or not group.users:
        raise HTTPException(status_code=404, detail="Group or users not found")
    for user in group.users:
        old_quota = user.proxy_quota_gb
        user.proxy_quota_gb = payload.quota_gb
        db.add(CorporateUserRightsHistory(
            user_id=user.id,
            changed_by_admin_id=admin.id,
            field_changed="proxy_quota_gb",
            old_value=str(old_quota),
            new_value=str(payload.quota_gb),
            note=f"Toplu kota güncellendi: {group.name}"
        ))
    db.commit()
    return {"msg": f"{group.name} grubundaki tüm kullanıcıların kotası {payload.quota_gb} GB olarak ayarlandı."}

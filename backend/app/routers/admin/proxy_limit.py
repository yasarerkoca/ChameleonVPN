from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

from app.models.user.user import User
from app.models.corporate.corporate_user_group import CorporateUserGroup
from app.models.corporate.corporate_user_rights_history import CorporateUserRightsHistory
from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user_optional

router = APIRouter(
    prefix="/admin/proxy-limit",
    tags=["admin-proxy-limit"]
)

def admin_required(current_user: User = Depends(get_current_user_optional)):
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin yetkisi gerekli")
    return current_user

class ProxyLimitRequest(BaseModel):
    count: int = Field(..., example=5, description="Aktif proxy limiti")

@router.post("/user/{user_id}", summary="Bireysel kullanıcı için proxy limiti belirle")
def set_user_proxy_count(
    user_id: int,
    payload: ProxyLimitRequest,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    old_count = user.active_proxy_count
    user.active_proxy_count = payload.count
    db.commit()
    db.add(CorporateUserRightsHistory(
        user_id=user.id,
        changed_by_admin_id=1,  # TODO: Giriş yapan admin id'sini ekle
        field_changed="active_proxy_count",
        old_value=str(old_count),
        new_value=str(payload.count),
        note="Kullanıcı aktif proxy limiti admin tarafından güncellendi"
    ))
    db.commit()
    return {"msg": f"{user.email} kullanıcısına {payload.count} adet aktif proxy limiti verildi."}

@router.post("/group/{group_id}", summary="Grup üyeleri için proxy limiti belirle")
def set_group_proxy_count(
    group_id: int,
    payload: ProxyLimitRequest,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    group = db.query(CorporateUserGroup).get(group_id)
    if not group or not group.users:
        raise HTTPException(status_code=404, detail="Group or users not found")
    for user in group.users:
        old_count = user.active_proxy_count
        user.active_proxy_count = payload.count
        db.add(CorporateUserRightsHistory(
            user_id=user.id,
            changed_by_admin_id=1,  # TODO: Giriş yapan admin id'sini ekle
            field_changed="active_proxy_count",
            old_value=str(old_count),
            new_value=str(payload.count),
            note=f"Toplu proxy limiti güncellendi: {group.name}"
        ))
    db.commit()
    return {"msg": f"{group.name} grubundaki tüm kullanıcıların proxy limiti {payload.count} olarak ayarlandı."}

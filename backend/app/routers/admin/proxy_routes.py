from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, Field

from app.utils.db.db_utils import get_db
from app.models.user.user import User
from app.models.proxy.proxy_ip import ProxyIP
from app.models.proxy.proxy_usage_log import ProxyUsageLog
from app.models.proxy.user_proxy_assignment import UserProxyAssignment
from app.models.corporate.corporate_user_group import CorporateUserGroup
from app.models.corporate.corporate_user_rights_history import CorporateUserRightsHistory
from app.deps import require_role

router = APIRouter(
    prefix="/admin/proxy",
    tags=["admin-proxy"]
)

# ----------------------------- MODELLER -----------------------------
class ProxyAssignRequest(BaseModel):
    user_id: int = Field(..., example=2)
    proxy_id: int = Field(..., example=4)

class QuotaRequest(BaseModel):
    quota_gb: int = Field(..., example=50)
# ----------------------- PROXY IP YÖNETİMİ --------------------------
@router.post("/add", summary="Yeni proxy IP ekle")
def add_proxy(
    ip_address: str = Query(..., example="192.168.1.100"),
    location: str = Query("", example="Almanya"),
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin"))
):
    proxy = ProxyIP(ip_address=ip_address, location=location)
    db.add(proxy)
    db.commit()
    return {"msg": f"Proxy IP {ip_address} eklendi."}

@router.get("/list", summary="Tüm proxy IP'lerini listele")
def list_proxies(db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    return db.query(ProxyIP).all()

@router.delete("/delete/{proxy_id}", summary="Proxy IP sil")
def delete_proxy(proxy_id: int, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    proxy = db.query(ProxyIP).get(proxy_id)
    if not proxy:
        raise HTTPException(status_code=404, detail="Proxy bulunamadı")
    db.delete(proxy)
    db.commit()
    return {"msg": "Proxy silindi."}

# --------------------- KULLANICIYA PROXY ATAMA ----------------------

@router.post("/assign", summary="Kullanıcıya proxy ata")
def assign_proxy(
    payload: ProxyAssignRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin"))
):
    assignment = UserProxyAssignment(user_id=payload.user_id, proxy_id=payload.proxy_id)
    db.add(assignment)
    db.commit()
    return {"msg": f"Proxy {payload.proxy_id}, kullanıcı {payload.user_id}'ye atandı."}

# --------------------- PROXY KULLANIM LOG'LARI ----------------------

@router.get("/usage-logs", summary="Tüm proxy kullanım loglarını getir")
def list_proxy_usage_logs(db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    return db.query(ProxyUsageLog).order_by(ProxyUsageLog.timestamp.desc()).all()

@router.get("/usage/search", summary="Proxy kullanım geçmişi ara")
def search_proxy_usage(
    user_id: Optional[int] = None,
    proxy_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin"))
):
    query = db.query(ProxyUsageLog)
    if user_id:
        query = query.filter(ProxyUsageLog.user_id == user_id)
    if proxy_id:
        query = query.filter(ProxyUsageLog.proxy_id == proxy_id)
    if start_date:
        query = query.filter(ProxyUsageLog.timestamp >= start_date)
    if end_date:
        query = query.filter(ProxyUsageLog.timestamp <= end_date)
    return query.order_by(ProxyUsageLog.timestamp.desc()).all()

# -------------------------- KOTA YÖNETİMİ ---------------------------

@router.post("/set-user-quota/{user_id}", summary="Kullanıcıya proxy kota GB ayarla")
def set_user_quota(
    user_id: int,
    payload: QuotaRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    old_quota = user.proxy_quota_gb
    user.proxy_quota_gb = payload.quota_gb
    db.commit()
    db.add(CorporateUserRightsHistory(
        user_id=user.id,
        changed_by_admin_id=current_user.id,
        field_changed="proxy_quota_gb",
        old_value=str(old_quota),
        new_value=str(payload.quota_gb),
        note="Kullanıcı kotası admin tarafından güncellendi"
    ))
    db.commit()
    return {"msg": f"Kullanıcı kotası {payload.quota_gb} GB olarak ayarlandı."}

@router.post("/set-group-quota/{group_id}", summary="Grup kullanıcılarına toplu proxy kota GB ayarla")
def set_group_quota(
    group_id: int,
    payload: QuotaRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    group = db.query(CorporateUserGroup).get(group_id)
    if not group or not group.users:
        raise HTTPException(status_code=404, detail="Group or users not found")
    for user in group.users:
        old_quota = user.proxy_quota_gb
        user.proxy_quota_gb = payload.quota_gb
        db.add(CorporateUserRightsHistory(
            user_id=user.id,
            changed_by_admin_id=current_user.id,
            field_changed="proxy_quota_gb",
            old_value=str(old_quota),
            new_value=str(payload.quota_gb),
            note=f"Toplu kota güncellendi: {group.name}"
        ))
    db.commit()
    return {"msg": f"{group.name} grubundaki tüm kullanıcıların kotası {payload.quota_gb} GB olarak ayarlandı."}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.utils.db.db_utils import get_db
from app.models.security.blocked_ip_range import BlockedIPRange
from app.crud.security.blocked_ip_range_crud import (
    add_blocked_ip_range, get_all_blocked_ip_ranges, remove_blocked_ip_range
)
from app.utils.auth.auth_utils import get_current_user_optional
from pydantic import BaseModel

router = APIRouter(
    prefix="/admin/ip-range",
    tags=["admin-ip-range"]
)

def admin_required(current_user = Depends(get_current_user_optional)):
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin yetkisi gerekli")
    return current_user

class IPRangeAddRequest(BaseModel):
    cidr: str
    reason: str = ""

@router.get("/", summary="Tüm engelli IP aralıklarını getir")
def list_ip_ranges(db: Session = Depends(get_db), _ = Depends(admin_required)):
    return get_all_blocked_ip_ranges(db)

@router.post("/add", summary="Yeni CIDR IP aralığı ekle")
def add_ip_range(payload: IPRangeAddRequest, db: Session = Depends(get_db), _ = Depends(admin_required)):
    return add_blocked_ip_range(db, payload.cidr, payload.reason)

@router.delete("/delete/{cidr}", summary="CIDR IP aralığını sil")
def delete_ip_range(cidr: str, db: Session = Depends(get_db), _ = Depends(admin_required)):
    remove_blocked_ip_range(db, cidr)
    return {"msg": f"{cidr} IP aralığı kaldırıldı."}

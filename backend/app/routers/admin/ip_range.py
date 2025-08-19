from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.utils.db.db_utils import get_db
from app.models.security.blocked_ip_range import BlockedIPRange
from app.crud.security.blocked_ip_range_crud import (
    add_blocked_ip_range, get_all_blocked_ip_ranges, remove_blocked_ip_range
)
from app.deps import require_role
from pydantic import BaseModel

router = APIRouter(
    prefix="/admin/ip-range",
    tags=["admin-ip-range"]
)

class IPRangeAddRequest(BaseModel):
    cidr: str
    reason: str = ""

@router.get("/", summary="Tüm engelli IP aralıklarını getir")
def list_ip_ranges(db: Session = Depends(get_db), _ = Depends(require_role("admin"))):
    return get_all_blocked_ip_ranges(db)

@router.post("/add", summary="Yeni CIDR IP aralığı ekle")
def add_ip_range(payload: IPRangeAddRequest, db: Session = Depends(get_db), _ = Depends(require_role("admin"))):
    return add_blocked_ip_range(db, payload.cidr, payload.reason)

@router.delete("/delete/{cidr}", summary="CIDR IP aralığını sil")
def delete_ip_range(cidr: str, db: Session = Depends(get_db), _ = Depends(require_role("admin"))):
    remove_blocked_ip_range(db, cidr)
    return {"msg": f"{cidr} IP aralığı kaldırıldı."}

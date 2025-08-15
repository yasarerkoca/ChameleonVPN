from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field

from app.models.security.blocked_ip import BlockedIP
from app.models.user.user import User
from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user_optional

router = APIRouter(
    prefix="/admin/security-controls",
    tags=["admin-security-controls"]
)

def admin_required(current_user: User = Depends(get_current_user_optional)):
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin yetkisi gerekli")
    return current_user

class IPBlockRequest(BaseModel):
    ip: str = Field(..., example="192.168.1.100")
    reason: Optional[str] = Field("admin block", example="Geçici engelleme.")
    minutes: Optional[int] = Field(1440, description="Blok süresi (dakika)")

@router.post("/block-ip", summary="IP adresi engelle")
def block_ip(
    payload: IPBlockRequest,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    from datetime import datetime, timedelta
    expire_time = datetime.utcnow() + timedelta(minutes=payload.minutes)
    db.add(BlockedIP(ip_address=payload.ip, reason=payload.reason, ban_until=expire_time))
    db.commit()
    return {"msg": f"{payload.ip} adresi {payload.minutes} dk boyunca engellendi."}

@router.get("/blocked-ips", summary="Engellenmiş IP'leri listele")
def list_blocked_ips(db: Session = Depends(get_db), _: User = Depends(admin_required)):
    return db.query(BlockedIP).order_by(BlockedIP.ban_until.desc()).all()

@router.delete("/unblock-ip/{ip}", summary="IP engelini kaldır")
def unblock_ip(ip: str, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    entry = db.query(BlockedIP).filter(BlockedIP.ip_address == ip).first()
    if not entry:
        raise HTTPException(status_code=404, detail="IP engeli bulunamadı.")
    db.delete(entry)
    db.commit()
    return {"msg": f"{ip} engeli kaldırıldı."}

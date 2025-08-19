from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.proxy.proxy_ip import ProxyIP
from app.models.security.blocked_ip import BlockedIP
from app.models.user.user import User
from app.utils.db.db_utils import get_db
from app.deps import require_role
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/admin/ip-block",
    tags=["admin-ip-block"]
)

# -------------------- MODELLER ---------------------
class IPBlockRequest(BaseModel):
    ip_addresses: List[str] = Field(..., example=["192.168.1.1", "10.0.0.2"])
    reason: Optional[str] = Field("admin block", example="admin block")
    minutes: Optional[int] = Field(1440, description="Blok süresi (dakika cinsinden)")

class ProxyBlockRequest(BaseModel):
    proxy_ids: List[int] = Field(..., example=[1, 2, 3])

# -------------------- ENDPOINTS --------------------

@router.post("/block-ips", summary="IP adreslerini bloke et")
def block_ips(
    payload: IPBlockRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin"))
):
    blocked = []
    expire_time = datetime.utcnow() + timedelta(minutes=payload.minutes)
    for ip in payload.ip_addresses:
        # Zaten banlı mı kontrol et
        existing = db.query(BlockedIP).filter(
            BlockedIP.ip_address == ip,
            BlockedIP.ban_until > datetime.utcnow()
        ).first()
        if existing:
            continue
        db.add(BlockedIP(ip_address=ip, reason=payload.reason, ban_until=expire_time))
        blocked.append(ip)
    db.commit()
    return {"msg": f"{len(blocked)} IP adresi bloklandı.", "ips": blocked}

@router.post("/block-proxies", summary="Proxy'leri bloke et")
def block_proxies(
    payload: ProxyBlockRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin"))
):
    blocked = []
    proxies = db.query(ProxyIP).filter(ProxyIP.id.in_(payload.proxy_ids)).all()
    for proxy in proxies:
        proxy.status = "blocked"
        blocked.append(proxy.ip_address)
    db.commit()
    return {"msg": f"{len(blocked)} proxy bloklandı.", "proxies": blocked}

@router.get("/list", summary="Banlı IP adreslerini getir")
def list_blocked_ips(
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin"))
):
    result = db.query(BlockedIP).all()
    return [
        {
            "ip_address": x.ip_address,
            "reason": x.reason,
            "ban_until": x.ban_until,
            "blocked_at": x.blocked_at
        }
        for x in result
    ]

@router.delete("/unban/{ip}", summary="Banı kaldır (unban)")
def unban_ip(
    ip: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin"))
):
    rec = db.query(BlockedIP).filter(BlockedIP.ip_address == ip).first()
    if not rec:
        raise HTTPException(status_code=404, detail="IP zaten banlı değil")
    db.delete(rec)
    db.commit()
    return {"msg": f"{ip} için ban kaldırıldı"}

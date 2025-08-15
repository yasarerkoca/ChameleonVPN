from sqlalchemy.orm import Session
from app.models.security.blocked_ip import BlockedIP
from datetime import datetime, timedelta

def is_ip_blocked(db: Session, ip: str) -> bool:
    blocked = db.query(BlockedIP).filter(
        BlockedIP.ip_address == ip,
        BlockedIP.ban_until > datetime.utcnow()
    ).first()
    return bool(blocked)

def block_ip(db: Session, ip: str, reason: str, minutes: int = 60):
    ban_until = datetime.utcnow() + timedelta(minutes=minutes)
    blocked = BlockedIP(ip_address=ip, reason=reason, ban_until=ban_until)
    db.add(blocked)
    db.commit()

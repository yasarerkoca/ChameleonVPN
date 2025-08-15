# ~/ChameleonVPN/backend/app/crud/security/blocked_ip_range_crud.py

from sqlalchemy.orm import Session
from app.models.security.blocked_ip_range import BlockedIPRange

def add_blocked_ip_range(db: Session, cidr: str, reason: str = ""):
    obj = BlockedIPRange(cidr=cidr, reason=reason)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def remove_blocked_ip_range(db: Session, cidr: str):
    db.query(BlockedIPRange).filter(BlockedIPRange.cidr == cidr).delete()
    db.commit()

def get_all_blocked_ip_ranges(db: Session):
    return db.query(BlockedIPRange).all()

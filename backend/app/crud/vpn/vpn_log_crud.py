from sqlalchemy.orm import Session
from app.models.vpn.vpn_log import VPNLog
from app.schemas.vpn.vpn_config import VPNLogCreate
from typing import List


def create_vpn_log(db: Session, log_data: VPNLogCreate) -> VPNLog:
    log = VPNLog(**log_data.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_user_vpn_logs(db: Session, user_id: int) -> List[VPNLog]:
    return db.query(VPNLog).filter(
        VPNLog.user_id == user_id
    ).order_by(VPNLog.connected_at.desc()).all()

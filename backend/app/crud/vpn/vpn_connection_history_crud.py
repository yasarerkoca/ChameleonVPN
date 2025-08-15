from sqlalchemy.orm import Session
from app.models.vpn.vpn_connection_history import VPNConnectionHistory
from app.schemas.vpn.vpn_connection_history import VPNConnectionHistoryCreate

def create_vpn_connection_log(db: Session, log_data: VPNConnectionHistoryCreate) -> VPNConnectionHistory:
    log = VPNConnectionHistory(**log_data.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_user_vpn_history(db: Session, user_id: int):
    return db.query(VPNConnectionHistory).filter_by(user_id=user_id).order_by(VPNConnectionHistory.connected_at.desc()).all()

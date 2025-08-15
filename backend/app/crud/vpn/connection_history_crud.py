from sqlalchemy.orm import Session
from app.models.vpn.vpn_connection_history import VPNConnectionHistory
from app.schemas.vpn.vpn_connection_history import VPNConnectionHistoryCreate
from datetime import datetime

def create_connection_log(db: Session, data: VPNConnectionHistoryCreate) -> VPNConnectionHistory:
    log = VPNConnectionHistory(**data.dict(), connected_at=datetime.utcnow())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_user_connection_history(db: Session, user_id: int):
    return db.query(VPNConnectionHistory).filter(VPNConnectionHistory.user_id == user_id).all()

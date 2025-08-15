from sqlalchemy.orm import Session
from app.models.vpn.connection_attempt import ConnectionAttempt
from app.schemas.vpn.vpn_config import ConnectionAttemptCreate
from typing import List


def log_connection_attempt(db: Session, attempt_data: ConnectionAttemptCreate) -> ConnectionAttempt:
    attempt = ConnectionAttempt(**attempt_data.dict())
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


def get_user_connection_attempts(db: Session, user_id: int) -> List[ConnectionAttempt]:
    return db.query(ConnectionAttempt).filter(
        ConnectionAttempt.user_id == user_id
    ).order_by(ConnectionAttempt.timestamp.desc()).all()

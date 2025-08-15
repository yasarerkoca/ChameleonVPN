from sqlalchemy.orm import Session
from app.models.security.user_blocklist import UserBlocklist


def block_user(db: Session, user_id: int, reason: str):
    record = UserBlocklist(user_id=user_id, reason=reason)
    db.add(record)
    db.commit()
    return record


def is_user_blocked(db: Session, user_id: int):
    return db.query(UserBlocklist).filter_by(user_id=user_id).first() is not None

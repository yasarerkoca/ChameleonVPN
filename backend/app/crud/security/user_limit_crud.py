from sqlalchemy.orm import Session
from app.models.security.limit import UserLimit


def get_user_limit(db: Session, user_id: int):
    return db.query(UserLimit).filter(UserLimit.user_id == user_id).first()


def set_user_limit(db: Session, limit: UserLimit):
    db.add(limit)
    db.commit()
    db.refresh(limit)
    return limit

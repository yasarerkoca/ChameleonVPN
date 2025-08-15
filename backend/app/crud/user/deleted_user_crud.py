from sqlalchemy.orm import Session
from app.models.user.deleted_user import DeletedUser
from datetime import datetime


def log_deleted_user(db: Session, user_id: int, email: str, deleted_by: str = "system") -> DeletedUser:
    record = DeletedUser(
        user_id=user_id,
        email=email,
        deleted_by=deleted_by,
        deleted_at=datetime.utcnow()
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_deleted_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DeletedUser).order_by(DeletedUser.deleted_at.desc()).offset(skip).limit(limit).all()

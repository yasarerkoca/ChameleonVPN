from sqlalchemy.orm import Session
from app.models.user.user_server_activity import UserServerActivity
from app.schemas.user.user_meta import ServerActivityCreate
from typing import List


def log_user_server_activity(db: Session, data: ServerActivityCreate) -> UserServerActivity:
    activity = UserServerActivity(**data.dict())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def get_user_server_activities(db: Session, user_id: int) -> List[UserServerActivity]:
    return db.query(UserServerActivity).filter(UserServerActivity.user_id == user_id).order_by(
        UserServerActivity.timestamp.desc()
    ).all()


def get_last_server_activity(db: Session, user_id: int) -> UserServerActivity | None:
    return db.query(UserServerActivity).filter(UserServerActivity.user_id == user_id).order_by(
        UserServerActivity.timestamp.desc()
    ).first()

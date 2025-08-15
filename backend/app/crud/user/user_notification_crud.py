from sqlalchemy.orm import Session
from app.models.user.user_notification import UserNotification
from app.schemas.user.user_meta import NotificationCreate
from typing import List


def create_notification(db: Session, notification: NotificationCreate) -> UserNotification:
    db_notification = UserNotification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def get_user_notifications(db: Session, user_id: int, unread_only: bool = False) -> List[UserNotification]:
    query = db.query(UserNotification).filter(UserNotification.user_id == user_id)
    if unread_only:
        query = query.filter(UserNotification.is_read == False)
    return query.order_by(UserNotification.created_at.desc()).all()


def mark_notification_as_read(db: Session, notification_id: int) -> UserNotification | None:
    notification = db.query(UserNotification).filter(UserNotification.id == notification_id).first()
    if not notification:
        return None
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification


def delete_notification(db: Session, notification_id: int) -> bool:
    notification = db.query(UserNotification).filter(UserNotification.id == notification_id).first()
    if not notification:
        return False
    db.delete(notification)
    db.commit()
    return True

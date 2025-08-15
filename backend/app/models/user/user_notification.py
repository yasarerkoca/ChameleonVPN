# ~/ChameleonVPN/backend/app/models/user/user_notification.py

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserNotification(Base):
    __tablename__ = "user_notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    title = Column(String(128), nullable=True)
    message = Column(Text, nullable=False)
    type = Column(String(64), default="info")            # info, warning, alert, etc.
    status = Column(String(32), default="unread")        # unread, read, archived
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<UserNotification user_id={self.user_id} type={self.type} status={self.status}>"

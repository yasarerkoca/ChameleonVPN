# ~/ChameleonVPN/backend/app/models/user/user_notification.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base


class UserNotification(Base):
    __tablename__ = "user_notifications"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Şema farklıysa bu alanlar opsiyoneldir (nullable=True); DB kolonlarıyla uyuşuyorsa kullanılır.
    title = Column(String(200), nullable=True)
    message = Column(String(1000), nullable=True)
    type = Column(String(32), nullable=True)

    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # ÇAKIŞMAYI ÖNLEME: backref yerine back_populates kullanıyoruz
    user = relationship("User", back_populates="notifications")

    def __repr__(self) -> str:
        return f"<UserNotification id={self.id} user_id={self.user_id} read={self.is_read}>"

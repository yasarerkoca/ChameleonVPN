# ~/ChameleonVPN/backend/app/models/user/user_activity_log.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base

class UserActivityLog(Base):
    __tablename__ = "user_activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    activity_type = Column(String(64), nullable=False)      # Örn: login, logout, update_profile
    detail = Column(String(256), nullable=True)              # Ek bilgi (örn: IP, endpoint, değişiklik)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship('User', backref='activity_logs')

    def __repr__(self):
        return f"<UserActivityLog user_id={self.user_id}, type={self.activity_type}>"

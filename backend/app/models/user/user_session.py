# ~/ChameleonVPN/backend/app/models/user/user_session.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    session_token = Column(String(128), unique=True, nullable=False)
    status = Column(String(32), default="active")  # active, ended, expired, revoked

    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)

    ip_address = Column(String(45), nullable=True)
    device_info = Column(String(256), nullable=True)

    user = relationship('User', backref='sessions')

    def __repr__(self):
        return f"<UserSession user_id={self.user_id} status={self.status}>"

# ~/ChameleonVPN/backend/app/models/user/user_server_activity.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserServerActivity(Base):
    __tablename__ = "user_server_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    server_ip = Column(String(64), nullable=False)
    activity_type = Column(String(64), nullable=False)  # connect, disconnect, fail, etc.
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    details = Column(String(256), nullable=True)

    user = relationship("User", back_populates="activities")

    def __repr__(self):
        return f"<UserServerActivity user_id={self.user_id} server_ip={self.server_ip} type={self.activity_type}>"

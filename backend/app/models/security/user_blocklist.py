# ~/ChameleonVPN/backend/app/models/security/user_blocklist.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserBlocklist(Base):
    __tablename__ = "user_blocklist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    reason = Column(String(256), nullable=True)
    blocked_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="blocklist")

    def __repr__(self):
        return f"<UserBlocklist user_id={self.user_id}, reason={self.reason}>"

# ~/ChameleonVPN/backend/app/models/security/api_key.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class APIKey(Base):
    from sqlalchemy import Column, Integer, ForeignKey
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(128), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="api_keys")

    def __repr__(self):
        return f"<APIKey id={self.id}, user_id={self.user_id}, revoked={self.revoked}>"

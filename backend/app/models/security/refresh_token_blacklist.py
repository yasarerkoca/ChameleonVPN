# ~/ChameleonVPN/backend/app/models/security/refresh_token_blacklist.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.config.database import Base

class RefreshTokenBlacklist(Base):
    __tablename__ = "refresh_token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(512), unique=True, nullable=False)  # JWT Refresh token
    blacklisted_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<RefreshTokenBlacklist token={self.token[:10]}...>"

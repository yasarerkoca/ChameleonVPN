# ~/ChameleonVPN/backend/app/models/security/blocked_ip.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.config.database import Base

class BlockedIP(Base):
    __tablename__ = "blocked_ips"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(64), unique=True, nullable=False)   # Engellenen IP
    reason = Column(String(256), nullable=True)                    # Açıklama
    ban_until = Column(DateTime, nullable=False)                   # Ban süresi
    blocked_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<BlockedIP ip_address={self.ip_address}>"

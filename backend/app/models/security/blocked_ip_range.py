# ~/ChameleonVPN/backend/app/models/security/blocked_ip_range.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.config.database import Base

class BlockedIPRange(Base):
    __tablename__ = "blocked_ip_ranges"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    cidr = Column(String(64), nullable=False, unique=True)  # örn: "10.0.0.0/8"
    reason = Column(String(256), nullable=True, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<BlockedIPRange {self.cidr}>"

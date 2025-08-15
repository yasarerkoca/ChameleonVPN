from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.config.database import Base

class BlockedIPRange(Base):
    __tablename__ = "blocked_ip_ranges"

    id = Column(Integer, primary_key=True, index=True)
    cidr = Column(String(64), nullable=False, unique=True)
    reason = Column(String(256), nullable=True, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

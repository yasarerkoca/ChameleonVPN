from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.config.database import Base

class Peer(Base):
    __tablename__ = "peers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    public_key = Column(String(255), nullable=False, unique=True)
    assigned_ip = Column(String(64), nullable=True, unique=True)
    allowed_ips = Column(String(255), nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    revoked_at = Column(DateTime(timezone=True), nullable=True)

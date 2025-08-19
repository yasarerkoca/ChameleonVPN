from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base


class VPNKey(Base):
    __tablename__ = "vpn_keys"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer, ForeignKey("vpn_servers.id"), nullable=False, index=True)
    public_key = Column(String(256), unique=True, nullable=False)
    private_key = Column(String(256), nullable=False)
    ip_address = Column(String(64), unique=True, nullable=False)
    is_allocated = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    peer = relationship("VPNPeer", back_populates="key", uselist=False)

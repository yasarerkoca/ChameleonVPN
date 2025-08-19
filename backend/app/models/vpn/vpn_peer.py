from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base


class VPNPeer(Base):
    __tablename__ = "vpn_peers"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    server_id = Column(Integer, ForeignKey("vpn_servers.id"), nullable=False, index=True)
    key_id = Column(Integer, ForeignKey("vpn_keys.id"), nullable=False, unique=True)
    ip_address = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    # relationships
    key = relationship("VPNKey", back_populates="peer")
    user = relationship("User", backref="vpn_peers")
    server = relationship("VPNServer", backref="vpn_peers")

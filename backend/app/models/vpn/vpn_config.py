# ~/ChameleonVPN/backend/app/models/vpn/vpn_config.py
from sqlalchemy import Column, Integer, ForeignKey, JSON, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.config.database import Base

class VPNConfig(Base):
    __tablename__ = "vpn_configs"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer, ForeignKey("vpn_servers.id", ondelete="CASCADE"), nullable=False, index=True)
    config = Column(JSON, nullable=True)      # genel ayarlar
    wg_quick = Column(Text, nullable=True)    # opsiyonel wg-quick içerik
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    server = relationship("VPNServer", back_populates="config")

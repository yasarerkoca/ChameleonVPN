# ~/ChameleonVPN/backend/app/models/vpn/vpn_config.py

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class VPNConfig(Base):
    __tablename__ = "vpn_configs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    server_id = Column(Integer, ForeignKey("vpn_servers.id"), nullable=False)
    config = Column(Text, nullable=False)

    # İlişkiler (isteğe bağlı)
    user = relationship("User", back_populates="vpn_configs")
    server = relationship("VPNServer", back_populates="vpn_configs")

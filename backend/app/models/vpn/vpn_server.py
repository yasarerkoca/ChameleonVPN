# ~/ChameleonVPN/backend/app/models/vpn/vpn_server.py

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class VPNServer(Base):
    __tablename__ = "vpn_servers"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    ip_address = Column(String(64), nullable=False, unique=True)
    country_code = Column(String(8), nullable=True)
    city = Column(String(64), nullable=True)

    # AI yönlendirme için metrikler
    load_ratio = Column(Float, nullable=True)              # % yük
    last_ping = Column(Integer, nullable=True)             # ms
    is_blacklisted = Column(Boolean, default=False)        # AI kara liste

    type = Column(String(32), nullable=False)              # openvpn, wireguard vs.
    status = Column(String(16), default="active")
    capacity = Column(Integer, default=100)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    vpn_configs = relationship("VPNConfig", back_populates="server")  # Mevcut durum doğru

    # ilişkiler
    logs = relationship("VPNLog", back_populates="vpn_server")
    connections = relationship("ConnectionAttempt", back_populates="vpn_server")

    def __repr__(self):
        return f"<VPNServer {self.name} ({self.ip_address}) – {self.type}>"

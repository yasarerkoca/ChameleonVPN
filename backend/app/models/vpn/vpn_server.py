# ~/ChameleonVPN/backend/app/models/vpn/vpn_server.py

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base


class VPNServer(Base):
    __tablename__ = "vpn_servers"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    ip_address = Column(String(64), nullable=False, unique=True, index=True)
    country_code = Column(String(8), nullable=True)
    city = Column(String(64), nullable=True)

    # AI yönlendirme metrikleri
    load_ratio = Column(Float, nullable=True)       # %
    last_ping = Column(Integer, nullable=True)      # ms
    is_blacklisted = Column(Boolean, default=False)

    type = Column(String(32), nullable=False)       # openvpn, wireguard, ...
    status = Column(String(16), default="active", index=True)
    capacity = Column(Integer, default=100)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # İlişkiler
    vpn_configs = relationship(
        "VPNConfig",
        back_populates="server",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # Aşağıdaki overlaps argümanları; eski modellerin backref adları (vpn_logs, connection_attempts)
    # ile bu sınıftaki adların (logs, connections) çakışma uyarılarını giderir.
    logs = relationship(
        "VPNLog",
        back_populates="vpn_server",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
        overlaps="vpn_logs",
    )

    connections = relationship(
        "ConnectionAttempt",
        back_populates="vpn_server",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
        overlaps="connection_attempts",
    )

    def __repr__(self):
        return f"<VPNServer id={self.id} name={self.name} ip={self.ip_address} type={self.type}>"

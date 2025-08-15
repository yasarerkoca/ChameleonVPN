# ~/ChameleonVPN/backend/app/models/proxy/proxy_ip.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class ProxyIP(Base):
    __tablename__ = "proxy_ips"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(64), nullable=False, unique=True)  # IPv4 / IPv6
    port = Column(Integer, nullable=False)
    country = Column(String(64), nullable=True)                   # GeoIP ülke bilgisi
    total_quota_mb = Column(BigInteger, default=0)                # Maksimum kota (MB)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # İlişkiler
    usage_logs = relationship("ProxyUsageLog", back_populates="proxy", cascade="all, delete-orphan")
    assignments = relationship("UserProxyAssignment", back_populates="proxy", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ProxyIP {self.ip_address}:{self.port} - Active={self.is_active}>"

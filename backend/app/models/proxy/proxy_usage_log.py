# ~/ChameleonVPN/backend/app/models/proxy/proxy_usage_log.py

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class ProxyUsageLog(Base):
    __tablename__ = "proxy_usage_logs"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    proxy_id = Column(Integer, ForeignKey("proxy_ips.id", ondelete="CASCADE"), nullable=False)

    used_mb = Column(BigInteger, default=0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    note = Column(String(256), nullable=True)

    # İlişkiler
    proxy = relationship("ProxyIP", back_populates="usage_logs")
    user = relationship("User", back_populates="proxy_usage_logs")

    def __repr__(self):
        return f"<ProxyUsageLog user_id={self.user_id}, used_mb={self.used_mb}>"

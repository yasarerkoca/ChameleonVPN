# ~/ChameleonVPN/backend/app/models/proxy/user_proxy_assignment.py

from sqlalchemy import Column, Integer, BigInteger, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserProxyAssignment(Base):
    __tablename__ = "user_proxy_assignments"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    proxy_id = Column(Integer, ForeignKey("proxy_ips.id", ondelete="CASCADE"), nullable=False)

    assigned_quota_mb = Column(BigInteger, default=0)
    assigned_until = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # İlişkiler
    user = relationship('User', backref='proxy_assignments')
    proxy = relationship("ProxyIP", back_populates="assignments")

    def __repr__(self):
        return f"<UserProxyAssignment user_id={self.user_id}, proxy_id={self.proxy_id}, active={self.is_active}>"

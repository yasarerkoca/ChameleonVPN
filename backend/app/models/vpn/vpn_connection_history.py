# ~/ChameleonVPN/backend/app/models/vpn/vpn_connection_history.py

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.config.database import Base

class VPNConnectionHistory(Base):
    __tablename__ = "vpn_connection_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    server_id = Column(Integer, ForeignKey("vpn_servers.id"), nullable=False)
    ip = Column(String(64), nullable=False)
    country_code = Column(String(8), nullable=True)
    duration = Column(Integer, nullable=True)
    success = Column(Boolean, default=True)  # testte kullanılıyor!
    connected_at = Column(DateTime(timezone=True), server_default=func.now())
    disconnected_at = Column(DateTime(timezone=True), nullable=True)

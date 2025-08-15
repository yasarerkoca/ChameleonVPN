# ~/ChameleonVPN/backend/app/models/vpn/vpn_log.py

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class VPNLog(Base):
    __tablename__ = "vpn_logs"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    server_id = Column(Integer, ForeignKey("vpn_servers.id", ondelete="SET NULL"))

    connected_at = Column(DateTime(timezone=True), server_default=func.now())
    disconnected_at = Column(DateTime(timezone=True), nullable=True)

    traffic_sent_mb = Column(Integer, default=0)
    traffic_received_mb = Column(Integer, default=0)

    user = relationship("User", backref="vpn_logs")
    vpn_server = relationship("VPNServer", backref="vpn_logs")

    def __repr__(self):
        return f"<VPNLog user_id={self.user_id} server_id={self.server_id} sent={self.traffic_sent_mb}MB>"

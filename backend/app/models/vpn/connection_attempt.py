# ~/ChameleonVPN/backend/app/models/vpn/connection_attempt.py

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base

class ConnectionAttempt(Base):
    __tablename__ = "connection_attempts"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    server_id = Column(Integer, ForeignKey("vpn_servers.id", ondelete="SET NULL"))

    attempt_time = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(16), nullable=False)  # success, fail
    reason = Column(Text, nullable=True)

    # ilişkiler
    user = relationship("User", backref="connection_attempts")
    vpn_server = relationship("VPNServer", backref="connection_attempts")

    def __repr__(self):
        return f"<ConnectionAttempt user_id={self.user_id} server_id={self.server_id} status={self.status}>"

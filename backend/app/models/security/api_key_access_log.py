# ~/ChameleonVPN/backend/app/models/security/api_key_access_log.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class APIKeyAccessLog(Base):
    __tablename__ = "api_key_access_logs"

    id = Column(Integer, primary_key=True, index=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id", ondelete="SET NULL"), nullable=True)

    access_time = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String(64), nullable=True)         # Erişen IP adresi
    endpoint = Column(String(128), nullable=True)          # Erişilen endpoint (örn. /admin/users)

    api_key = relationship("APIKey", backref="access_logs")

    def __repr__(self):
        return f"<APIKeyAccessLog api_key_id={self.api_key_id}, endpoint={self.endpoint}>"

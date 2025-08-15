# ~/ChameleonVPN/backend/app/models/security/failed_login_attempt.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.config.database import Base

class FailedLoginAttempt(Base):
    __tablename__ = "failed_login_attempts"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(64), nullable=False, index=True)
    email = Column(String(256), nullable=True, index=True)  # Sadece email
    attempt_time = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return f"<FailedLoginAttempt ip={self.ip_address} email={self.email}>"

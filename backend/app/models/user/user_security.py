# ~/ChameleonVPN/backend/app/models/user/user_security.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserSecurity(Base):
    __tablename__ = "user_security"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    mfa_enabled = Column(Boolean, default=False)
    totp_secret = Column(String(64), nullable=True)

    last_login = Column(DateTime, nullable=True)
    last_ip = Column(String(64), nullable=True)

    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)

    reset_token = Column(String(256), nullable=True)
    reset_token_expire = Column(DateTime, nullable=True)

    user = relationship("User", backref="security", uselist=False)

    def __repr__(self):
        return f"<UserSecurity user_id={self.user_id} mfa_enabled={self.mfa_enabled}>"

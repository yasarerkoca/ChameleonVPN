# ~/ChameleonVPN/backend/app/models/user/user_flags_settings.py

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserFlagsSettings(Base):
    __tablename__ = "user_flags_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    notification_settings = Column(JSONB, nullable=True)   # Örn: {'email': true, 'sms': false}
    flags = Column(JSONB, nullable=True)                   # Örn: {'is_beta': true}
    preferences = Column(JSONB, nullable=True)             # Örn: {'lang': 'en', 'theme': 'dark'}
    proxy_quota_gb = Column(Integer, default=0)
    active_proxy_count = Column(Integer, default=0)

    user = relationship("User", backref="flags_settings", uselist=False)

    def __repr__(self):
        return f"<UserFlagsSettings user_id={self.user_id}>"

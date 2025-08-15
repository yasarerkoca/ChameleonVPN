# ~/ChameleonVPN/backend/app/models/user/user_profile.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    phone_number = Column(String(32), nullable=True)
    preferred_language = Column(String(8), default='tr')
    referral_code = Column(String(16), unique=True, nullable=True)
    referred_by = Column(String(16), nullable=True)
    is_terms_accepted = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    anonymized_at = Column(DateTime, nullable=True)
    country_code = Column(String(8), nullable=True)
    city = Column(String(64), nullable=True)
    region = Column(String(64), nullable=True)

    user = relationship("User", backref="profile", uselist=False)

    def __repr__(self):
        return f"<UserProfile user_id={self.user_id} phone={self.phone_number}>"

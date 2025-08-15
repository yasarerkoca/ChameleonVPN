# ~/ChameleonVPN/backend/app/models/user/user_referral_rewards.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserReferralReward(Base):
    __tablename__ = "user_referral_rewards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    referred_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False)

    reward_amount = Column(Float, default=0.0)
    reward_currency = Column(String(10), default="USD")
    status = Column(String(32), default="pending")  # pending, paid, expired, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship('User',
        foreign_keys=[user_id],
        backref='referrals'
    )
    referred_user = relationship(
        "User",
        foreign_keys=[referred_user_id],
        viewonly=True
    )

    def __repr__(self):
        return (
            f"<UserReferralReward user_id={self.user_id} "
            f"referred={self.referred_user_id} amount={self.reward_amount}>"
        )

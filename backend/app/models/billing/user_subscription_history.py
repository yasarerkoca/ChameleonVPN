from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.config.database import Base

class UserSubscriptionHistory(Base):
    __tablename__ = "user_subscription_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=True)
    action = Column(String(32), nullable=False)  # 'subscribe', 'cancel', 'renew', vs.
    created_at = Column(DateTime)
    notes = Column(String(256), nullable=True)

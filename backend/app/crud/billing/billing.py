# ~/ChameleonVPN/backend/app/crud/billing/billing.py

from sqlalchemy.orm import Session
from typing import List
from app.models.billing.billing_history import BillingHistory
from app.models.billing.subscription_history import SubscriptionHistory


def get_user_billing_history(db: Session, user_id: int) -> List[BillingHistory]:
    return db.query(BillingHistory).filter(BillingHistory.user_id == user_id).order_by(BillingHistory.created_at.desc()).all()


def get_user_subscription_history(db: Session, user_id: int) -> List[SubscriptionHistory]:
    return db.query(SubscriptionHistory).filter(SubscriptionHistory.user_id == user_id).order_by(SubscriptionHistory.start_date.desc()).all()

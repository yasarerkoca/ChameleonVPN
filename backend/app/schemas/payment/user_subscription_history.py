# ~/ChameleonVPN/backend/app/schemas/payment/user_subscription_history.py

from pydantic import BaseModel
from datetime import datetime

class UserSubscriptionHistoryOut(BaseModel):
    id: int
    user_id: int
    plan_name: str
    start_date: datetime
    end_date: datetime
    status: str

    class Config:
        from_attributes = True

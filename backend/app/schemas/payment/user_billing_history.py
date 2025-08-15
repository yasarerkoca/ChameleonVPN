from pydantic import BaseModel
from datetime import datetime


class UserBillingHistoryOut(BaseModel):
    id: int
    user_id: int
    amount: float
    description: str
    created_at: datetime

    class Config:
        from_attributes = True

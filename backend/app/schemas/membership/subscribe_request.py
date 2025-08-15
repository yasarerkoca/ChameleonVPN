# ~/ChameleonVPN/backend/app/schemas/membership/subscribe_request.py

from pydantic import BaseModel

class SubscribeRequest(BaseModel):
    plan_id: int
    payment_method: str  # Örn: 'credit_card', 'paypal', 'crypto'

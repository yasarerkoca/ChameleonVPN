# ~/ChameleonVPN/backend/app/schemas/membership/upgrade_request.py

from pydantic import BaseModel

class UpgradeRequest(BaseModel):
    new_plan_id: int
    payment_method: str  # Örn: 'credit_card', 'paypal', 'crypto'

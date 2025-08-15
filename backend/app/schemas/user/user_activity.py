# ~/ChameleonVPN/backend/app/schemas/user/user_activity.py

from pydantic import BaseModel
from datetime import datetime

class UserServerActivityOut(BaseModel):
    id: int
    user_id: int
    server_id: int
    ip_address: str
    country_code: str
    connected_at: datetime
    disconnected_at: datetime | None = None

    class Config:
        from_attributes = True  # Pydantic v2 uyumu

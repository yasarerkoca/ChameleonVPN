# ~/ChameleonVPN/backend/app/schemas/user/user_session.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserSessionOut(BaseModel):
    session_id: str = Field(..., example="abc123xyz")
    user_id: int = Field(..., example=42)
    device_info: Optional[str] = Field(None, example="Windows 11 - Chrome")
    ip_address: Optional[str] = Field(None, example="192.168.1.100")
    last_active: datetime = Field(..., example="2025-08-01T15:00:00Z")

    class Config:
        from_attributes = True

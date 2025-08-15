from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class VPNLogOut(BaseModel):
    id: int
    user_id: int = Field(..., example=42)
    server_id: int = Field(..., example=101)
    connected_at: datetime = Field(..., example="2025-08-01T14:45:00Z")
    disconnected_at: Optional[datetime] = Field(None, example="2025-08-01T15:30:00Z")
    ip_address: Optional[str] = Field(None, example="203.0.113.45")
    protocol: Optional[str] = Field(None, example="WireGuard")

    class Config:
        from_attributes = True

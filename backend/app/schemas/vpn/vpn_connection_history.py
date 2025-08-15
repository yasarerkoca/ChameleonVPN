from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VPNConnectionHistoryCreate(BaseModel):
    user_id: int
    server_id: int
    ip: str
    country_code: Optional[str] = None
    duration: Optional[int] = None
    success: bool
    disconnected_at: Optional[datetime] = None

class VPNConnectionHistoryOut(VPNConnectionHistoryCreate):
    id: int
    connected_at: datetime

    class Config:
        from_attributes = True

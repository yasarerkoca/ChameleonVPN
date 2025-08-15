from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProxyOut(BaseModel):
    id: int
    ip_address: str = Field(..., example="192.168.1.100")
    port: int = Field(..., example=8080)
    country: Optional[str] = Field(None, example="US")

    class Config:
        from_attributes = True


class ProxyQuotaOut(BaseModel):
    proxy_id: int
    quota_total: int = Field(..., example=10000)
    quota_used: int = Field(..., example=2500)

    class Config:
        from_attributes = True


class ProxyPurchaseRequest(BaseModel):
    plan_id: int
    duration_days: int = Field(..., example=30)


class ProxyLogOut(BaseModel):
    id: int
    proxy_id: int
    user_id: int
    timestamp: datetime
    action: str

    class Config:
        from_attributes = True

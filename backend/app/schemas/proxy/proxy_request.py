# ~/ChameleonVPN/backend/app/schemas/proxy/proxy_request.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProxyRequestBase(BaseModel):
    request_reason: Optional[str] = Field(None, example="Kurumsal kullanım için gerekli.")


class ProxyRequestCreate(ProxyRequestBase):
    user_id: int


class ProxyRequestOut(ProxyRequestBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

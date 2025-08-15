from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProxyQuotaOut(BaseModel):
    """
    Kullanıcıya proxy üzerinden atanan kota bilgisi.

    Attributes:
        user_id (int): Kullanıcı ID'si.
        proxy_id (int): Proxy ID'si.
        assigned_quota_mb (int): Kullanıcıya atanan toplam kota (MB).
        used_quota_mb (int): Şu ana kadar kullanılan kota (MB).
        assigned_until (Optional[datetime]): Kota kullanım süresinin sonu (varsa).
    """
    user_id: int = Field(..., example=7)
    proxy_id: int = Field(..., example=3)
    assigned_quota_mb: int = Field(..., example=5000)
    used_quota_mb: int = Field(..., example=1200)
    assigned_until: Optional[datetime] = Field(None, example="2025-08-31T23:59:59Z")

    class Config:
        from_attributes = True

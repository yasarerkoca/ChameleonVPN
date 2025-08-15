from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserLimitOut(BaseModel):
    """
    Kullanıcının VPN ve proxy kullanım sınırları.

    Attributes:
        user_id (int): Kullanıcı ID'si.
        vpn_quota_gb (float): VPN için toplam kota (GB).
        proxy_quota_gb (float): Proxy hizmeti için kota (GB).
        device_limit (int): Eş zamanlı cihaz sınırı.
        ip_limit (int): Eş zamanlı IP sınırı.
        start_date (datetime): Kota kullanım başlangıç tarihi.
        end_date (datetime): Kota kullanım bitiş tarihi.
        created_at (datetime): Kayıt oluşturulma tarihi.
    """
    user_id: int = Field(..., example=101)
    vpn_quota_gb: Optional[float] = Field(None, example=50.0)
    proxy_quota_gb: Optional[float] = Field(None, example=25.0)
    device_limit: Optional[int] = Field(None, example=3)
    ip_limit: Optional[int] = Field(None, example=2)
    start_date: Optional[datetime] = Field(None, example="2025-08-01T00:00:00Z")
    end_date: Optional[datetime] = Field(None, example="2025-09-01T00:00:00Z")
    created_at: Optional[datetime] = Field(None, example="2025-08-01T12:00:00Z")

    class Config:
        from_attributes = True

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProxyIPBase(BaseModel):
    """
    Proxy IP için temel bilgiler.

    Attributes:
        ip_address (str): Proxy IP adresi.
        port (int): Bağlantı portu.
        country (Optional[str]): IP'nin ait olduğu ülke.
        total_quota_mb (Optional[int]): Tanımlı toplam kota (MB).
        is_active (Optional[bool]): Proxy aktif mi?
    """
    ip_address: str = Field(..., example="192.168.1.100")
    port: int = Field(..., example=8080)
    country: Optional[str] = Field(None, example="US")
    total_quota_mb: Optional[int] = Field(default=0, example=10000)
    is_active: Optional[bool] = Field(default=True)


class ProxyIPCreate(ProxyIPBase):
    """
    Yeni proxy IP oluşturmak için input şeması.
    """
    pass


class ProxyIPOut(ProxyIPBase):
    """
    Proxy IP kaydının dışa aktarım (output) şeması.

    Attributes:
        id (int): Proxy ID'si.
        created_at (datetime): Oluşturulma zamanı.
    """
    id: int
    created_at: datetime = Field(..., example="2025-08-01T13:00:00Z")

    class Config:
        from_attributes = True

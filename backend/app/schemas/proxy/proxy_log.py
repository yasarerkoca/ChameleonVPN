from pydantic import BaseModel, Field
from datetime import datetime


class ProxyLogOut(BaseModel):
    """
    Proxy ile ilgili kullanıcı aktivitelerini loglama şeması.

    Attributes:
        id (int): Log ID'si.
        user_id (int): İşlemi yapan kullanıcı ID'si.
        ip (str): Proxy IP adresi.
        action (str): Yapılan işlem (örn. "ASSIGNED", "REVOKED", "EXPIRED").
        timestamp (datetime): İşlem zamanı.
    """
    id: int
    user_id: int = Field(..., example=7)
    ip: str = Field(..., example="192.168.1.100")
    action: str = Field(..., example="ASSIGNED")
    timestamp: datetime = Field(..., example="2025-08-01T17:10:00Z")

    class Config:
        from_attributes = True

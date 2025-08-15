from pydantic import BaseModel, Field
from datetime import datetime


class APIKeyAccessLogBase(BaseModel):
    """
    API anahtarı kullanımıyla ilgili erişim log bilgisi.

    Attributes:
        api_key_id (int): Kullanılan API anahtarının ID'si.
        path_accessed (str): Erişilen endpoint (örn. "/admin/user").
        ip_address (str): İsteği gönderen IP adresi.
        timestamp (datetime): Erişim zamanı.
    """
    api_key_id: int = Field(..., example=1)
    path_accessed: str = Field(..., example="/admin/user")
    ip_address: str = Field(..., example="192.168.1.1")
    timestamp: datetime = Field(..., example="2025-08-01T15:45:00Z")


class APIKeyAccessLogOut(APIKeyAccessLogBase):
    """
    API erişim logunun dışa aktarımı.

    Attributes:
        id (int): Log kaydı ID'si.
    """
    id: int

    class Config:
        from_attributes = True

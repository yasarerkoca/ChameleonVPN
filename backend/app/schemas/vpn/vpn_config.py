from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class VPNConfigOut(BaseModel):
    """
    Kullanıcının indireceği VPN yapılandırma çıktısı.
    """
    server_id: int = Field(..., example=101)
    config: str = Field(..., example="[Interface]\nPrivateKey = ...")

    class Config:
        from_attributes = True


class ConnectionAttemptCreate(BaseModel):
    """
    Yeni VPN bağlantı denemesi kaydı için şema.
    """
    user_id: int = Field(..., example=42)
    ip_address: Optional[str] = Field(None, example="192.168.1.1")
    timestamp: datetime = Field(..., example="2025-08-01T14:45:00Z")
    success: bool = Field(..., example=True)
    protocol: Optional[str] = Field(None, example="WireGuard")


class VPNLogCreate(BaseModel):
    """
    VPN kullanım log kaydı için giriş şeması.
    """
    user_id: int = Field(..., example=42)
    server_id: int = Field(..., example=101)
    connected_at: datetime = Field(..., example="2025-08-01T14:45:00Z")
    disconnected_at: Optional[datetime] = Field(None, example="2025-08-01T15:15:00Z")
    protocol: Optional[str] = Field(None, example="OpenVPN")
    ip_address: Optional[str] = Field(None, example="203.0.113.1")

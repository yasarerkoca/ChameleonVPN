from pydantic import BaseModel, Field
from typing import Optional


class VPNServerCreate(BaseModel):
    """
    Yeni bir VPN sunucusu oluşturmak için istenen alanlar.
    """
    name: str = Field(..., example="Frankfurt-1")
    ip_address: str = Field(..., example="192.0.2.1")
    type: str = Field(..., example="WireGuard")  # openvpn / wireguard
    country_code: Optional[str] = Field(None, example="DE")  # ISO kod
    city: Optional[str] = Field(None, example="Frankfurt")
    capacity: Optional[int] = Field(100, example=100)  # Maks. eşzamanlı bağlantı
    status: Optional[str] = Field("active", example="active")  # active / passive


class VPNServerUpdate(BaseModel):
    """
    Mevcut bir VPN sunucusunu güncellemek için kullanılan alanlar.
    """
    name: Optional[str] = Field(None, example="Frankfurt-2")
    ip_address: Optional[str] = Field(None, example="192.0.2.2")
    type: Optional[str] = Field(None, example="OpenVPN")
    country_code: Optional[str] = Field(None, example="DE")
    city: Optional[str] = Field(None, example="Berlin")
    capacity: Optional[int] = Field(None, example=200)
    status: Optional[str] = Field(None, example="passive")


class VPNServerOut(BaseModel):
    """
    API response için kullanılan sunucu çıktısı şeması.
    """
    id: int
    name: str
    ip_address: str
    type: str  # openvpn / wireguard
    country_code: Optional[str]
    city: Optional[str]
    capacity: Optional[int]
    status: Optional[str]

    class Config:
        from_attributes = True  # SQLAlchemy uyumu

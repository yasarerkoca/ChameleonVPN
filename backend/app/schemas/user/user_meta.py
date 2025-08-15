from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


# -------------------- Sistem Bildirimleri --------------------
class UserNotification(BaseModel):
    message: str = Field(..., example="Şifreniz başarıyla değiştirildi.")
    type: str = Field(..., example="security")
    sent_at: datetime = Field(..., example="2025-08-01T14:00:00Z")

class NotificationCreate(BaseModel):
    user_id: int = Field(..., example=1)
    message: str = Field(..., example="Şifreniz başarıyla güncellendi.")
    type: str = Field(..., example="security")


# -------------------- Kullanıcı Silme --------------------
class UserDeleted(BaseModel):
    user_id: int = Field(..., example=42)
    deleted_at: datetime = Field(..., example="2025-08-01T12:00:00Z")
    reason: Optional[str] = Field(None, example="İstek üzerine silindi.")


# -------------------- Destek Talebi --------------------
class UserSupportTicket(BaseModel):
    subject: str = Field(..., example="VPN bağlantısı kurulamıyor")
    description: str = Field(..., example="Bağlantı kurulurken hata alıyorum.")
    created_at: datetime = Field(..., example="2025-08-01T11:30:00Z")

class SupportTicketCreate(BaseModel):
    subject: str
    description: str


# -------------------- Yönlendirme Ödülleri --------------------
class UserReferralRewards(BaseModel):
    referred_email: EmailStr = Field(..., example="arkadas@example.com")
    reward_given: bool = Field(..., example=True)
    created_at: datetime = Field(..., example="2025-08-01T10:15:00Z")

class ReferralRewardCreate(BaseModel):
    referred_email: EmailStr = Field(..., example="yeni.kullanici@example.com")
    reward_given: bool = Field(default=False)


# -------------------- Referans İlişkisi --------------------
class UserRelationship(BaseModel):
    referred_by_id: Optional[int] = Field(None, example=17)
    referred_to_id: Optional[int] = Field(None, example=42)

class UserRelationshipCreate(BaseModel):
    referred_by_id: Optional[int] = Field(None, example=1)
    referred_to_id: Optional[int] = Field(None, example=2)


# -------------------- Sosyal Giriş --------------------
class UserExternalAuth(BaseModel):
    provider: str = Field(..., example="google")
    external_id: str = Field(..., example="google-oauth2|1234567890")

class ExternalAuthCreate(BaseModel):
    provider: str = Field(..., example="google")
    external_id: str = Field(..., example="google-oauth2|1234567890")
    user_id: int = Field(..., example=42)


# -------------------- Güncellemeler --------------------
class UserStatusUpdate(BaseModel):
    is_active: Optional[bool] = Field(None, description="Kullanıcının aktiflik durumu")
    is_deleted: Optional[bool] = Field(None, description="Kullanıcının silinme durumu")

class UserFlagsUpdate(BaseModel):
    flags: dict = Field(..., example={"beta_user": True, "vpn_blocked": False})
    notification_settings: Optional[dict] = Field(None)
    preferences: Optional[dict] = Field(None)

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, example="John Doe")
    phone_number: Optional[str] = Field(None, example="+905555555555")
    preferred_language: Optional[str] = Field(None, example="tr")
    city: Optional[str] = Field(None, example="İstanbul")
    region: Optional[str] = Field(None, example="Marmara")
    country_code: Optional[str] = Field(None, example="TR")

class UserSecurityUpdate(BaseModel):
    password: Optional[str] = Field(None, example="YeniŞifre123")
    mfa_enabled: Optional[bool] = Field(None, example=True)
    totp_secret: Optional[str] = Field(None, example="JBSWY3DPEHPK3PXP")

class ServerActivityCreate(BaseModel):
    """
    Yeni kullanıcı sunucu aktivitesi oluşturma şeması.
    """
    user_id: int = Field(..., example=42)
    server_ip: str = Field(..., example="192.168.1.100")
    action: str = Field(..., example="connected")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class UserSessionCreate(BaseModel):
    """
    Yeni kullanıcı oturumu oluşturma şeması.
    """
    user_id: int = Field(..., example=42)
    session_token: str = Field(..., example="abc123xyz456")
    user_agent: Optional[str] = Field(None, example="Mozilla/5.0")
    ip_address: Optional[str] = Field(None, example="192.168.1.10")
    login_time: datetime = Field(default_factory=datetime.utcnow)

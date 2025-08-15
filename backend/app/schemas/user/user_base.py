from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """
    Kullanıcıya ait temel alanlar (email, ad soyad, aktiflik).
    """
    email: EmailStr = Field(..., example="user@example.com")
    full_name: Optional[str] = Field(None, example="John Doe")
    is_active: bool = Field(default=True)


class UserCreate(UserBase):
    """
    Yeni kullanıcı oluşturma isteği (şifre dahil).
    """
    password: str = Field(..., example="StrongPassword123!")


class UserLogin(BaseModel):
    """
    Kullanıcı giriş isteği (email + şifre).
    """
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="StrongPassword123!")


class UserUpdate(BaseModel):
    """
    Kullanıcı bilgilerini güncelleme şeması.
    """
    full_name: Optional[str] = Field(None, example="Jane Doe")
    is_active: Optional[bool] = Field(None, description="Kullanıcı aktif mi?")
    is_email_verified: Optional[bool] = Field(None, description="E-posta doğrulandı mı?")


class PasswordChange(BaseModel):
    """
    Parola değiştirme isteği şeması.
    """
    old_password: str = Field(..., example="OldPass123")
    new_password: str = Field(..., example="NewStrongPass123!")


class UserOut(UserBase):
    """
    Kullanıcı verisinin dışa aktarımı (output).
    """
    id: int
    created_at: datetime = Field(..., example="2025-08-01T12:00:00Z")

    class Config:
        from_attributes = True  # Pydantic v2 uyumu için


class TwoFactorVerifyRequest(BaseModel):
    token: str = Field(..., example="123456")

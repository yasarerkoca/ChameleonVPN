from pydantic import BaseModel, Field
from datetime import datetime


class TwoFactorTokenBase(BaseModel):
    """
    Kullanıcının iki faktörlü doğrulama (2FA) token bilgisi.

    Attributes:
        user_id (int): Token ile ilişkili kullanıcı ID'si.
        token (str): Doğrulama token'ı.
        created_at (datetime): Token oluşturulma zamanı.
        expires_at (datetime): Token geçerlilik süresi bitişi.
    """
    user_id: int = Field(..., example=42)
    token: str = Field(..., example="678392")
    created_at: datetime = Field(..., example="2025-08-01T17:00:00Z")
    expires_at: datetime = Field(..., example="2025-08-01T17:05:00Z")


class TwoFactorTokenOut(TwoFactorTokenBase):
    """
    2FA token verisinin dışa aktarımı.

    Attributes:
        id (int): Token kaydının ID'si.
    """
    id: int

    class Config:
        from_attributes = True

# ~/ChameleonVPN/backend/app/schemas/security/api_key.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class APIKeyCreate(BaseModel):
    """
    API anahtarı oluşturma isteği.
    Sadece 'key' gönderilir; 'revoked' sunucuda False başlar.
    """
    key: str = Field(..., example="sk_live_xxx")


class APIKeyOut(BaseModel):
    """
    API anahtarı dışa aktarım şeması (response).
    """
    id: int
    key: str = Field(..., example="sk_live_xxx")
    revoked: bool = False
    created_at: Optional[datetime] = None

    # Pydantic v2 uyumu: SQLAlchemy instance -> model dönüşümleri
    model_config = dict(from_attributes=True)


__all__ = ["APIKeyCreate", "APIKeyOut"]

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class APIKeyBase(BaseModel):
    """
    API anahtarı bilgisi.

    Attributes:
        name (str): Anahtar adı (örneğin sistem içi tanım).
        key (str): Gizli anahtar değeri.
        is_active (bool): Anahtar aktif mi?
    """
    name: str = Field(..., example="admin-dashboard")
    key: str = Field(..., example="sk_test_abc123xyz")
    is_active: bool = Field(default=True)


class APIKeyOut(APIKeyBase):
    """
    API anahtarının dışa aktarımı (output) şeması.

    Attributes:
        id (int): Anahtarın ID'si.
        created_at (datetime): Oluşturulma zamanı.
    """
    id: int
    created_at: Optional[datetime] = Field(None, example="2025-08-01T14:00:00Z")

    class Config:
        from_attributes = True

from pydantic import BaseModel, Field
from datetime import datetime


class RefreshTokenBlacklistBase(BaseModel):
    """
    Sistemden manuel olarak kara listeye alınan refresh token.

    Attributes:
        token (str): Kara listeye alınmış refresh token değeri.
        blacklisted_at (datetime): Kara listeye alınma zamanı.
    """
    token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5...")
    blacklisted_at: datetime = Field(..., example="2025-08-01T16:45:00Z")


class RefreshTokenBlacklistOut(RefreshTokenBlacklistBase):
    """
    Kara liste token kaydının dışa aktarımı.

    Attributes:
        id (int): Kayıt ID'si.
    """
    id: int

    class Config:
        from_attributes = True

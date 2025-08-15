from pydantic import BaseModel, Field
from datetime import datetime


class UserBlocklistBase(BaseModel):
    """
    Sistemden engellenmiş kullanıcı bilgisi.

    Attributes:
        user_id (int): Engellenen kullanıcının ID'si.
        reason (str): Engelleme nedeni.
        blocked_at (datetime): Engelleme zamanı.
    """
    user_id: int = Field(..., example=17)
    reason: str = Field(..., example="Aşırı kötüye kullanım (abuse)")
    blocked_at: datetime = Field(..., example="2025-08-01T18:00:00Z")


class UserBlocklistOut(UserBlocklistBase):
    """
    Engellenmiş kullanıcı kaydının dışa aktarımı.

    Attributes:
        id (int): Kayıt ID'si.
    """
    id: int

    class Config:
        from_attributes = True

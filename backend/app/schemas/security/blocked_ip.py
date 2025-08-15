from pydantic import BaseModel, Field
from datetime import datetime


class BlockedIPBase(BaseModel):
    """
    Güvenlik nedeniyle engellenmiş IP adresi kaydı.

    Attributes:
        ip_address (str): Engellenen IP adresi.
        reason (str): Engelleme nedeni (örn. brute-force, spam).
        blocked_at (datetime): Engelleme zamanı.
    """
    ip_address: str = Field(..., example="203.0.113.42")
    reason: str = Field(..., example="Brute-force attack")
    blocked_at: datetime = Field(..., example="2025-08-01T16:00:00Z")


class BlockedIPOut(BlockedIPBase):
    """
    Engellenmiş IP bilgisinin dışa aktarımı.

    Attributes:
        id (int): Engelleme kaydının ID'si.
    """
    id: int

    class Config:
        from_attributes = True

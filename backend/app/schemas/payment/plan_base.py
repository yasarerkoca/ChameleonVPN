from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PlanBase(BaseModel):
    """
    Abonelik planı için temel model.

    Attributes:
        name (str): Plan adı (örn. "Pro", "Premium").
        price (float): Plan ücreti (USD).
        duration_days (int): Plan süresi (gün).
        proxy_limit (Optional[int]): Maksimum proxy limiti.
        data_limit_gb (Optional[float]): Aylık veri limiti (GB).
    """
    name: str = Field(..., example="Premium")
    price: float = Field(..., example=9.99)
    duration_days: int = Field(..., example=30)
    proxy_limit: Optional[int] = Field(None, example=10)
    data_limit_gb: Optional[float] = Field(None, example=100.0)


class PlanCreate(PlanBase):
    """
    Yeni plan oluşturmak için input şeması.
    """
    pass


class PlanOut(PlanBase):
    """
    Plan verisinin dışa aktarım (output) şeması.

    Attributes:
        id (int): Plan ID'si.
        created_at (datetime): Oluşturulma tarihi.
    """
    id: int
    created_at: datetime = Field(..., example="2025-08-01T12:00:00Z")

    class Config:
        from_attributes = True

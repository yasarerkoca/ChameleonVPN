from pydantic import BaseModel, Field
from datetime import datetime
from app.schemas.payment import PlanBase


class MembershipOut(BaseModel):
    """
    Kullanıcıya ait aktif üyelik bilgisinin dışa aktarımı (output).
    """
    id: int
    plan: PlanBase
    start_date: datetime = Field(..., example="2025-08-01T00:00:00Z")
    end_date: datetime = Field(..., example="2025-09-01T00:00:00Z")
    quota_total: int = Field(..., example=10240)
    quota_used: int = Field(..., example=2048)

    class Config:
        from_attributes = True

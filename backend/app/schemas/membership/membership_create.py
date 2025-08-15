from pydantic import BaseModel, Field


class MembershipCreate(BaseModel):
    """
    Yeni üyelik oluşturmak için gereken bilgiler.
    
    Attributes:
        plan_id (int): Seçilen plan ID'si.
        quota_total (int): Başlangıç kotası (MB/GB).
    """
    plan_id: int = Field(..., example=2)
    quota_total: int = Field(..., example=10240)

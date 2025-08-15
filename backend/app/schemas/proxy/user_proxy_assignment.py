from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserProxyAssignmentBase(BaseModel):
    """
    Bir kullanıcıya atanmış proxy kaydı.

    Attributes:
        user_id (int): Kullanıcı ID'si.
        proxy_id (int): Proxy ID'si.
        assigned_quota_mb (Optional[int]): Tanımlanan kota (MB).
        assigned_until (Optional[datetime]): Geçerlilik bitiş tarihi.
        is_active (Optional[bool]): Atama şu an aktif mi?
    """
    user_id: int = Field(..., example=7)
    proxy_id: int = Field(..., example=3)
    assigned_quota_mb: Optional[int] = Field(default=0, example=5000)
    assigned_until: Optional[datetime] = Field(None, example="2025-09-01T23:59:59Z")
    is_active: Optional[bool] = Field(default=True)


class UserProxyAssignmentCreate(UserProxyAssignmentBase):
    """
    Yeni proxy ataması yapmak için input şeması.
    """
    pass


class UserProxyAssignmentOut(UserProxyAssignmentBase):
    """
    Kullanıcı-proxy ilişkisinin dışa aktarım (output) şeması.

    Attributes:
        id (int): Atama ID'si.
        created_at (datetime): Oluşturulma zamanı.
    """
    id: int
    created_at: datetime = Field(..., example="2025-08-01T18:30:00Z")

    class Config:
        from_attributes = True


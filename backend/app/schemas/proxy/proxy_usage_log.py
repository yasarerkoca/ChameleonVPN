from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProxyUsageLogBase(BaseModel):
    """
    Kullanıcının bir proxy üzerinden yaptığı veri kullanımının logu.

    Attributes:
        user_id (int): Kullanıcı ID'si.
        proxy_id (int): Kullanılan proxy ID'si.
        used_mb (Optional[int]): Kullanılan veri miktarı (MB).
        timestamp (Optional[datetime]): Logun oluşturulma zamanı.
        note (Optional[str]): İsteğe bağlı açıklama / etiket.
    """
    user_id: int = Field(..., example=5)
    proxy_id: int = Field(..., example=2)
    used_mb: Optional[int] = Field(default=0, example=1024)
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    note: Optional[str] = Field(None, example="AI tarafından tespit edilen aşırı kullanım.")


class ProxyUsageLogCreate(ProxyUsageLogBase):
    """
    Yeni proxy kullanım logu oluşturmak için input şeması.
    """
    pass


class ProxyUsageLogOut(ProxyUsageLogBase):
    """
    Proxy kullanım logunun dışa aktarım (output) şeması.

    Attributes:
        id (int): Log kaydı ID'si.
    """
    id: int

    class Config:
        from_attributes = True

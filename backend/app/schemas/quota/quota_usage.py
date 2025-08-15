from pydantic import BaseModel, Field


class QuotaUsageRecord(BaseModel):
    """
    Kullanıcının geçmişe veya anlık duruma ait kota kullanım kaydı.

    Attributes:
        user_id (int): Kullanıcı ID'si.
        quota_used (float): Kullanılan veri miktarı (MB).
        quota_limit (float): Kullanıcının mevcut kota limiti (MB).
    """
    user_id: int = Field(..., example=7)
    quota_used: float = Field(..., example=1500.5)
    quota_limit: float = Field(..., example=5000.0)

    class Config:
        from_attributes = True

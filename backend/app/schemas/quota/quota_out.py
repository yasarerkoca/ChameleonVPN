from pydantic import BaseModel, Field


class QuotaUsageOut(BaseModel):
    """
    Kullanıcının genel VPN ve proxy kotasını gösteren çıktı modeli.
    """
    quota_total: int = Field(..., example=10240)
    quota_used: int = Field(..., example=2048)
    proxy_quota_total: int = Field(..., example=5000)
    proxy_quota_used: int = Field(..., example=1300)

    class Config:
        from_attributes = True


class UserLimitOut(BaseModel):
    """
    Kullanıcıya atanmış limit değerlerini temsil eder (admin tarafından belirlenen sabit sınırlar).
    """
    vpn_limit: int = Field(..., example=15000)
    proxy_limit: int = Field(..., example=7000)

    class Config:
        from_attributes = True

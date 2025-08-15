from pydantic import BaseModel, Field
from datetime import datetime


class MembershipBase(BaseModel):
    """
    Kullanıcının sahip olduğu üyelik bilgilerinin temel yapısı.

    Attributes:
        start_date (datetime): Üyeliğin başlangıç tarihi.
        end_date (datetime): Üyeliğin bitiş tarihi.
        quota_total (int): Üyelik kapsamında tanımlı toplam kota (MB/GB).
    """
    start_date: datetime = Field(..., example="2025-08-01T00:00:00Z")
    end_date: datetime = Field(..., example="2025-09-01T00:00:00Z")
    quota_total: int = Field(..., example=10240)  # örn. 10 GB

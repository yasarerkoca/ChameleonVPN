from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# Enum tanımları
class PaymentMethod(str, Enum):
    stripe = "stripe"
    iyzico = "iyzico"

class PaymentStatus(str, Enum):
    completed = "completed"
    failed = "failed"
    pending = "pending"

class PaymentType(str, Enum):
    proxy = "proxy"
    ek_kota = "ek_kota"

# Temel ödeme şeması
class PaymentBase(BaseModel):
    amount: float = Field(..., example=29.99)
    method: PaymentMethod = Field(..., example="stripe")
    status: PaymentStatus = Field(..., example="completed")
    type: PaymentType = Field(..., example="proxy")

# Yeni ödeme kaydı oluşturmak için input şeması
class PaymentCreate(PaymentBase):
    user_id: int = Field(..., example=5)

# Output şeması
class PaymentOut(PaymentBase):
    id: int
    user_id: int
    created_at: datetime = Field(..., example="2025-08-01T13:45:00Z")

    class Config:
        from_attributes = True

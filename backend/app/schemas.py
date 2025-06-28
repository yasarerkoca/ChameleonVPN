from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=64)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool
    is_active: bool
    email_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 uyumu


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


class VPNProfileOut(BaseModel):
    id: int
    name: str
    config: str

    class Config:
        from_attributes = True


class VPNProfileCreate(BaseModel):
    name: str
    config: str

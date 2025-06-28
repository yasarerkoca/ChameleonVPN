
from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=64)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool
    is_active: bool
    email_verified: bool
    created_at: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

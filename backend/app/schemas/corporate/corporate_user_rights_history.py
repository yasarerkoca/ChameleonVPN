from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CorporateUserRightBase(BaseModel):
    """
    Kurumsal kullanıcı yetki geçmişi için temel alanlar.
    
    Attributes:
        user_id (int): Yetkisi değiştirilen kullanıcı ID'si.
        changed_by_admin_id (Optional[int]): Değişikliği yapan admin ID'si.
        field_changed (str): Değiştirilen alan adı.
        old_value (Optional[str]): Önceki değer.
        new_value (Optional[str]): Yeni değer.
        changed_at (Optional[datetime]): Değişiklik zamanı.
        note (Optional[str]): İsteğe bağlı not.
    """
    user_id: int = Field(..., example=17)
    changed_by_admin_id: Optional[int] = Field(None, example=1)
    field_changed: str = Field(..., example="proxy_limit")
    old_value: Optional[str] = Field(None, example="10")
    new_value: Optional[str] = Field(None, example="20")
    changed_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    note: Optional[str] = Field(None, example="Yetki güncellendi.")


class CorporateUserRightCreate(CorporateUserRightBase):
    """
    Yeni yetki değişiklik kaydı oluşturmak için şema.
    """
    pass


class CorporateUserRightOut(CorporateUserRightBase):
    """
    Yetki geçmişi kaydının dışa aktarım (output) şeması.
    
    Attributes:
        id (int): Kayıt ID'si.
    """
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel, Field


class CorporateUserGroupBase(BaseModel):
    """
    Kurumsal kullanıcı grubu için temel alanlar.
    
    Attributes:
        name (str): Grup adı (örn. "Acme Corp. Adminler").
        max_proxies (int): Grup için tanımlı maksimum proxy adedi.
    """
    name: str = Field(..., example="Acme Corp. Adminler")
    max_proxies: int = Field(..., example=20)


class CorporateUserGroupCreate(CorporateUserGroupBase):
    """
    Yeni kurumsal kullanıcı grubu oluşturmak için kullanılan giriş şeması.
    """
    pass


class CorporateUserGroupOut(CorporateUserGroupBase):
    """
    Dışa veri aktarımında kullanılan şema (output).
    
    Attributes:
        id (int): Grup veritabanı ID'si.
    """
    id: int

    class Config:
        from_attributes = True

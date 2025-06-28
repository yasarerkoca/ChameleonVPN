from pydantic import BaseModel

class VPNProfileOut(BaseModel):
    id: int
    name: str
    server: str
    config: str

    class Config:
        from_attributes = True  # Pydantic V2'de orm_mode yerine bu kullanılır
    

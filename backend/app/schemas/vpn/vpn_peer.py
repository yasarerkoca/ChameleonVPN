from pydantic import BaseModel


class VPNPeerCreate(BaseModel):
    server_id: int


class VPNPeerOut(BaseModel):
    id: int
    user_id: int
    server_id: int
    ip_address: str
    public_key: str

    class Config:
        orm_mode = True


class VPNPeerWithConfig(BaseModel):
    id: int
    config: str

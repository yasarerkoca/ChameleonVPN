from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import PlainTextResponse
from typing import List

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user
from app.models.user.user import User
from app.models.vpn.vpn_server import VPNServer
from app.schemas.vpn.vpn_server import VPNServerOut, VPNServerCreate

router = APIRouter(
    prefix="/vpn/server",
    tags=["vpn-server"]
)

def admin_required(current_user: User = Depends(get_current_user)):
    if not getattr(current_user, "is_admin", False) and getattr(current_user, "role", "") != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

@router.get("/", response_model=List[VPNServerOut], summary="Tüm VPN sunucularını listele (herkes görebilir)")
def list_servers(db: Session = Depends(get_db)):
    return db.query(VPNServer).all()

@router.post("/", response_model=VPNServerOut, summary="Yeni VPN sunucusu ekle (admin)")
def create_server(
    server: VPNServerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    new_server = VPNServer(**server.dict())
    db.add(new_server)
    db.commit()
    db.refresh(new_server)
    return new_server

@router.delete("/{server_id}", summary="VPN sunucusunu sil (admin)")
def delete_server(
    server_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    server = db.query(VPNServer).get(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    db.delete(server)
    db.commit()
    return {"msg": "Server deleted"}

@router.get("/my", response_model=List[VPNServerOut], summary="Kullanıcıya atanmış VPN sunucularını getir (isteğe bağlı)")
def my_servers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Eğer kullanıcıya özel sunucu ilişkisi yoksa hepsini dön (dummy)
    return db.query(VPNServer).all()

@router.get("/my-config/{server_id}", response_class=PlainTextResponse, summary="Seçilen sunucunun yapılandırmasını düz metin olarak getir")
def get_my_vpn_config(
    server_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    server = db.query(VPNServer).get(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    # TODO: Gerçek kullanıcı key'leriyle dosya üretilmeli
    config = f"""
[Interface]
PrivateKey = KULLANICI_PRIVATE_KEY
Address = 10.0.0.2/24

[Peer]
PublicKey = SERVER_PUBLIC_KEY
Endpoint = {server.ip_address}:51820
AllowedIPs = 0.0.0.0/0
"""
    return config.strip()

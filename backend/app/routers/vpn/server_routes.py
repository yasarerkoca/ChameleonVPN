from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import PlainTextResponse
from typing import Dict, List

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user
from app.models.user.user import User
from app.models.vpn.vpn_server import VPNServer
from app.models.vpn.vpn_config import VPNConfig
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

    # Önceden oluşturulmuş bir yapılandırma varsa onu dön
    existing = (
        db.query(VPNConfig)
        .filter(
            VPNConfig.user_id == current_user.id,
            VPNConfig.server_id == server.id,
        )
        .first()
    )
    if existing:
        return existing.config.strip()

    # Kullanıcı anahtarlarını veritabanından veya dış servisten getir
    def _fetch_user_keys(user: User, protocol: str) -> Dict[str, str]:
        """Kullanıcıya ait VPN anahtarlarını getir (örnek/stub)."""
        if protocol.lower() == "wireguard":
            # Gerçek senaryoda bu bilgiler güvenli bir şekilde saklanıp alınmalı
            return {"private_key": "USER_PRIVATE_KEY", "public_key": "USER_PUBLIC_KEY"}
        elif protocol.lower() == "openvpn":
            return {"cert": "USER_CERT", "key": "USER_KEY"}
        raise HTTPException(status_code=400, detail="Unsupported VPN protocol")

    keys = _fetch_user_keys(current_user, server.type)

    # Protokole göre yapılandırma metnini oluştur
    if server.type.lower() == "wireguard":
        server_public_key = getattr(server, "public_key", "SERVER_PUBLIC_KEY")
        config = (
            f"[Interface]\n"
            f"PrivateKey = {keys['private_key']}\n"
            f"Address = 10.0.0.2/24\n\n"
            f"[Peer]\n"
            f"PublicKey = {server_public_key}\n"
            f"Endpoint = {server.ip_address}:51820\n"
            f"AllowedIPs = 0.0.0.0/0"
        )
    elif server.type.lower() == "openvpn":
        config = (
            "client\n"
            f"remote {server.ip_address} 1194\n"
            "dev tun\n"
            f"<cert>\n{keys['cert']}\n</cert>\n"
            f"<key>\n{keys['key']}\n</key>"
        )
    else:
        raise HTTPException(status_code=400, detail="Unsupported VPN server type")

    # Yapılandırmayı veritabanına kaydet (cache) ve döndür
    db_config = VPNConfig(user_id=current_user.id, server_id=server.id, config=config)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)

    return config.strip()

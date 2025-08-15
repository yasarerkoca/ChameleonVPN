from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.user.user import User

from app.utils.db.db_utils import get_db
from app.utils.geo.geoip_utils import get_country_by_ip
from app.services.ai_server_selector import rank_servers
from app.models.vpn.vpn_server import VPNServer
from app.schemas.vpn.vpn_server import VPNServerOut
from app.utils.auth.auth_utils import get_current_user

router = APIRouter(
    prefix="/vpn/auto",
    tags=["vpn-auto-selector"]
)

@router.get("/connect", response_model=VPNServerOut, summary="En uygun sunucuyu AI ile bul ve döndür")
def auto_connect(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client_ip = request.client.host
    if client_ip in ("127.0.0.1", "localhost"):
        raise HTTPException(status_code=400, detail="Gerçek IP tespit edilemedi")

    user_country = get_country_by_ip(client_ip)
    servers: List[VPNServer] = db.query(VPNServer).filter(VPNServer.status == "active").all()

    if not servers:
        raise HTTPException(status_code=404, detail="Hiç sunucu bulunamadı")

    sorted_servers = rank_servers(
        user_country_code=user_country,
        servers=servers,
        db=db,
        user_ip=client_ip
    )

    if not sorted_servers:
        raise HTTPException(status_code=500, detail="AI sunucu skorlama başarısız")

    return sorted_servers[0]

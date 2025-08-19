from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user
from app.models.user.user import User
from app.schemas.vpn.vpn_peer import VPNPeerCreate, VPNPeerOut, VPNPeerWithConfig
from app.services import wireguard_service

router = APIRouter(prefix="/vpn/peers", tags=["vpn-peers"])


@router.get("/", response_model=List[VPNPeerOut])
def list_my_peers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    peers = wireguard_service.list_peers(db, current_user.id)
    result = []
    for p in peers:
        result.append(
            VPNPeerOut(
                id=p.id,
                user_id=p.user_id,
                server_id=p.server_id,
                ip_address=p.ip_address,
                public_key=p.key.public_key if p.key else "",
            )
        )
    return result


@router.post("/", response_model=VPNPeerWithConfig)
def create_peer(
    payload: VPNPeerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    peer, config = wireguard_service.allocate_peer(db, current_user.id, payload.server_id)
    return VPNPeerWithConfig(id=peer.id, config=config)


@router.delete("/{peer_id}")
def delete_peer(
    peer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    wireguard_service.revoke_peer(db, peer_id, current_user.id)
    return {"detail": "Peer revoked"}

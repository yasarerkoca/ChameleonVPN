import os
import subprocess
from typing import List, Tuple
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.vpn.vpn_key import VPNKey
from app.models.vpn.vpn_peer import VPNPeer
from app.models.vpn.vpn_server import VPNServer

WG_INTERFACE = os.getenv("WG_INTERFACE", "wg0")

def allocate_peer(db: Session, user_id: int, server_id: int) -> Tuple[VPNPeer, str]:
    """Allocate a VPN peer for the given user and server and configure WireGuard."""
    server = db.query(VPNServer).get(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    key = (
        db.query(VPNKey)
        .filter(VPNKey.server_id == server_id, VPNKey.is_allocated.is_(False))
        .first()
    )
    if not key:
        raise HTTPException(status_code=404, detail="No available keys")

    key.is_allocated = True
    peer = VPNPeer(
        user_id=user_id,
        server_id=server_id,
        key_id=key.id,
        ip_address=key.ip_address,
    )
    db.add(peer)

    try:
        subprocess.run(
            [
                "wg",
                "set",
                WG_INTERFACE,
                "peer",
                key.public_key,
                "allowed-ips",
                f"{key.ip_address}/32",
            ],
            check=True,
        )
        db.commit()
        db.refresh(peer)
    except subprocess.CalledProcessError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to configure WireGuard peer"
        ) from exc
    config = generate_config(key, server)
    return peer, config


def list_peers(db: Session, user_id: int) -> List[VPNPeer]:
    return db.query(VPNPeer).filter(VPNPeer.user_id == user_id).all()


def revoke_peer(db: Session, peer_id: int, user_id: int | None = None) -> None:
    query = db.query(VPNPeer).filter(VPNPeer.id == peer_id)
    if user_id is not None:
        query = query.filter(VPNPeer.user_id == user_id)
    peer = query.first()
    if not peer:
        raise HTTPException(status_code=404, detail="Peer not found")

    key = db.query(VPNKey).get(peer.key_id)
    try:
        subprocess.run(
            [
                "wg",
                "set",
                WG_INTERFACE,
                "peer",
                key.public_key if key else peer.key.public_key,
                "remove",
            ],
            check=True,
        )
        if key:
            key.is_allocated = False
        db.delete(peer)
        db.commit()
    except subprocess.CalledProcessError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to revoke WireGuard peer"
        ) from exc

def generate_config(key: VPNKey, server: VPNServer) -> str:
    server_public_key = getattr(server, "public_key", "SERVER_PUBLIC_KEY")
    return (
        f"[Interface]\n"
        f"PrivateKey = {key.private_key}\n"
        f"Address = {key.ip_address}/32\n\n"
        f"[Peer]\n"
        f"PublicKey = {server_public_key}\n"
        f"Endpoint = {server.ip_address}:51820\n"
        f"AllowedIPs = 0.0.0.0/0"
    )

from sqlalchemy.orm import Session
from app.models.vpn.vpn_server import VPNServer
from app.schemas.vpn.vpn_server import VPNServerCreate, VPNServerUpdate
from typing import List


def create_vpn_server(db: Session, server_data: VPNServerCreate) -> VPNServer:
    server = VPNServer(**server_data.dict())
    db.add(server)
    db.commit()
    db.refresh(server)
    return server


def get_all_vpn_servers(db: Session) -> List[VPNServer]:
    return db.query(VPNServer).all()


def get_vpn_server_by_id(db: Session, server_id: int) -> VPNServer | None:
    return db.query(VPNServer).filter(VPNServer.id == server_id).first()


def update_vpn_server(db: Session, server_id: int, update_data: VPNServerUpdate) -> VPNServer | None:
    server = get_vpn_server_by_id(db, server_id)
    if not server:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(server, key, value)
    db.commit()
    db.refresh(server)
    return server


def delete_vpn_server(db: Session, server_id: int) -> bool:
    server = get_vpn_server_by_id(db, server_id)
    if not server:
        return False
    db.delete(server)
    db.commit()
    return True

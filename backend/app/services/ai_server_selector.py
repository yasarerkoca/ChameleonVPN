from typing import List, Optional
from app.models.vpn.vpn_server import VPNServer
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.logs.ai_server_selection_log_crud import log_ai_selection


def calculate_server_score(
    load_ratio: float,
    latency_ms: Optional[int],
    country_match: bool,
    uptime_seconds: Optional[int] = None,
    blacklist_penalty: bool = False
) -> float:
    score = 0.0
    score += max(0, 100 - load_ratio)
    score += max(0, 100 - (latency_ms or 100))
    score += 20 if country_match else 0
    score += min(uptime_seconds / 1000, 10) if uptime_seconds else 0
    score -= 50 if blacklist_penalty else 0
    return score


def rank_servers(
    user_country_code: str,
    servers: List[VPNServer],
    db: Session,
    user_ip: str
) -> List[VPNServer]:
    scored = []
    now = datetime.utcnow()

    for server in servers:
        uptime = (now - server.created_at).total_seconds() if server.created_at else None
        country_match = (server.country_code == user_country_code)
        score = calculate_server_score(
            load_ratio=server.load_ratio or 0,
            latency_ms=server.last_ping or 100,
            country_match=country_match,
            uptime_seconds=uptime,
            blacklist_penalty=server.is_blacklisted if hasattr(server, "is_blacklisted") else False
        )
        reason = (
            f"Load: {server.load_ratio} | Ping: {server.last_ping} | "
            f"Match: {country_match} | Blacklisted: {server.is_blacklisted}"
        )
        scored.append((server, score, reason))

    # En iyi sunucuyu logla
    if scored:
        top = max(scored, key=lambda x: x[1])
        log_ai_selection(
            db=db,
            user_ip=user_ip,
            selected_server_id=top[0].id,
            score=top[1],
            country=user_country_code,
            reason=top[2]
        )

    return [s[0] for s in sorted(scored, key=lambda x: x[1], reverse=True)]


def get_best_vpn_server(
    db: Session,
    user_ip: str,
    user_country_code: Optional[str] = None
) -> Optional[VPNServer]:
    """
    Kullanıcının IP'sine göre en uygun VPN sunucusunu getir.
    """
    query = db.query(VPNServer).filter(VPNServer.status == "active", VPNServer.is_blacklisted == False)

    if user_country_code:
        query = query.filter(VPNServer.country_code == user_country_code)

    servers = query.all()

    if not servers:
        return None

    ranked = rank_servers(user_country_code or "", servers, db, user_ip)
    return ranked[0] if ranked else None

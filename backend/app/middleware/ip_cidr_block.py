# ~/ChameleonVPN/backend/app/middleware/ip_cidr_block.py
import ipaddress
import os
import time
from typing import Optional, List

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .common import should_bypass

# DB yardımcıları isteğe bağlı import — yoksa middleware no-op davranır
try:
    from app.utils.db.db_utils import get_db  # generator (yield) döner
    from app.models.security.blocked_ip_range import BlockedIPRange
except Exception:
    get_db = None           # type: ignore
    BlockedIPRange = None   # type: ignore

# Basit bellek içi cache (CIDR -> ip_network)
_CACHE_TTL = int(os.getenv("CIDR_CACHE_TTL", "30"))
_CACHE = {"ts": 0.0, "networks": []}  # type: ignore[dict-item]


class IPCIDRBlockMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Sağlık/dokümantasyon gibi bypass edilecek uçlar
        if should_bypass(request):
            return await call_next(request)

        # Middleware devre dışı mı veya DB yok mu? Akışı bozma
        if (
            os.getenv("CIDR_BLOCK_ENABLED", "1").lower() in ("0", "false", "no")
            or not (get_db and BlockedIPRange)
        ):
            return await call_next(request)

        client_ip = request.client.host if request.client else "0.0.0.0"
        try:
            ip_obj = ipaddress.ip_address(client_ip)
        except Exception:
            # Şüpheli IP formatı — engellemeyelim
            return await call_next(request)

        # Cache süresi dolduysa CIDR'ları DB'den çek
        now = time.time()
        if now - _CACHE["ts"] > _CACHE_TTL or not _CACHE["networks"]:
            try:
                # get_db() bir generator; next() ile session alıp close() ile finalize edeceğiz
                gen = get_db()                   # type: ignore[call-arg]
                db = next(gen)                   # type: ignore[misc]
                try:
                    cidrs: List[str] = [row.cidr for row in db.query(BlockedIPRange.cidr).all()]  # type: ignore[attr-defined]
                finally:
                    try:
                        gen.close()  # type: ignore[attr-defined]
                    except Exception:
                        pass

                networks = []
                for c in cidrs:
                    try:
                        networks.append(ipaddress.ip_network(c, strict=False))
                    except Exception:
                        # Hatalı CIDR kaydını atla
                        continue

                _CACHE["networks"] = networks
                _CACHE["ts"] = now
            except Exception:
                # DB/parse hatasında trafiği kesmeyelim
                return await call_next(request)

        # Üye olduğu bir ağ varsa engelle
        for net in _CACHE["networks"]:
            try:
                if ip_obj in net:
                    return JSONResponse(
                        status_code=403,
                        content={"detail": "Erişiminiz IP aralığı nedeniyle engellendi."},
                    )
            except Exception:
                continue

        return await call_next(request)


# Eski kullanım için fonksiyon sarmalayıcı (opsiyonel)
async def ip_cidr_block_middleware(request, call_next):
    return await IPCIDRBlockMiddleware(None).dispatch(request, call_next)

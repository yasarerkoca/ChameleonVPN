# ~/ChameleonVPN/backend/app/middleware/ip_cidr_block.py

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import ipaddress

from app.utils.db.db_utils import get_db
from app.models.security.blocked_ip_range import BlockedIPRange

class IPCIDRBlockMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        db = next(get_db())
        blocked_ranges = db.query(BlockedIPRange).all()
        for ipr in blocked_ranges:
            try:
                if ipaddress.ip_address(client_ip) in ipaddress.ip_network(ipr.cidr):
                    return JSONResponse(status_code=403, content={"detail": "Erişiminiz IP aralığı nedeniyle engellendi."})
            except Exception:
                continue
        return await call_next(request)

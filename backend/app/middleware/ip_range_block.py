# ~/ChameleonVPN/backend/app/middleware/ip_range_block.py

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.db.db_utils import get_db
from app.crud.security.blocked_ip_range_crud import get_all_blocked_ip_ranges
import ipaddress

class IPRangeBlockMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        db = next(get_db())
        blocked_ranges = get_all_blocked_ip_ranges(db)
        for blocked in blocked_ranges:
            try:
                if ipaddress.ip_address(ip) in ipaddress.ip_network(blocked.cidr):
                    return JSONResponse(status_code=403, content={"detail": "IP adresiniz bloklu bir aralıkta. Erişim engellendi."})
            except Exception:
                continue
        return await call_next(request)

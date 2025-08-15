SKIP_PATHS={"/docs","/openapi.json","/redoc","/metrics"}
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.utils.db.db_utils import get_db
from app.crud.security.blocked_ip_crud import is_ip_blocked

class IPBlockMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        db_gen = get_db()
        db = next(db_gen)
        client_ip = request.client.host
        if is_ip_blocked(db, client_ip):
            db.close()
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "IP adresiniz geçici olarak engellendi."}
            )
        response = await call_next(request)
        db.close()
        return response

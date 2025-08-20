"""HTTP request/response logging middleware."""

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from .logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Logs basic information about each request and response."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        logger.info(f"⬅️ {request.method} {request.url.path}")

        try:
            response = await call_next(request)
        except Exception as exc:  # pragma: no cover - log then re-raise
            logger.exception(
                f"❌ {request.method} {request.url.path} failed: {exc}"  # noqa: BLE001
            )
            raise

        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"➡️ {request.method} {request.url.path} "
            f"{response.status_code} {process_time:.2f}ms"
        )
        return response

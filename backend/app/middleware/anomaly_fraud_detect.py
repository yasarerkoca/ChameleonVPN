from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .common import should_bypass

class AnomalyFraudDetectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if should_bypass(request):
            return await call_next(request)
        try:
            # Davranış / anomali analizi (şimdilik no-op)
            return await call_next(request)
        except Exception:
            return await call_next(request)

async def anomaly_fraud_detect_middleware(request, call_next):
    return await AnomalyFraudDetectMiddleware(None).dispatch(request, call_next)

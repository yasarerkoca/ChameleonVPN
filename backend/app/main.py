from fastapi import FastAPI, Depends, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from prometheus_fastapi_instrumentator import Instrumentator

from app.middleware.api_key_log import APIKeyAccessLogger
from app.middleware.ip_cidr_block import IPCIDRBlockMiddleware
from app.middleware.ip_block import IPBlockMiddleware
from app.middleware.geoip_block import geoip_block_middleware
from app.middleware.mfa_enforce import MFAEnforceMiddleware
from app.middleware.login_bruteforce import LoginBruteForceMiddleware
from app.middleware.anomaly_fraud_detect import AnomalyFraudDetectMiddleware
from app.middleware.session_hijack import SessionHijackMiddleware
from app.middleware.mfa_required import MFARequiredMiddleware
from app.middleware.mfa_enforcement import MFAEnforcementMiddleware
from app.logs.log_middleware import LoggingMiddleware
from app.logs.logger import logger
from app.routers import include_routers
from app.events import register_startup_events, register_shutdown_events

import redis.asyncio as aioredis  # GÜNCEL
import os

app = FastAPI(
    title="ChameleonVPN API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

Instrumentator().instrument(app).expose(app)

# 🌐 Global Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(MFAEnforceMiddleware)
app.add_middleware(IPCIDRBlockMiddleware)
app.add_middleware(APIKeyAccessLogger)
app.add_middleware(IPBlockMiddleware)
app.add_middleware(LoginBruteForceMiddleware)
app.add_middleware(AnomalyFraudDetectMiddleware)
app.add_middleware(SessionHijackMiddleware)
app.add_middleware(MFARequiredMiddleware)
app.add_middleware(MFAEnforcementMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "dev-secret")
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(geoip_block_middleware)

logger.info("🚀 ChameleonVPN backend initialized")
register_startup_events(app)
register_shutdown_events(app)

@app.on_event("startup")
async def setup_redis_limiter():
    redis = aioredis.from_url(
        os.getenv("REDIS_URL", "redis://redis:6379"),
        encoding="utf-8",
        decode_responses=True
    )
    await FastAPILimiter.init(redis)
    logger.info("✅ Redis bağlantısı ve RateLimiter başlatıldı")

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    logger.exception(f"❌ {request.method} {request.url.path} hatası: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Lütfen sistem yöneticisine başvurun."}
    )

# 🔗 Router'lar
include_routers(app)

# 📦 APK İndirme Endpoint'i
@app.get("/download/apk", tags=["Utility"])
def download_apk():
    apk_path = "/home/yasarerkoca/chameleon_vpn_client/build/app/outputs/flutter-apk/app-release.apk"
    if not os.path.exists(apk_path):
        logger.warning("📦 APK dosyası bulunamadı.")
        return JSONResponse(status_code=404, content={"detail": "APK bulunamadı."})
    return FileResponse(
        apk_path,
        media_type="application/vnd.android.package-archive",
        filename="chameleon_vpn.apk"
    )

# 🧪 Rate Limit Test Endpoint'i
@app.get("/test-limit", dependencies=[Depends(RateLimiter(times=5, seconds=60))], tags=["Utility"])
async def test_limit():
    logger.info("✅ Rate limit test çağrıldı")
    return {"msg": "Rate limit testi başarılı!"}

# 🌱 Sağlık Kontrolü
@app.get("/", tags=["Root"])
def root():
    logger.info("🏠 Root endpoint çağrıldı")
    return {"message": "ChameleonVPN API running!"}

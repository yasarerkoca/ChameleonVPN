# ~/ChameleonVPN/backend/app/main.py
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse   # FileResponse KALDIRILDI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.routing import APIRoute
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from prometheus_fastapi_instrumentator import Instrumentator
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app.config.base import settings
from app.middleware.api_key_log import APIKeyAccessLogger
from app.middleware.ip_cidr_block import IPCIDRBlockMiddleware
from app.middleware.ip_block import IPBlockMiddleware
from app.middleware.geoip_block import geoip_block_middleware
from app.middleware.mfa_enforce import MFAEnforceMiddleware
from app.middleware.login_bruteforce import LoginBruteForceMiddleware
from app.middleware.anomaly_fraud_detect import AnomalyFraudDetectMiddleware
from app.middleware.session_hijack import SessionHijackMiddleware
from app.logs.log_middleware import LoggingMiddleware
from app.logs.logger import logger
from app.routers import include_routers
from app.events.startup_events import register_startup_events
from app.events.shutdown_events import register_shutdown_events

import redis.asyncio as aioredis

# Sentry APM
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[FastApiIntegration()],
    )

# --- OpenAPI'de benzersiz operationId üretimi ---
def gen_unique_id(route: APIRoute) -> str:
    method = (list(route.methods)[0].lower() if route.methods else "get")
    tag = (route.tags[0] if route.tags else "default").replace(" ", "_")
    name = (route.name or "unknown").replace(" ", "_")
    path = (
        route.path.replace("/", "_")
        .strip("_")
        .replace("{", "")
        .replace("}", "")
    )
    return f"{method}_{tag}_{name}_{path}"
# -------------------------------------------------

app = FastAPI(
    title="ChameleonVPN API",
    version=settings.VERSION,
    docs_url="/docs" if settings.ENABLE_DOCS else None,
    redoc_url="/redoc" if settings.ENABLE_DOCS else None,
    openapi_url="/openapi.json" if settings.ENABLE_DOCS else None,
    generate_unique_id_function=gen_unique_id,
)

@app.get("/healthz")
async def healthz():
    return {"ok": True}

# Prometheus /metrics
Instrumentator().instrument(app).expose(app)

# CORS (Settings üzerinden normalize liste)
_cors = settings.cors_origins()
_allow_all = (len(_cors) == 1 and _cors[0] == "*")
allow_credentials = not _allow_all

# 🌐 Global Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(MFAEnforceMiddleware)
app.add_middleware(IPCIDRBlockMiddleware)
app.add_middleware(APIKeyAccessLogger)
app.add_middleware(IPBlockMiddleware)
app.add_middleware(LoginBruteForceMiddleware)
app.add_middleware(AnomalyFraudDetectMiddleware)
app.add_middleware(SessionHijackMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fonksiyonel middleware (GeoIP engelleme)
app.middleware("http")(geoip_block_middleware)

logger.info("🚀 ChameleonVPN backend initialized")
register_startup_events(app)
register_shutdown_events(app)

@app.on_event("startup")
async def setup_redis_limiter():
    redis = aioredis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(redis)
    logger.info("✅ Redis bağlantısı ve RateLimiter başlatıldı")

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    logger.exception(f"❌ {request.method} {request.url.path} hatası: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Lütfen sistem yöneticisine başvurun."},
    )

# 🔗 Router'lar
include_routers(app)

# 📦 APK İndirme Endpoint'i — KALDIRILDI, 410 GONE ile korunuyor
@app.get("/download/apk", tags=["Utility"])
def download_apk_gone():
    # Resmi mağazalar dışı dağıtım YASAK
    raise HTTPException(status_code=410, detail="Use official store links.")

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

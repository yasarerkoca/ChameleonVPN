# ~/ChameleonVPN/backend/app/config/base.py

from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, ValidationError
import os
import json

class Settings(BaseSettings):
    """
    Uygulama yapılandırması (.env + ortam değişkenleri).
    - extra="ignore": Tanımsız ENV anahtarları hata çıkarmaz.
    - case_sensitive=False: ENV adları büyük/küçük harf duyarsız.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- Veritabanı ---
    DATABASE_URL: str

    # --- JWT / Token ---
    SECRET_KEY: str                    # ZORUNLU (>=16)
    ALGORITHM: str = "HS256"           # .env: JWT_ALGO ile override edilir
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- Session ---
    SESSION_SECRET_KEY: str            # ZORUNLU (>=16)

    # --- Redis ---
    REDIS_URL: str = "redis://redis:6379/0"

    # --- CORS ---
    # JSON dizesi ('["https://a.com","https://b.com"]') veya CSV ("https://a.com,https://b.com")
    ALLOWED_ORIGINS: str = "*"

    # --- App bayrakları ---
    DEBUG: bool = False
    ENABLE_DOCS: bool = True
    UVICORN_WORKERS: int = 2

    # --- SMTP (opsiyonel) ---
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASS: Optional[str] = None
    SMTP_FROM: Optional[str] = None

    # --- Stripe (opsiyonel) ---
    STRIPE_API_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None

    # --- Google OAuth (opsiyonel) ---
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: Optional[str] = None

    # ---- Validators ----
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def database_url_alias(cls, v):
        # DB_URL alias desteği (varsa kullan)
        if (v is None or str(v).strip() == "") and os.getenv("DB_URL"):
            return os.getenv("DB_URL")
        if isinstance(v, str) and v.strip():
            return v
        raise ValueError("DATABASE_URL must be set (or DB_URL alias).")

    @field_validator("SECRET_KEY", "SESSION_SECRET_KEY", mode="before")
    @classmethod
    def validate_secret_keys(cls, v):
        if isinstance(v, str) and len(v.strip()) >= 16:
            return v.strip()
        raise ValueError("SECRET_KEY/SESSION_SECRET_KEY must be >= 16 characters.")

    @field_validator("ALGORITHM", mode="before")
    @classmethod
    def normalize_algo(cls, v):
        # JWT_ALGO varsa ALGORITHM'i override et
        return os.getenv("JWT_ALGO", v or "HS256")

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def normalize_allowed_origins(cls, v):
        # JSON list -> CSV, list -> CSV, diğerleri aynen
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("[") and s.endswith("]"):
                try:
                    arr = json.loads(s)
                    if isinstance(arr, list):
                        return ",".join(arr)
                except Exception:
                    return s
            return s or "*"
        elif isinstance(v, list):
            return ",".join(v)
        return "*"

    # FastAPI CORSMiddleware için liste döndür
    def cors_origins(self) -> List[str]:
        raw = (self.ALLOWED_ORIGINS or "").strip()
        if raw in ("", "*"):
            return ["*"]
        return [o.strip() for o in raw.split(",") if o.strip()]
try:
    settings = Settings()
except ValidationError as e:
    missing = ", ".join(err["loc"][0] for err in e.errors())
    raise RuntimeError(
        f"Kritik ortam değişkenleri eksik: {missing}. Lütfen .env dosyanızda bu değerleri tanımlayın."
    ) from e

if settings.SECRET_KEY in ("", "dev-secret"):
    raise RuntimeError(
        "Kritik ortam değişkeni eksik: SECRET_KEY. Lütfen .env dosyanızda güvenli bir SECRET_KEY belirleyin."
    )

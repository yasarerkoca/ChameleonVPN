# ~/ChameleonVPN/backend/app/config/base.py

from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
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
    SECRET_KEY: str = "dev-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Opsiyonel ayrı JWT alanları
    JWT_SECRET_KEY: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

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

    # --- Redis ---
    REDIS_URL: str = "redis://redis:6379"

    # --- CORS ---
    # .env'de JSON dizesi ('["https://a.com","https://b.com"]') veya CSV ("https://a.com,https://b.com")
    # tutulabilir. Aşağıdaki validator hepsini CSV stringe normalize eder; cors_origins() liste döndürür.
    ALLOWED_ORIGINS: str = "*"

    # --- Ek bayraklar ---
    ENABLE_DOCS: bool = True
    UVICORN_WORKERS: int = 2

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

    # FastAPI CORSMiddleware için kullanılacak liste
    def cors_origins(self) -> List[str]:
        raw = (self.ALLOWED_ORIGINS or "").strip()
        if raw in ("", "*"):
            return ["*"]
        return [o.strip() for o in raw.split(",") if o.strip()]


settings = Settings()

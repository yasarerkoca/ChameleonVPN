# ~/ChameleonVPN/backend/app/config/base.py
import os
import json
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, ValidationError


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- Veritabanı ---
    DATABASE_URL: str

    # --- JWT / Token ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 60
    EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # --- Session ---
    SESSION_SECRET_KEY: str

    # --- Redis ---
    REDIS_URL: str = "redis://redis:6379/0"

    # --- CORS ---
    ALLOWED_ORIGINS: str = ""

    # --- App bayrakları ---
    PROJECT_NAME: str = "ChameleonVPN"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENABLE_DOCS: bool = True
    UVICORN_WORKERS: int = 2

    # --- Varsayılan Yönetici ---
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

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

    # --- Sentry (opsiyonel) ---
    SENTRY_DSN: Optional[str] = None

    # --- URL configuration ---
    PASSWORD_RESET_URL: str
    EMAIL_VERIFY_URL: str

    # ---- Validators ----
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def database_url_must_exist(cls, v):
        if isinstance(v, str) and v.strip():
            return v.strip()
        raise ValueError("DATABASE_URL must be set in .env file.")

    @field_validator("SECRET_KEY", "SESSION_SECRET_KEY", mode="before")
    @classmethod
    def validate_secret_keys(cls, v):
        if isinstance(v, str) and len(v.strip()) >= 16:
            return v.strip()
        raise ValueError("SECRET_KEY/SESSION_SECRET_KEY must be >= 16 characters.")

    @field_validator("PASSWORD_RESET_URL", "EMAIL_VERIFY_URL", mode="before")
    @classmethod
    def validate_base_urls(cls, v):
        if isinstance(v, str) and v.strip():
            return v.strip()
        raise ValueError("PASSWORD_RESET_URL/EMAIL_VERIFY_URL must be set.")

    @field_validator("ALGORITHM", mode="before")
    @classmethod
    def normalize_algo(cls, v):
        return os.getenv("JWT_ALGO", v or "HS256")

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def normalize_allowed_origins(cls, v):
        if v is None:
            raise ValueError("ALLOWED_ORIGINS must be set.")
        if isinstance(v, str):
            s = v.strip()
            if not s:
                raise ValueError("ALLOWED_ORIGINS must be set.")
            if s.startswith("[") and s.endswith("]"):
                try:
                    arr = json.loads(s)
                    if isinstance(arr, list):
                        return ",".join(arr)
                except Exception:
                    return s
            return s
        elif isinstance(v, list):
            if not v:
                raise ValueError("ALLOWED_ORIGINS must be set.")
            return ",".join(v)
        raise ValueError("ALLOWED_ORIGINS must be a string or list.")

    @field_validator("ADMIN_EMAIL", "ADMIN_PASSWORD", mode="before")
    @classmethod
    def validate_admin_credentials(cls, v):
        if isinstance(v, str) and v.strip():
            return v.strip()
        raise ValueError("ADMIN_EMAIL/ADMIN_PASSWORD must be set and non-empty.")

    def cors_origins(self) -> List[str]:
        raw = (self.ALLOWED_ORIGINS or "").strip()
        if raw == "*":
            return ["*"]
        return [o.strip() for o in raw.split(",") if o.strip()]


try:
    settings = Settings()
except ValidationError as e:
    missing = ", ".join(err["loc"][0] for err in e.errors())
    raise RuntimeError(
        f"Kritik ortam değişkenleri eksik: {missing}. Lütfen backend/.env dosyanızda bu değerleri tanımlayın."
    ) from e

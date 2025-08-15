from pydantic_settings import BaseSettings

class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 💥 Fazla .env değişkenlerini yok sayar

jwt_settings = JWTSettings()

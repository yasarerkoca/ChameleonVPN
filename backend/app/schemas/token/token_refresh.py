from pydantic import BaseModel, Field


class TokenRefresh(BaseModel):
    """
    Access token yenileme isteği için refresh token taşıyan input şeması.

    Attributes:
        refresh_token (str): Kullanıcının geçerli refresh token'ı.
    """
    refresh_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR...")

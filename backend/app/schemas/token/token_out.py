from pydantic import BaseModel, Field


class TokenOut(BaseModel):
    """
    Access ve refresh token bilgisinin çıktı (response) şeması.

    Attributes:
        access_token (str): JWT access token.
        refresh_token (str): JWT refresh token.
        token_type (str): Token türü ("bearer").
    """
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR...")
    refresh_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR...")
    token_type: str = Field(default="bearer", example="bearer")

"""Authentication service package exports."""

from .firebase import get_or_create_user_from_firebase, verify_id_token
from .firebase_routes import (
    FirebaseLoginIn,
    TokenOut,
    firebase_login,
    router,
)

__all__ = [
    "verify_id_token",
    "get_or_create_user_from_firebase",
    "FirebaseLoginIn",
    "TokenOut",
    "firebase_login",
    "router",
]

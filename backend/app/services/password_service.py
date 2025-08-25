from passlib.hash import bcrypt


def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt."""
    return bcrypt.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the given hash."""
    return bcrypt.verify(plain_password, hashed_password)


__all__ = ["hash_password", "verify_password"]


from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
import re, secrets
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
BLACKLIST = set()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    if not is_strong_password(password):
        raise ValueError("Şifre yeterince güçlü değil!")
    return pwd_context.hash(password)
def is_strong_password(password):
    return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$', password))
def create_access_token(data: dict, expires_minutes: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "iss": "chameleonvpn", "aud": "chameleonvpn_users"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "iss": "chameleonvpn", "aud": "chameleonvpn_users", "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
def decode_token(token: str, audience="chameleonvpn_users"):
    if token in BLACKLIST:
        raise JWTError("Token blacklisted!")
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience=audience, issuer="chameleonvpn")
def revoke_token(token: str):
    BLACKLIST.add(token)
def generate_token():
    return secrets.token_urlsafe(32)
    
import os
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")
SECRET_KEY = os.getenv("SECRET_KEY", "very_insecure_dev_key")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
ALGORITHM = os.getenv("ALGORITHM", "HS256")
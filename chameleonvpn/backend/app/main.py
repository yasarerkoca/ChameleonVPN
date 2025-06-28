
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, vpn, admin
from app.database import Base, engine
import os

app = FastAPI(title="ChameleonVPN Backend")

if os.environ.get("ENV", "dev") == "dev":
    Base.metadata.create_all(bind=engine)

ALLOWED_ORIGINS = [
    "https://frontend.sizinsite.com",
    "https://admin.sizinsite.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if os.environ.get("ENV") == "prod" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(vpn.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"msg": "ChameleonVPN API running"}

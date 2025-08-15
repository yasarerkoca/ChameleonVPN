import geoip2.database
from fastapi import Request, HTTPException
import os

# Mutlak yol kullanımı
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "geoipdb", "GeoLite2-Country.mmdb")
reader = geoip2.database.Reader(DB_PATH)

ALLOWED_COUNTRIES = {"US", "DE", "TR"}  # Ayarlanabilir whitelist

async def geoip_block_middleware(request: Request, call_next):
    ip = request.client.host
    try:
        response = reader.country(ip)
        country = response.country.iso_code
        if country not in ALLOWED_COUNTRIES:
            raise HTTPException(status_code=403, detail="Access restricted by GeoIP")
    except Exception:
        # GeoIP servis hatası varsa engelleme
        pass
    return await call_next(request)

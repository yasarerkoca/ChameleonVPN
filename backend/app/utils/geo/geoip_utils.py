import geoip2.database
import os

# Proje kökünden geoipdb yolunu güvenli şekilde al
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "geoipdb", "GeoLite2-Country.mmdb")

# GeoIP reader global olarak başlat
reader = geoip2.database.Reader(DB_PATH)

def get_country_by_ip(ip_address: str) -> str:
    """
    IP adresine göre ülke kodunu (ISO alpha-2) döner.
    Örnek: 'TR', 'DE', 'US'
    """
    try:
        response = reader.country(ip_address)
        return response.country.iso_code or "UNKNOWN"
    except Exception:
        return "UNKNOWN"

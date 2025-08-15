from fastapi import APIRouter, Request

router = APIRouter(prefix="/test", tags=["monitor"])

@router.get("/dnsleak", summary="DNS leak testi için rehber endpoint")
def dns_leak_check(request: Request):
    client_ip = request.client.host
    return {
        "client_ip": client_ip,
        "test_url": "https://www.dnsleaktest.com",
        "note": "VPN ile bağlıyken bu sitede sadece internal DNS görünmeli (10.8.0.1)!"
    }

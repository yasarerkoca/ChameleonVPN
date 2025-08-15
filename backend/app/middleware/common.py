from starlette.requests import Request

SKIP_PATHS = {"/docs", "/openapi.json", "/redoc", "/metrics", "/healthz"}
def should_bypass(request: Request) -> bool:
    p = request.url.path
    return p in SKIP_PATHS or p.startswith("/static")

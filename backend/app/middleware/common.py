from starlette.requests import Request

SKIP_PATHS = {
    "/docs", "/openapi.json", "/redoc", "/metrics", "/healthz",
    "/favicon.ico", "/"
}
def should_bypass(request: Request) -> bool:
    p = request.url.path
    # statik dosyalar / assets
    return p in SKIP_PATHS or p.startswith("/static") or p.startswith("/assets")

#!/usr/bin/env sh
set -euo pipefail
cd /srv

echo "Starting backend (no alembic on startup)…"

# 1) Uygulama import edilebiliyor mu? (stack trace göster)
python - <<'PY'
import traceback, sys
try:
    import app.main  # sadece import; Uvicorn'u aşağıda başlatacağız
    print("import_ok")
except Exception:
    print("IMPORT_ERROR ↓↓↓", file=sys.stderr)
    traceback.print_exc()
    sys.exit(1)
PY

# 2) Uvicorn'u başlat
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info

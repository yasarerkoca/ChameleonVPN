#!/usr/bin/env sh
set -e

echo "==> Alembic upgrade (retry)..."
EC=1
for i in $(seq 1 30); do
  if alembic -c /srv/alembic.ini upgrade head; then
    EC=0; break
  fi
  echo "alembic retry $i/30"; sleep 3
done
[ "$EC" -ne 0 ] && echo "Alembic failed" && exit "$EC"

echo "==> Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

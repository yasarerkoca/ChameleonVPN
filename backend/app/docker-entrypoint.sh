#!/usr/bin/env sh
set -e

echo "==> Alembic upgrade head"
# DB ayağa kalkmadan hata verebilir; kısa retry ile deneyelim
for i in $(seq 1 20); do
  if alembic -c /srv/app/alembic.ini upgrade head; then
    break
  fi
  echo "alembic retry $i/20"; sleep 2
done

echo "==> Start Uvicorn"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

#!/usr/bin/env bash
set -euo pipefail

MSG="${1:-auto migration}"
ROOT="$(cd "$(dirname "$0")/.."; pwd)"

cd "$ROOT"
echo "==> DB/Redis"
docker-compose up -d db redis

echo "==> DB'yi HEAD'e yükselt"
docker-compose run --rm --entrypoint bash backend -lc \
  "cd /srv && alembic -c alembic.ini upgrade head"

echo "==> Senkron kontrol"
CURR=$(docker-compose run --rm --entrypoint bash backend -lc \
  "cd /srv && alembic -c alembic.ini current --verbose | awk '/Rev:/{print \$2}'" | tr -d '\r')
HEAD=$(docker-compose run --rm --entrypoint bash backend -lc \
  "cd /srv && alembic -c alembic.ini heads --verbose | awk '/Rev:/{print \$2}'" | tr -d '\r')

echo "current=$CURR head=$HEAD"
if [ -z "$CURR" ] || [ "$CURR" != "$HEAD" ]; then
  echo "DB HEAD değil (veya boş). Önce HEAD'e yükseltildi; yeniden çalıştırın."
  exit 1
fi

echo "==> Autogenerate (yalnızca farklar)"
docker-compose run --rm \
  -v "$PWD/backend/alembic/versions:/srv/alembic/versions" \
  --entrypoint bash backend -lc \
  "cd /srv && alembic -c alembic.ini revision --autogenerate -m \"$MSG\""

echo "==> Upgrade head"
docker-compose run --rm --entrypoint bash backend -lc \
  "cd /srv && alembic -c alembic.ini upgrade head"

echo "==> Servisleri yenile"
fuser -k 8000/tcp || true
docker-compose up -d --build
docker-compose ps

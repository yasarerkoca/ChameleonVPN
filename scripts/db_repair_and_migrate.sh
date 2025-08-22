#chmod +x scripts/db_repair_and_migrate.sh
#./scripts/db_repair_and_migrate.sh

#!/usr/bin/env bash
set -euo pipefail

BASE="beb3b7fa379b"

echo "==> Kill port 8000 (varsa)"
fuser -k 8000/tcp || true

echo "==> DB & Redis up"
docker-compose up -d db redis

echo "==> Durum kontrol"
HAS_AV=$(docker-compose exec -T db psql -U vpnadmin -d chameleonvpn -tAc "SELECT CASE WHEN to_regclass('public.alembic_version') IS NULL THEN 0 ELSE 1 END")
HAS_ROLES=$(docker-compose exec -T db psql -U vpnadmin -d chameleonvpn -tAc "SELECT CASE WHEN to_regclass('public.roles') IS NULL THEN 0 ELSE 1 END")
HAS_AFR=$(docker-compose exec -T db psql -U vpnadmin -d chameleonvpn -tAc "SELECT CASE WHEN to_regclass('public.anomaly_fraud_records') IS NULL THEN 0 ELSE 1 END")

echo "alembic_version:$HAS_AV roles:$HAS_ROLES anomaly_fraud_records:$HAS_AFR"

if [ "$HAS_AV" -eq 0 ] && { [ "$HAS_ROLES" -eq 1 ] || [ "$HAS_AFR" -eq 1 ]; }; then
  echo "==> Tablolar var ama alembic_version yok -> STAMP $BASE"
  docker-compose run --rm --entrypoint bash backend -lc "cd /srv && alembic -c alembic.ini stamp $BASE"
elif [ "$HAS_AV" -eq 0 ] && [ "$HAS_ROLES" -eq 0 ] && [ "$HAS_AFR" -eq 0 ]; then
  echo "==> Boş şema -> UPGRADE $BASE"
  docker-compose run --rm --entrypoint bash backend -lc "cd /srv && alembic -c alembic.ini upgrade $BASE"
else
  echo "==> alembic_version mevcut -> devam"
fi

echo "==> HEAD'e yükselt"
docker-compose run --rm --entrypoint bash backend -lc "cd /srv && alembic -c alembic.ini upgrade head"

echo "==> Servisleri başlat"
docker-compose up -d --build

echo "==> Healthcheck"
sleep 2
curl -fsS http://127.0.0.1/healthz || true
echo "==> Bitti."

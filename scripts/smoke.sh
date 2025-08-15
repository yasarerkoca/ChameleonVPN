#!/usr/bin/env bash
set -Eeuo pipefail

# --- Ayarlar ---
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"
BASE="http://${HOST}:${PORT}"
COMPOSE="${COMPOSE:-docker-compose}"

say() { printf "\n\033[1m▶ %s\033[0m\n" "$*"; }
ok()  { printf "   ✅ %s\n" "$*"; }
fail(){ printf "   ❌ %s\n" "$*"; exit 1; }

req() {
  local url="$1"; shift
  curl -sf --max-time 5 "$url" "$@"
}

code() {
  local url="$1"
  curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url"
}

# 1) Healthz
say "Healthz kontrolü"
resp="$(req "$BASE/healthz" || true)"
[[ "$resp" == *'"ok":true'* ]] || fail "/healthz ok:false döndü veya erişilemedi"
ok "/healthz OK"

# 2) Metrics
say "Prometheus /metrics kontrolü"
req "$BASE/metrics" >/dev/null || fail "/metrics erişilemedi"
ok "/metrics OK"

# 3) Docs (ENABLE_DOCS=true ise genelde açık)
say "Docs erişim kontrolü (varsa)"
if code "$BASE/docs" | grep -qE '200|401'; then
  ok "/docs erişilebilir"
else
  printf "   ℹ /docs kapalı olabilir (ENABLE_DOCS=false)\n"
fi

# 4) Rate limit testi
say "Rate limit testi (/test-limit, 60sn pencerede 5 istek)"
codes=""
for i in {1..6}; do
  c="$(code "$BASE/test-limit")"; codes="$codes $c"
done
echo "   Kodlar:$codes"
# Beklenti: 200 200 200 200 200 429 (sıra değişebilir ama en az bir 429 olmalı)
if echo "$codes" | grep -q "429"; then
  ok "Rate limit tetiklendi (429 görüldü)"
else
  printf "   ⚠ Rate limit tetiklenmedi; limiter yapılandırmasını kontrol et.\n"
fi

# 5) OpenAPI çekme ve operationId tekilliği (jq varsa)
say "OpenAPI ve operationId tekilliği"
req "$BASE/openapi.json" >/tmp/openapi.json || printf "   ℹ openapi.json alınamadı (docs kapalı olabilir)\n"
if command -v jq >/dev/null 2>&1 && [[ -s /tmp/openapi.json ]]; then
  dups="$(jq -r '
    [
      .paths[]? | to_entries[] |
      .value | to_entries[] |
      .value.operationId
    ] | group_by(.)[] | select(length>1) | .[0]
  ' /tmp/openapi.json || true)"
  if [[ -n "${dups:-}" ]]; then
    fail "Duplicate operationId bulundu: ${dups}"
  else
    ok "operationId’ler benzersiz"
  fi
else
  printf "   ℹ jq yok ya da openapi.json kapalı; tekillik atlandı\n"
fi

# 6) DB canlılığı ve tablo sayımı
say "PostgreSQL canlılık ve tablo sayısı"
$COMPOSE exec -T db psql -U vpnadmin -d chameleonvpn -c "SELECT 1;" >/dev/null || fail "DB SELECT 1 başarısız"
tables="$($COMPOSE exec -T db psql -U vpnadmin -d chameleonvpn -t -c \
  "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';" | tr -d '[:space:]')"
ok "DB canlı. public tablo sayısı: ${tables}"

# 7) Alembic head doğrulama
say "Alembic sürümü"
$COMPOSE exec -T backend alembic current || fail "alembic current çalışmadı"
ok "Alembic current çalıştı"

# 8) Redis roundtrip
say "Redis roundtrip"
$COMPOSE exec -T backend python - <<'PY'
import asyncio, os
import redis.asyncio as aioredis
async def main():
    r = aioredis.from_url(os.getenv("REDIS_URL","redis://redis:6379"), encoding="utf-8", decode_responses=True)
    await r.set("smoke:key","ok", ex=10)
    v = await r.get("smoke:key")
    print("value:", v)
asyncio.run(main())
PY
ok "Redis set/get OK"

say "Tüm smoke kontrolleri tamamlandı 🎉"

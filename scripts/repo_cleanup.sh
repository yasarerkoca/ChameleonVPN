#!/usr/bin/env bash
# repo_cleanup.sh — ChameleonVPN repo hijyeni + doğrulama + (opsiyonel) yeniden başlatma
set -Eeuo pipefail

trap 'echo "[X] Hata oldu. 8000 portunu boşaltıyorum..."; fuser -k 8000/tcp || true' ERR

# ---------- yardımcılar ----------
in_git() { git rev-parse --is-inside-work-tree >/dev/null 2>&1; }
try_move() { # try_move SRC DEST_DIR
  local src="$1" dst="$2"
  [[ -e "$src" || -d "$src" ]] || return 0
  mkdir -p "$dst"
  if in_git; then git mv -f "$src" "$dst" 2>/dev/null || mv -f "$src" "$dst"; else mv -f "$src" "$dst"; fi
}
try_rm() { # try_rm PATH
  if in_git && [[ -e "$1" || -d "$1" ]]; then git rm -r -f "$1" 2>/dev/null || rm -rf "$1"; else rm -rf "$1"; fi
}
ensure_line() { # ensure_line FILE "pattern"
  local file="$1" line="$2"
  touch "$file"; grep -qxF "$line" "$file" || echo "$line" >> "$file"
}

# ---------- köke geç ----------
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"
echo "[i] Repo kökü: $REPO"

mkdir -p archive

# 1) Backend içinde saçma dosyalar
mkdir -p archive/backend_misc
for p in 'backend/=' 'backend/=0.21' 'backend/[backend' 'backend/[backend]'; do
  [[ -e "$p" ]] && try_move "$p" "archive/backend_misc"
done

# 2) Firestore dosyaları → infra/firebase
mkdir -p infra/firebase
for f in firestore.indexes.json firestore.rules firebase.json; do
  [[ -f "backend/$f" ]] && try_move "backend/$f" "infra/firebase"
  [[ -f "$f" ]] && try_move "$f" "infra/firebase"
done

# 3) Legacy monorepo klasörü
if [[ -d chameleonvpn ]]; then
  ts="$(date +%Y%m%d_%H%M%S)"
  tar -czf "archive/monorepo_legacy_${ts}.tgz" chameleonvpn
  try_rm chameleonvpn
fi

# 4) Statik dosyalar → backend/app/static
mkdir -p backend/app/static
if [[ -d static ]]; then
  if compgen -G "static/*" >/dev/null; then
    # dosyalar varsa taşı
    if in_git; then
      # tek tek git mv, boşluklu adlar için güvenli
      while IFS= read -r -d '' item; do
        dst="backend/app/static/$(basename "$item")"
        git mv -f "$item" "backend/app/static/" 2>/dev/null || mv -f "$item" "backend/app/static/"
      done < <(find static -mindepth 1 -maxdepth 1 -print0)
    else
      mv -f static/* backend/app/static/ 2>/dev/null || true
    fi
  fi
  rmdir static 2>/dev/null || true
fi
touch backend/app/static/.gitkeep

# 5) db_backups → sistem dizini
if [[ -d db_backups ]]; then
  sudo mkdir -p /var/backups/chameleonvpn || mkdir -p /var/backups/chameleonvpn
  if command -v rsync >/dev/null 2>&1; then
    (sudo rsync -av db_backups/ /var/backups/chameleonvpn/ 2>/dev/null || rsync -av db_backups/ /var/backups/chameleonvpn/)
  else
    (sudo cp -a db_backups/. /var/backups/chameleonvpn/ 2>/dev/null || cp -a db_backups/. /var/backups/chameleonvpn/)
  fi
  try_rm db_backups
fi

# 6) frontend konsolidasyonu
mkdir -p frontend
[[ -d web-admin ]] && try_move web-admin frontend
[[ -d web-user  ]] && try_move web-user  frontend

# 7) Dokümantasyon iskeleti
mkdir -p docs/{adr,api,runbooks}
[[ -f docs/README.md ]] || cat > docs/README.md <<'MD'
# ChameleonVPN Docs
- `adr/` : Architecture Decision Records
- `api/` : API sözleşmeleri
- `runbooks/` : Operasyon rehberleri
MD
[[ -f docs/adr/0001-record-architecture.md ]] || cat > docs/adr/0001-record-architecture.md <<'MD'
# ADR-0001: Architecture is Documented
Tarih: '"$(date +%F)"'
Karar: Sistem mimarisi ADR'lerle kayıt altına alınır.
MD

# 8) Makefile (yedeğe al, sonra yaz)
if [[ -f Makefile ]]; then
  ts="$(date +%Y%m%d_%H%M%S)"
  cp Makefile "archive/Makefile.${ts}.bak"
fi
cat > Makefile <<'MK'
COMPOSE ?= docker compose

.PHONY: help backend-up backend-down backend-migrate mobile-build

help:
	@echo "Targets: backend-up | backend-down | backend-migrate | mobile-build"

backend-up:
	$(COMPOSE) up -d

backend-down:
	$(COMPOSE) down

backend-migrate:
	cd backend && alembic upgrade head

mobile-build:
	cd chameleon_vpn_client && flutter clean && flutter pub get && flutter build apk
MK

# 9) .gitignore rötuşları
ensure_line .gitignore ".venv/"
ensure_line .gitignore "logs/**.log"
ensure_line .gitignore "*.log"
ensure_line .gitignore "builds/"
ensure_line .gitignore "*.deb"
ensure_line .gitignore "archive/"
ensure_line .gitignore "/db_backups/"
ensure_line .gitignore "/var/backups/"
ensure_line .gitignore "alembic.log"

# 10) Git commit (varsa)
if in_git; then
  git add -A
  git commit -m "Repo hygiene: firebase→infra, legacy arşiv, static→backend, docs iskeleti, backups off-repo, frontend konsolidasyonu, .gitignore/Makefile" || true
fi

# 11) Doğrulama çıktıları
echo "---- DOĞRULAMA ----"
grep -R "web-admin\|web-user" -n . | grep -v "frontend/" || true
grep -R "static/" -n backend | grep -v "app/static" || true
grep -R "db_backups" -n . || true
grep -R "firestore\.rules\|firestore\.indexes\.json" -n . || true

# 12) (Opsiyonel) yeniden build + up
COMPOSE_CMD="$(command -v docker-compose >/dev/null 2>&1 && echo docker-compose || echo 'docker compose')"
if [[ -f docker-compose.yml || -f compose.yaml || -f docker-compose.yaml ]]; then
  echo "[i] Docker build ve up çalıştırılıyor..."
  eval "$COMPOSE_CMD build"
  fuser -k 8000/tcp || true
  eval "$COMPOSE_CMD up -d"
else
  echo "[i] Compose dosyası bulunamadı, docker adımı atlandı."
fi

echo "✅ Bitti. Hata görürsen önce: fuser -k 8000/tcp"

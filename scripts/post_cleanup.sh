#!/usr/bin/env bash
set -Eeuo pipefail

# 1) Makefile firebase-deploy: TAB ile düzelt
sed -i '/^firebase-deploy:$/,${s/^        /\t/}' Makefile || true

# 2) docs/example -> archive
mkdir -p archive/docs_examples
[ -d docs/example ] && (git mv docs/example archive/docs_examples 2>/dev/null || mv -f docs/example archive/docs_examples) || true
grep -qxF "archive/docs_examples/" .gitignore || echo "archive/docs_examples/" >> .gitignore

# 3) Grep için daha temiz alias önerileri (opsiyonel not)
# Kullanım: grep -R --binary-files=without-match --exclude-dir=.git --exclude-dir='**/flutter/ephemeral' 'aranan' -n .

# 4) Compose rebuild
COMPOSE_CMD="$(command -v docker-compose >/dev/null 2>&1 && echo docker-compose || echo 'docker compose')"
$COMPOSE_CMD build
fuser -k 8000/tcp || true
$COMPOSE_CMD up -d

echo "✅ post-cleanup bitti."

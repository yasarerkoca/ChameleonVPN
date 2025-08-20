#!/usr/bin/env bash
set -euo pipefail

# ==== Ayarlar ====
REPO_DIR="${REPO_DIR:-$HOME/ChameleonVPN}"
REMOTE_NAME="${REMOTE_NAME:-github}"
REMOTE_URL="${REMOTE_URL:-git@github.com:yasarerkoca/ChameleonVPN.git}"
FPR_EXPECTED="${FPR_EXPECTED:-SHA256:wcRqXvyr5V6LP7P6i/LQKWaSgUghpuk7xFwgR+KEOtk}"
ENV_BACKUP_DIR="${ENV_BACKUP_DIR:-$REPO_DIR/infra/secrets/env-backups}"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"

trap 'echo "HATA: Satır $LINENO başarısız." >&2' ERR

# ==== SSH anahtarı (fingerprint ile) ====
ID_FILE="${ID_FILE:-}"
if [[ -z "${ID_FILE}" ]]; then
  for pub in "$HOME"/.ssh/*.pub; do
    [[ -e "$pub" ]] || continue
    fpr="$(ssh-keygen -lf "$pub" -E sha256 | awk '{print $2}')"
    if [[ "$fpr" == "$FPR_EXPECTED" ]]; then ID_FILE="${pub%.pub}"; break; fi
  done
fi
[[ -z "${ID_FILE:-}" ]] && { echo "HATA: SSH key yok (ID_FILE verin)."; exit 1; }
chmod 600 "$ID_FILE" || true
export GIT_SSH_COMMAND="ssh -i $ID_FILE -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"

# ==== Repo hazırla ====
cd "$REPO_DIR"
git config --global --add safe.directory "$REPO_DIR" || true
git rev-parse --git-dir >/dev/null 2>&1 || git init -b main
git show-ref --verify --quiet refs/heads/main || git branch -M main
git remote get-url "$REMOTE_NAME" >/dev/null 2>&1 || git remote add "$REMOTE_NAME" "$REMOTE_URL"
git remote set-url "$REMOTE_NAME" "$REMOTE_URL"
git fetch "$REMOTE_NAME" || true
# local main 'unborn' ise remote/main'e sabitle
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  git checkout -B main "$REMOTE_NAME/main"
fi
git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1 || git branch --set-upstream-to="$REMOTE_NAME"/main main || true
git pull --rebase --autostash "$REMOTE_NAME" main || true

# ==== .env dosyalarını DÜZ yedekle ====
mkdir -p "$ENV_BACKUP_DIR"
ENV_FILES=()
# NUL-terminated güvenli tarama (boş girdileri önler)
while IFS= read -r -d '' f; do
  ENV_FILES+=("$f")
done < <(find "$REPO_DIR" \
  -path "$ENV_BACKUP_DIR" -prune -o \
  -path "$REPO_DIR/.git" -prune -o \
  -name node_modules -prune -o \
  -name venv -prune -o \
  -type f -name ".env" -print0)

for envf in "${ENV_FILES[@]}"; do
  [[ -z "$envf" ]] && continue
  rel="${envf#"$REPO_DIR"/}"                     # örn: backend/.env
  dest_dir="$ENV_BACKUP_DIR/$(dirname "$rel")"   # örn: infra/secrets/env-backups/backend
  mkdir -p "$dest_dir"
  out="$dest_dir/.env.${TIMESTAMP}"
  install -m 600 -- "$envf" "$out"
  echo "ENV yedek: $out"
done

# ==== Commit & Push ====
git add -A
git add -f "$ENV_BACKUP_DIR" || true
if ! git diff --cached --quiet; then
  git commit -m "chore(backup): ${TIMESTAMP} (plain .env backups)"
fi
git push -u "$REMOTE_NAME" main
git push "$REMOTE_NAME" --tags

echo "OK: GitHub yedek tamam (plain .env)."

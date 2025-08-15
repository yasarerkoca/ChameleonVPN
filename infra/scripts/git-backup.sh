#cd ~/ChameleonVPN/infra/scripts
#chmod +x git-backup.sh
#./git-backup.sh

#!/usr/bin/env bash
set -euo pipefail

# === Ayarlar ===
REPO_DIR="${REPO_DIR:-$HOME/ChameleonVPN}"
REMOTE_NAME="${REMOTE_NAME:-github}"
REMOTE_URL="${REMOTE_URL:-git@github.com:yasarerkoca/ChameleonVPN.git}"
FPR_EXPECTED="SHA256:wcRqXvyr5V6LP7P6i/LQKWaSgUghpuk7xFwgR+KEOtk"

# === SSH key’i fingerprint’e göre bul ===
ID_FILE="${ID_FILE:-}"
if [[ -z "${ID_FILE}" ]]; then
  for pub in "$HOME"/.ssh/*.pub; do
    [[ -e "$pub" ]] || continue
    fpr="$(ssh-keygen -lf "$pub" -E sha256 | awk '{print $2}')"
    if [[ "$fpr" == "$FPR_EXPECTED" ]]; then
      ID_FILE="${pub%.pub}"
      break
    fi
  done
fi
if [[ -z "${ID_FILE:-}" ]]; then
  echo "HATA: Fingerprint eşleşen SSH key bulunamadı. ID_FILE ile özel anahtar yolunu verin." >&2
  exit 1
fi
chmod 600 "$ID_FILE" || true
export GIT_SSH_COMMAND="ssh -i $ID_FILE -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"

# === Repo yedekle ===
cd "$REPO_DIR"
git rev-parse --git-dir >/dev/null 2>&1 || git init -b main
git show-ref --verify --quiet refs/heads/main || git branch -M main

if ! git remote get-url "$REMOTE_NAME" >/dev/null 2>&1; then
  git remote add "$REMOTE_NAME" "$REMOTE_URL"
fi

git add -A
if ! git diff --cached --quiet; then
  git commit -m "Auto backup: $(date -Iseconds)"
fi

git push -u "$REMOTE_NAME" main
git push "$REMOTE_NAME" --tags
echo "OK: GitHub yedek tamam."

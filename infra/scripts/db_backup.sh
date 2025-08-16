#chmod +x ~/ChameleonVPN/infra/scripts/db_backup.sh

#!/usr/bin/env bash
set -euo pipefail
DATE="$(date +%Y%m%d_%H%M%S)"
OUT="db_backup_${DATE}.sql"
PGUSER="${PGUSER:-vpnadmin}"
PGPASSWORD="${PGPASSWORD:-iryna}"
PGDATABASE="${PGDATABASE:-chameleonvpn}"
PGHOST="${PGHOST:-localhost}"
EXPORT_DIR="${EXPORT_DIR:-$HOME/db_backups}"
mkdir -p "$EXPORT_DIR"
PGPASSWORD="$PGPASSWORD" pg_dump -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" > "$EXPORT_DIR/$OUT"
echo "OK: $EXPORT_DIR/$OUT"

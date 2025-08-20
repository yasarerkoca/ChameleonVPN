#!/usr/bin/env bash
set -euo pipefail

BACKUP_ROOT="${BACKUP_ROOT:-$HOME/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"

PGUSER="${PGUSER:-vpnadmin}"
PGPASSWORD="${PGPASSWORD:?Environment variable PGPASSWORD must be set}"
PGDATABASE="${PGDATABASE:-chameleonvpn}"
PGHOST="${PGHOST:-localhost}"

REDIS_HOST="${REDIS_HOST:-localhost}"
REDIS_PORT="${REDIS_PORT:-6379}"

DATE="$(date +%Y%m%d_%H%M%S)"
TARGET_DIR="$BACKUP_ROOT/$DATE"

mkdir -p "$TARGET_DIR"

# Dump Postgres
PGPASSWORD="$PGPASSWORD" pg_dump -h "$PGHOST" -U "$PGUSER" "$PGDATABASE" | gzip > "$TARGET_DIR/postgres.sql.gz"

# Dump Redis
redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" --rdb "$TARGET_DIR/redis.rdb"

# Prune old backups
find "$BACKUP_ROOT" -mindepth 1 -maxdepth 1 -type d -mtime +"$RETENTION_DAYS" -exec rm -rf {} +

echo "Backup completed: $TARGET_DIR"

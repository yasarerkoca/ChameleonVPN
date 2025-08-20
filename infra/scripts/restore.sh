#!/usr/bin/env bash
set -euo pipefail

BACKUP_ROOT="${BACKUP_ROOT:-$HOME/backups}"
TARGET="${1:-latest}"

PGUSER="${PGUSER:-vpnadmin}"
PGPASSWORD="${PGPASSWORD:?Environment variable PGPASSWORD must be set}"
PGDATABASE="${PGDATABASE:-chameleonvpn}"
PGHOST="${PGHOST:-localhost}"

REDIS_HOST="${REDIS_HOST:-localhost}"
REDIS_PORT="${REDIS_PORT:-6379}"

if [ "$TARGET" = "latest" ]; then
  TARGET_DIR=$(ls -1d "$BACKUP_ROOT"/* 2>/dev/null | sort | tail -n 1)
else
  TARGET_DIR="$BACKUP_ROOT/$TARGET"
fi

if [ -z "${TARGET_DIR:-}" ] || [ ! -d "$TARGET_DIR" ]; then
  echo "Backup '$TARGET' not found" >&2
  exit 1
fi

POSTGRES_FILE="$TARGET_DIR/postgres.sql.gz"
REDIS_FILE="$TARGET_DIR/redis.rdb"

if [ ! -f "$POSTGRES_FILE" ] || [ ! -f "$REDIS_FILE" ]; then
  echo "Backup files missing in $TARGET_DIR" >&2
  exit 1
fi

echo "Restoring Postgres from $POSTGRES_FILE"
PGPASSWORD="$PGPASSWORD" gunzip -c "$POSTGRES_FILE" | psql -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE"

echo "Restoring Redis from $REDIS_FILE"
redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" FLUSHALL
redis-check-rdb "$REDIS_FILE" --convert | redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" --pipe

echo "Restore completed from $TARGET_DIR"

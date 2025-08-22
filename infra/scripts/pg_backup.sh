#!/bin/bash
# Environment variables:
#   BACKUP_DIR: Directory for backup files (defaults to $HOME/pg_backups)
#   GPG_PASSPHRASE: Passphrase used to encrypt the backup (required)
#   LOG_DIR: Directory for log files (defaults to $HOME)

DATE=$(date +%Y-%m-%d-%H%M)
BACKUP_DIR="${BACKUP_DIR:-$HOME/pg_backups}"
DB_NAME="chameleonvpn"
DB_USER="vpnadmin"
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_$DATE.sql.gz"
GPG_PASSPHRASE="${GPG_PASSPHRASE:?Environment variable GPG_PASSPHRASE must be set}"
LOG_DIR="${LOG_DIR:-$HOME}"

mkdir -p "$BACKUP_DIR" "$LOG_DIR"

# Gzip ile yedekle
pg_dump -U $DB_USER $DB_NAME | gzip > "$BACKUP_FILE"

# GPG ile şifrele
gpg --batch --yes --passphrase "$GPG_PASSPHRASE" -c "$BACKUP_FILE"

# Şifreli dosyayı Google Drive’a gönder
rclone copy "$BACKUP_FILE.gpg" gdrive:ChameleonVPN-Backups/ >> "$LOG_DIR/rclone-backup.log" 2>&1

# Eski .gpg dosyalarını sil (14 günden eski)
find "$BACKUP_DIR" -type f -mtime +14 -name '*.gpg' -delete

# Backup durumu logla
if [ -f "$BACKUP_FILE.gpg" ]; then
    echo "$(date): Backup başarılı: $BACKUP_FILE.gpg" >> "$LOG_DIR/backup_status.log"
else
    echo "$(date): Backup BAŞARISIZ!" >> "$LOG_DIR/backup_status.log"
fi

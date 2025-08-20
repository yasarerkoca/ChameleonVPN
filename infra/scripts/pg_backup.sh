#!/bin/bash

DATE=$(date +%Y-%m-%d-%H%M)
BACKUP_DIR="/var/backups/chameleonvpn"
DB_NAME="chameleonvpn"
DB_USER="vpnadmin"
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_$DATE.sql.gz"
GPG_PASSPHRASE="SeninParolan"  # PAROLANI BURAYA YAZ

mkdir -p "$BACKUP_DIR"

# Gzip ile yedekle
pg_dump -U $DB_USER $DB_NAME | gzip > "$BACKUP_FILE"

# GPG ile şifrele
gpg --batch --yes --passphrase "$GPG_PASSPHRASE" -c "$BACKUP_FILE"

# Şifreli dosyayı Google Drive’a gönder
rclone copy "$BACKUP_FILE.gpg" gdrive:ChameleonVPN-Backups/ >> /home/yasarerkoca/rclone-backup.log 2>&1

# Eski .gpg dosyalarını sil (14 günden eski)
find "$BACKUP_DIR" -type f -mtime +14 -name '*.gpg' -delete

# Backup durumu logla
if [ -f "$BACKUP_FILE.gpg" ]; then
    echo "$(date): Backup başarılı: $BACKUP_FILE.gpg" >> /home/yasarerkoca/backup_status.log
else
    echo "$(date): Backup BAŞARISIZ!" >> /home/yasarerkoca/backup_status.log
fi

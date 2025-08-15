#!/bin/bash
BACKUP_DIR="/var/backups/chameleonvpn"
REMOTE=gdrive:chameleonvpn_backups

rclone copy $BACKUP_DIR $REMOTE --update

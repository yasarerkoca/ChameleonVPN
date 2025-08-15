#!/bin/bash
BACKUP_DIR=~/db_backups
REMOTE=gdrive:chameleonvpn_backups

rclone copy $BACKUP_DIR $REMOTE --update

#!/bin/bash

# LOG_DIR: Directory where log files will be written. Defaults to $HOME.
LOG_DIR="${LOG_DIR:-$HOME}"
# Sistem paket listelerini güncelle ve tüm paketleri yükselt
sudo apt update && sudo apt upgrade -y

# (Opsiyonel) Otomatik eski paket/çekirdek temizliği:
sudo apt autoremove -y
sudo apt autoclean

# Güncelleme tarihi ve sonucu log dosyasına yazılsın
echo "$(date): Sistem güncellendi." >> "$LOG_DIR/sys_update.log"

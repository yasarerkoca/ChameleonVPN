#!/bin/bash

# Sistem paket listelerini güncelle ve tüm paketleri yükselt
sudo apt update && sudo apt upgrade -y

# (Opsiyonel) Otomatik eski paket/çekirdek temizliği:
sudo apt autoremove -y
sudo apt autoclean

# Güncelleme tarihi ve sonucu log dosyasına yazılsın
echo "$(date): Sistem güncellendi." >> /home/yasarerkoca/sys_update.log

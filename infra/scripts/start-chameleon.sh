#!/bin/bash

echo "[CHAMELEON] PostgreSQL başlatılıyor..."
sudo systemctl start postgresql

echo "[CHAMELEON] WireGuard başlatılıyor..."
sudo systemctl start wg-quick@wg0

echo "[CHAMELEON] FastAPI backend başlatılıyor..."
sudo systemctl start chameleon-backend

echo "[CHAMELEON] Tüm servisler başarıyla başlatıldı."

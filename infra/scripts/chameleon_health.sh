#!/bin/bash
# LOG_DIR: Directory where log files will be written. Defaults to $HOME.
LOG_DIR="${LOG_DIR:-$HOME}"

if ! curl -sf http://localhost:8000/ > /dev/null; then
    systemctl restart chameleonvpn-backend
    echo "$(date): API restart edildi." >> "$LOG_DIR/chameleon_health.log"
fi

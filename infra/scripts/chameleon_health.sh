#!/bin/bash
if ! curl -sf http://localhost:8000/ > /dev/null; then
    systemctl restart chameleonvpn-backend
    echo "$(date): API restart edildi." >> /home/yasarerkoca/chameleon_health.log
fi

# ~/ChameleonVPN/backend/app/services/proxy_config_service.py

from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def generate_proxy_config(
    ip: str,
    port: int,
    protocol: str = "socks5",
    timeout: int = 30,
    dns: str = "10.8.0.1"
) -> str:
    """
    Proxy/VPN yapılandırma metni üretir.
    DNS leak koruması için internal DNS zorunlu eklenir.

    Args:
        ip (str): Proxy IP adresi
        port (int): Proxy portu
        protocol (str): Bağlantı protokolü (varsayılan: socks5)
        timeout (int): Zaman aşımı süresi (saniye)
        dns (str): DNS sunucusu (varsayılan: 10.8.0.1)

    Returns:
        str: Yapılandırma metni
    """
    template = f"""
proxy_ip = {ip}
proxy_port = {port}
dns = {dns}

[connection]
type = {protocol}
timeout = {timeout}
"""
    return template.strip()

def save_config_to_file(config_str: str, filename: Path) -> None:
    """
    Üretilen config dosyasını belirtilen yola kaydeder.

    Args:
        config_str (str): Config içeriği
        filename (Path): Kaydedilecek dosya yolu
    """
    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
        filename.write_text(config_str)
        logger.info(f"Proxy yapılandırma dosyası oluşturuldu: {filename}")
    except Exception as e:
        logger.error(f"Config dosyası kaydedilemedi: {filename} - {str(e)}")
        raise

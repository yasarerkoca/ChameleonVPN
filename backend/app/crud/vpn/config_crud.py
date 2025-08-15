# ~/ChameleonVPN/backend/app/crud/vpn/config.py

from sqlalchemy.orm import Session
from app.models.vpn.vpn_config import VPNConfig  # modelin adını senin dosyana göre güncelle
from app.models.user.user import User
from typing import List


def get_vpn_config_for_user(db: Session, user: User) -> VPNConfig:
    """
    Belirli bir kullanıcı için VPN yapılandırma dosyasını getir.
    """
    return db.query(VPNConfig).filter(VPNConfig.user_id == user.id).first()


def get_all_vpn_configs(db: Session) -> List[VPNConfig]:
    """
    Tüm kullanıcıların aktif VPN yapılandırmalarını getirir.
    """
    return db.query(VPNConfig).filter(VPNConfig.config.isnot(None)).all()

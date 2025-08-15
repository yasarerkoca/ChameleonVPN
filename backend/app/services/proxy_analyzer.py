# app.services.proxy_analyzer - Proxy kullanım loglarında anomali tespiti

from typing import List, Dict
from app.models.proxy.proxy_usage_log import ProxyUsageLog
import logging

logger = logging.getLogger(__name__)


def detect_anomalies(logs: List[ProxyUsageLog], threshold_mb: int = 1000) -> List[Dict]:
    """
    Kullanıcıların kısa sürede fazla proxy verisi kullanıp kullanmadığını analiz eder.

    Args:
        logs (List[ProxyUsageLog]): Kullanıcı proxy kullanım logları
        threshold_mb (int): Aşım eşiği (MB)

    Returns:
        List[Dict]: Anomali tespit edilen kullanıcılar
    """
    anomalies = {}
    user_logs = {}

    # Logları kullanıcıya göre gruplandır
    for log in logs:
        user_logs.setdefault(log.user_id, []).append(log)

    for user_id, user_log_list in user_logs.items():
        total_used = sum(log.used_mb for log in user_log_list)

        if total_used > threshold_mb:
            anomalies[user_id] = {
                "user_id": user_id,
                "total_used_mb": total_used,
                "message": "Kota aşımı"
            }

            logger.warning(f"Kota aşımı: user_id={user_id}, used={total_used} MB")

    return list(anomalies.values())

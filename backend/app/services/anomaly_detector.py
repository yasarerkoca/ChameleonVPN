# app.services.anomaly_detector - AI tabanlı anomali tespiti

from typing import List, Dict


def detect_anomalies(
    logs: List[Dict],
    traffic_threshold: int = 5000,
    connect_threshold: int = 50
) -> List[Dict]:
    """
    Kullanıcı logları üzerinden AI tabanlı basit anomali analizi yapar.
    """
    anomalies = []

    for log in logs:
        user_id = log.get("user_id")
        traffic = log.get("traffic_mb", 0)
        connections = log.get("connect_count", 0)
        reasons = []

        if traffic > traffic_threshold:
            reasons.append("Yüksek trafik kullanımı")
        if connections > connect_threshold:
            reasons.append("Çok fazla bağlantı denemesi")

        if reasons:
            anomalies.append({
                "user_id": user_id,
                "problems": reasons,
                "traffic_mb": traffic,
                "connect_count": connections
            })

    return anomalies


def run_deep_anomaly_analysis(logs: List[Dict]) -> Dict:
    """
    Gelişmiş AI log analizi. Anomali oranı ve örnek problemler döner.
    """
    anomalies = detect_anomalies(logs)
    total_logs = len(logs)
    anomaly_count = len(anomalies)

    return {
        "total_logs": total_logs,
        "anomalies_detected": anomaly_count,
        "anomaly_ratio": round(anomaly_count / total_logs, 3) if total_logs > 0 else 0,
        "examples": anomalies[:5]
    }

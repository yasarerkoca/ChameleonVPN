# ~/ChameleonVPN/backend/app/models/__init__.py
"""
Modelleri tek noktadan içe aktarma.

Yükleme sırası notu:
1) User
2) Security
3) Corporate
4) Proxy
5) VPN
6) Billing
7) Logs (en sonda)
"""

from app.config.database import Base

# 1) USER
from .user import (
    User, UserSession, UserSupportTicket, UserActivityLog, UserNotification,
    UserReferralReward, UserExternalAuth, DeletedUser, UserServerActivity,
    UserSecurity, UserFlagsSettings, UserProfile, UserRelationship,
)

# RBAC
from .role import Role
from .permission import Permission

# 2) SECURITY
from .security import (
    APIKey, APIKeyAccessLog, BlockedIP, BlockedIPRange,
    TwoFactorToken, UserBlocklist, UserLimit,
)

# 3) CORPORATE
from .corporate import CorporateUserGroup, CorporateUserRightsHistory

# 4) PROXY
from .proxy import ProxyIP, ProxyUsageLog, UserProxyAssignment

# 5) VPN
from .vpn import VPNConfig, VPNServer, VPNLog, ConnectionAttempt

# 6) BILLING
from .billing import (
    Plan, Payment, Membership, UserBillingHistory, UserSubscriptionHistory,
)

# 7) LOGS (ORM MODELLER EN SONA)
# DİKKAT: ORM modelleri logs paketinden alınır.
from app.logs.ai_server_selection_log import AIServerSelectionLog
from app.logs.anomaly_fraud_record import AnomalyFraudRecord

__all__ = [
    "Base",
    # User
    "User", "UserSession", "UserSupportTicket", "UserActivityLog", "UserNotification",
    "UserReferralReward", "UserExternalAuth", "DeletedUser", "UserServerActivity",
    "UserSecurity", "UserFlagsSettings", "UserProfile", "UserRelationship",
    # RBAC
    "Role", "Permission",
    # Security
    "APIKey", "APIKeyAccessLog", "BlockedIP", "BlockedIPRange",
    "TwoFactorToken", "UserBlocklist", "UserLimit",
    # Corporate
    "CorporateUserGroup", "CorporateUserRightsHistory",
    # Proxy
    "ProxyIP", "ProxyUsageLog", "UserProxyAssignment",
    # VPN
    "VPNConfig", "VPNServer", "VPNLog", "ConnectionAttempt",
    # Billing
    "Plan", "Payment", "Membership", "UserBillingHistory", "UserSubscriptionHistory",
    # Logs
    "AIServerSelectionLog", "AnomalyFraudRecord",
]

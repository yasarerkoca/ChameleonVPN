# ~/ChameleonVPN/backend/app/models/__init__.py

from app.config.database import Base

# ======================
# USER MODELLERİ
# ======================
from .user import (
    User,
    UserSession,
    UserSupportTicket,
    UserActivityLog,
    UserNotification,
    UserReferralReward,
    UserExternalAuth,
    DeletedUser,
    UserServerActivity,
    UserSecurity,
    UserFlagsSettings,
    UserProfile,
    UserRelationship
)

# ======================
# PROXY MODELLERİ
# ======================
from .proxy import (
    ProxyIP,
    ProxyUsageLog,
    UserProxyAssignment
)

# ======================
# VPN MODELLERİ
# ======================
from .vpn import (
    VPNServer,
    VPNLog,
    ConnectionAttempt
)

# ======================
# BILLING MODELLERİ
# ======================
from .billing import (
    Plan,
    Payment,
    Membership,
    UserBillingHistory,
    UserSubscriptionHistory
)

# ======================
# CORPORATE MODELLERİ
# ======================
from .corporate import (
    CorporateUserGroup,
    CorporateUserRightsHistory
)

# ======================
# SECURITY MODELLERİ
# ======================
from .security import (
    APIKey,
    APIKeyAccessLog,
    BlockedIP,
    RefreshTokenBlacklist,
    TwoFactorToken,
    UserBlocklist,
    UserLimit
)

# ======================
# LOG MODELLERİ
# ======================
from .logs import (
    SystemAlert,
    ConsentLog,
    EmailSmsLog,
    AdminActivityLog,
    AnomalyFraudRecord,
    UserManualAudit
)

__all__ = [
    # User
    "User",
    "UserSession",
    "UserSupportTicket",
    "UserActivityLog",
    "UserNotification",
    "UserReferralReward",
    "UserExternalAuth",
    "DeletedUser",
    "UserServerActivity",
    "UserSecurity",
    "UserFlagsSettings",
    "UserProfile",
    "UserRelationship",

    # Proxy
    "ProxyIP",
    "ProxyUsageLog",
    "UserProxyAssignment",

    # VPN
    "VPNServer",
    "VPNLog",
    "ConnectionAttempt",

    # Billing
    "Plan",
    "Payment",
    "Membership",
    "UserBillingHistory",
    "UserSubscriptionHistory",

    # Corporate
    "CorporateUserGroup",
    "CorporateUserRightsHistory",

    # Security
    "APIKey",
    "APIKeyAccessLog",
    "BlockedIP",
    "RefreshTokenBlacklist",
    "TwoFactorToken",
    "UserBlocklist",
    "UserLimit",

    # Logs
    "SystemAlert",
    "ConsentLog",
    "EmailSmsLog",
    "AdminActivityLog",
    "AnomalyFraudRecord",
    "UserManualAudit"
]

# ~/ChameleonVPN/backend/app/models/__init__.py

"""
Modelleri tek noktadan içe aktarma.
Not: İlişki hatalarını önlemek için yükleme sırası önemli:
1) User
2) Security (User’a back_populates edenler)
3) Corporate (User’a back_populates edenler)
4) Diğer domain’ler (proxy, vpn, billing, logs)
"""

from app.config.database import Base

# 1) USER
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
    UserRelationship,
)

# RBAC
from .role import Role
from .permission import Permission

# 2) SECURITY (User.back_populates: api_keys, two_factor_tokens, limits, vb.)
from .security import (
    APIKey,
    APIKeyAccessLog,
    BlockedIP,
    BlockedIPRange,
    TwoFactorToken,
    UserBlocklist,
    UserLimit,
)

# 3) CORPORATE
from .corporate import (
    CorporateUserGroup,
    CorporateUserRightsHistory,
)

# 4) PROXY
from .proxy import (
    ProxyIP,
    ProxyUsageLog,
    UserProxyAssignment,
)

# 5) VPN
from .vpn import (
    VPNServer,
    VPNLog,
    ConnectionAttempt,
)

# 6) BILLING
from .billing import (
    Plan,
    Payment,
    Membership,
    UserBillingHistory,
    UserSubscriptionHistory,
)

__all__ = [
    # Base
    "Base",

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
    "Role",
    "Permission",

    # Security
    "APIKey",
    "APIKeyAccessLog",
    "BlockedIP",
    "BlockedIPRange",
    "TwoFactorToken",
    "UserBlocklist",
    "UserLimit",

    # Corporate
    "CorporateUserGroup",
    "CorporateUserRightsHistory",

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

]

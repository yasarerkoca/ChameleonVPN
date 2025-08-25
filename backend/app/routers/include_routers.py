from fastapi import FastAPI

# --- Auth ---
from .auth import (
    auth_account_actions,
    auth_profile_routes,
    oauth,
    password,
    auth_login,
)
from .auth.auth_2fa import router as auth_2fa_router
# --- Admin ---
from .admin import (
    account_unlock,
    ip_range,
    ai_logs,
    anomaly_analysis,
    api_key_routes,
    ban_manage,
    groups,
    ip_block,
    manual_audit,
    proxy_limit,
    proxy_routes,
    quota_routes,
    security_controls,
    session_routes,
    status_management,
    user_audit_summary,
    user_csv,
    user_routes,
    ai_server_log_routes,
)

# --- Payment ---
from .payment import (
    payment_routes,
    billing_routes,
    provider_routes,
    webhook_routes,
)

# --- Membership ---
from .membership import membership_routes

# --- VPN ---
from .vpn import (
    server_routes,
    activity_routes,
    quota_routes as vpn_quota_routes,
    config_routes,
    status_routes,
    traffic_routes,
    ai_selector_routes,
    connection_routes,
    vpn_peers,
)

# --- Corporate ---
from .corporate import corporate_routes

# --- Monitor ---
from .monitor import monitor_routes
from .monitor import dnsleak

# --- Proxy (User) ---
from .proxy import user_routes as proxy_user_routes


def include_routers(app: FastAPI):
    # AUTH
    app.include_router(auth_account_actions.router)
    app.include_router(auth_login.router)
    app.include_router(auth_profile_routes.router)
    app.include_router(oauth.router)
    app.include_router(password.router)
    app.include_router(auth_2fa_router)

    # ADMIN
    admin_routers = [
        account_unlock.router,
        ip_range.router,
        ai_logs.router,
        ai_server_log_routes.router,
        anomaly_analysis.router,
        api_key_routes.router,
        ban_manage.router,
        groups.router,
        ip_block.router,
        manual_audit.router,
        proxy_limit.router,
        proxy_routes.router,
        quota_routes.router,
        security_controls.router,
        session_routes.router,
        status_management.router,
        user_audit_summary.router,
        user_csv.router,
        user_routes.router,
    ]
    for r in admin_routers:
        app.include_router(r)

    # PAYMENT
    app.include_router(payment_routes.router)
    app.include_router(billing_routes.router)
    app.include_router(provider_routes.router)
    app.include_router(webhook_routes.router)

    # MEMBERSHIP
    app.include_router(membership_routes.router)

    # VPN
    app.include_router(server_routes.router)
    app.include_router(activity_routes.router)
    app.include_router(vpn_quota_routes.router)
    app.include_router(config_routes.router)
    app.include_router(status_routes.router)
    app.include_router(traffic_routes.router)
    app.include_router(ai_selector_routes.router)
    app.include_router(connection_routes.router)
    app.include_router(vpn_peers.router)
    # CORPORATE
    app.include_router(corporate_routes.router)

    # MONITOR
    app.include_router(monitor_routes.router)
    app.include_router(dnsleak.router)
    # PROXY (USER)
    app.include_router(proxy_user_routes.router)

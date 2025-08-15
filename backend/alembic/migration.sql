---- Alembic başlıyor ----
Alembic gördüğü tablolar: dict_keys([])
BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> dd3b40c3aef0

CREATE TABLE corporate_user_groups (
    id SERIAL NOT NULL, 
    name VARCHAR NOT NULL, 
    max_proxies INTEGER, 
    is_active BOOLEAN, 
    PRIMARY KEY (id), 
    UNIQUE (name)
);

CREATE INDEX ix_corporate_user_groups_id ON corporate_user_groups (id);

CREATE TABLE deleted_users (
    id SERIAL NOT NULL, 
    original_user_id INTEGER, 
    email VARCHAR(128), 
    deletion_reason VARCHAR(64), 
    deleted_at TIMESTAMP WITHOUT TIME ZONE, 
    last_ip VARCHAR(64), 
    last_device_id VARCHAR(128), 
    notes TEXT, 
    PRIMARY KEY (id)
);

CREATE TABLE payments (
    id SERIAL NOT NULL, 
    user_id INTEGER NOT NULL, 
    amount NUMERIC(10, 2) NOT NULL, 
    type VARCHAR NOT NULL, 
    description VARCHAR, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id)
);

CREATE INDEX ix_payments_id ON payments (id);

CREATE TABLE plans (
    id SERIAL NOT NULL, 
    name VARCHAR NOT NULL, 
    quota_mb BIGINT NOT NULL, 
    price NUMERIC(10, 2) NOT NULL, 
    duration_days INTEGER NOT NULL, 
    is_active BOOLEAN, 
    PRIMARY KEY (id), 
    UNIQUE (name)
);

CREATE INDEX ix_plans_id ON plans (id);

CREATE TABLE proxy_ips (
    id SERIAL NOT NULL, 
    ip_address VARCHAR NOT NULL, 
    port INTEGER NOT NULL, 
    country VARCHAR, 
    total_quota_mb BIGINT, 
    is_active BOOLEAN, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id), 
    UNIQUE (ip_address)
);

CREATE INDEX ix_proxy_ips_id ON proxy_ips (id);

CREATE TABLE user_blocklist (
    id SERIAL NOT NULL, 
    email VARCHAR(128), 
    ip_address VARCHAR(64), 
    device_id VARCHAR(128), 
    reason VARCHAR(64), 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    block_until TIMESTAMP WITHOUT TIME ZONE, 
    notes TEXT, 
    PRIMARY KEY (id)
);

CREATE TABLE users (
    id SERIAL NOT NULL, 
    email VARCHAR(128) NOT NULL, 
    password_hash VARCHAR(256), 
    full_name VARCHAR(128), 
    is_active BOOLEAN, 
    is_email_verified BOOLEAN, 
    is_admin BOOLEAN, 
    role VARCHAR(16), 
    status VARCHAR(16), 
    corporate_account_id INTEGER, 
    is_corporate_admin BOOLEAN, 
    mfa_enabled BOOLEAN, 
    last_login TIMESTAMP WITHOUT TIME ZONE, 
    last_ip VARCHAR(64), 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    phone_number VARCHAR(32), 
    preferred_language VARCHAR(8), 
    failed_login_attempts INTEGER, 
    locked_until TIMESTAMP WITHOUT TIME ZONE, 
    referral_code VARCHAR(16), 
    referred_by VARCHAR(16), 
    notification_settings JSONB, 
    is_terms_accepted BOOLEAN, 
    reset_token VARCHAR(256), 
    reset_token_expire TIMESTAMP WITHOUT TIME ZONE, 
    is_deleted BOOLEAN, 
    anonymized_at TIMESTAMP WITHOUT TIME ZONE, 
    flags JSONB, 
    preferences JSONB, 
    country_code VARCHAR(8), 
    city VARCHAR(64), 
    region VARCHAR(64), 
    PRIMARY KEY (id), 
    UNIQUE (email), 
    UNIQUE (referral_code)
);

CREATE INDEX ix_users_id ON users (id);

CREATE TABLE vpn_servers (
    id SERIAL NOT NULL, 
    name VARCHAR(128), 
    ip_address VARCHAR(64), 
    country_code VARCHAR(8), 
    city VARCHAR(64), 
    type VARCHAR(32), 
    status VARCHAR(16), 
    capacity INTEGER, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id)
);

CREATE TABLE admin_activity_logs (
    id SERIAL NOT NULL, 
    admin_user_id INTEGER, 
    action VARCHAR(128), 
    target_table VARCHAR(64), 
    target_id INTEGER, 
    details TEXT, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    ip_address VARCHAR(64), 
    PRIMARY KEY (id), 
    FOREIGN KEY(admin_user_id) REFERENCES users (id)
);

CREATE TABLE anomaly_fraud_records (
    id SERIAL NOT NULL, 
    user_id INTEGER, 
    detected_at TIMESTAMP WITHOUT TIME ZONE, 
    type VARCHAR(64), 
    details TEXT, 
    status VARCHAR(16), 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE connection_attempts (
    id SERIAL NOT NULL, 
    user_id INTEGER, 
    server_id INTEGER, 
    attempt_time TIMESTAMP WITHOUT TIME ZONE, 
    status VARCHAR(16), 
    reason TEXT, 
    PRIMARY KEY (id), 
    FOREIGN KEY(server_id) REFERENCES vpn_servers (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE consent_logs (
    id SERIAL NOT NULL, 
    user_id INTEGER, 
    consent_type VARCHAR(32), 
    consent_version VARCHAR(16), 
    consented_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE corporate_user_rights_history (
    id SERIAL NOT NULL, 
    corporate_account_id INTEGER, 
    user_id INTEGER, 
    action VARCHAR(64), 
    old_rights JSONB, 
    new_rights JSONB, 
    updated_by INTEGER, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    FOREIGN KEY(updated_by) REFERENCES users (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE email_sms_logs (
    id SERIAL NOT NULL, 
    user_id INTEGER, 
    type VARCHAR(16), 
    recipient VARCHAR(128), 
    subject VARCHAR(128), 
    message TEXT, 
    sent_at TIMESTAMP WITHOUT TIME ZONE, 
    delivery_status VARCHAR(16), 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE promo_codes (
    id SERIAL NOT NULL, 
    code VARCHAR(32), 
    user_id INTEGER, 
    discount_percent INTEGER, 
    valid_from TIMESTAMP WITHOUT TIME ZONE, 
    valid_until TIMESTAMP WITHOUT TIME ZONE, 
    usage_limit INTEGER, 
    description VARCHAR(128), 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id), 
    UNIQUE (code)
);

CREATE TABLE proxy_usage_logs (
    id SERIAL NOT NULL, 
    user_id INTEGER NOT NULL, 
    proxy_id INTEGER NOT NULL, 
    used_mb BIGINT, 
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT now(), 
    note VARCHAR, 
    PRIMARY KEY (id), 
    FOREIGN KEY(proxy_id) REFERENCES proxy_ips (id)
);

CREATE INDEX ix_proxy_usage_logs_id ON proxy_usage_logs (id);

CREATE TABLE system_alerts (
    id SERIAL NOT NULL, 
    alert_type VARCHAR(64), 
    message TEXT, 
    severity VARCHAR(16), 
    related_user INTEGER, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    FOREIGN KEY(related_user) REFERENCES users (id)
);

CREATE TABLE user_activity_logs (
    id SERIAL NOT NULL, 
    user_id INTEGER, 
    action VARCHAR(64), 
    details TEXT, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    ip_address VARCHAR(64), 
    device_id VARCHAR(128), 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE user_billing_history (
    id SERIAL NOT NULL, 
    user_id INTEGER, 
    invoice_no VARCHAR(32), 
    amount NUMERIC(10, 2), 
    currency VARCHAR(8), 
    paid_at TIMESTAMP WITHOUT TIME ZONE, 
    pdf_url VARCHAR(256), 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE user_external_auth (
    id SERIAL NOT NULL, 
    user_id INTEGER, 
    provider VARCHAR(32), 
    provider_user_id VARCHAR(128), 
    access_token TEXT, 
    refresh_token TEXT, 
    token_expire TIMESTAMP WITHOUT TIME ZONE, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE user_limits (
    id SERIAL NOT NULL, 
    user_id INTEGER, 
    vpn_quota_gb NUMERIC(8, 2), 
    proxy_quota_gb NUMERIC(8, 2), 
    device_limit INTEGER, 
    ip_limit INTEGER, 
    start_date TIMESTAMP WITHOUT TIME ZONE, 
    end_date TIMESTAMP WITHOUT TIME ZONE, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE user_notifications (
    id SERIAL NOT NULL, 
    user_id INTEGER, 
    title VARCHAR(128), 
    message TEXT, 
    type VARCHAR(32), 
    status VARCHAR(16), 
    link VARCHAR(256), 
    sent_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE user_proxy_assignments (
    id SERIAL NOT NULL, 
    user_id INTEGER NOT NULL, 
    proxy_id INTEGER NOT NULL, 
    assigned_quota_mb BIGINT, 
    assigned_until TIMESTAMP WITHOUT TIME ZONE, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(), 
    is_active BOOLEAN, 
    PRIMARY KEY (id), 
    FOREIGN KEY(proxy_id) REFERENCES proxy_ips (id)
);

CREATE INDEX ix_user_proxy_assignments_id ON user_proxy_assignments (id);

CREATE TABLE user_referral_rewards (
    id SERIAL NOT NULL, 
    referrer_user_id INTEGER, 
    referred_user_id INTEGER, 
    reward_plan VARCHAR(32), 
    reward_quota_gb NUMERIC(8, 2), 
    status VARCHAR(16), 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    FOREIGN KEY(referred_user_id) REFERENCES users (id), 
    FOREIGN KEY(referrer_user_id) REFERENCES users (id)
);

CREATE TABLE user_server_activities (
    id SERIAL NOT NULL, 
    user_id INTEGER, 
    server_ip VARCHAR(64) NOT NULL, 
    activity_type VARCHAR(64) NOT NULL, 
    timestamp TIMESTAMP WITHOUT TIME ZONE, 
    details TEXT, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE user_sessions (
    id SERIAL NOT NULL, 
    user_id INTEGER, 
    device_id VARCHAR(128), 
    device_type VARCHAR(32), 
    ip_address VARCHAR(64), 
    status VARCHAR(16), 
    started_at TIMESTAMP WITHOUT TIME ZONE, 
    ended_at TIMESTAMP WITHOUT TIME ZONE, 
    last_activity TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE user_subscription_history (
    id SERIAL NOT NULL, 
    user_id INTEGER, 
    plan_name VARCHAR(64), 
    start_date TIMESTAMP WITHOUT TIME ZONE, 
    end_date TIMESTAMP WITHOUT TIME ZONE, 
    quota_gb NUMERIC(12, 2), 
    payment_id INTEGER, 
    status VARCHAR(16), 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE user_support_tickets (
    id SERIAL NOT NULL, 
    user_id INTEGER, 
    subject VARCHAR(128), 
    status VARCHAR(16), 
    priority VARCHAR(16), 
    assigned_admin INTEGER, 
    last_update TIMESTAMP WITHOUT TIME ZONE, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    FOREIGN KEY(assigned_admin) REFERENCES users (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

INSERT INTO alembic_version (version_num) VALUES ('dd3b40c3aef0') RETURNING alembic_version.version_num;

COMMIT;


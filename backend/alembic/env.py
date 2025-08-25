# ~/ChameleonVPN/backend/alembic/env.py
from __future__ import annotations
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
import os, sys

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# PYTHONPATH ayarı
BACKEND_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# App metadata
from app.config.database import Base
# Modeller autogenerate için import edilmeli:
from app.models import peer  # noqa: F401
# failed login attempts tablosu için model
from app.models.security import failed_login_attempt  # noqa: F401
# (Varsa diğer modelleri de import et: from app.models import user, ...)

target_metadata = Base.metadata

def get_url() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    from app.config.base import settings
    return settings.DATABASE_URL

def run_migrations_offline():
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool, future=True
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

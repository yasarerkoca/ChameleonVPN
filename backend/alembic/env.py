# ~/ChameleonVPN/backend/alembic/env.py
from __future__ import annotations

import os
import sys
from string import Template
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Alembic Config objesi
config = context.config

# /app yolunu import path'e ekle (app.* importları için)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# --- Modelleri import et ---
from app.config.database import Base  # Base metadata

# Modelleri açıkça import ediyoruz ki Alembic tabloları tanısın
from app.models import peer
from app.models import role
from app.models import permission
from app.models.user import user

# ENV'den gelen DATABASE_URL'i .ini'deki sqlalchemy.url üzerine yaz
raw_url = os.getenv("DATABASE_URL")
db_pass = os.getenv("POSTGRES_PASSWORD")
if raw_url and "${POSTGRES_PASSWORD}" in raw_url and db_pass:
    db_url = Template(raw_url).substitute(POSTGRES_PASSWORD=db_pass)
    config.set_main_option("sqlalchemy.url", db_url)
elif raw_url:
    config.set_main_option("sqlalchemy.url", raw_url)

# Alembic metadata hedefi
target_metadata = Base.metadata

# (Opsiyonel) logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Offline mod: yalnızca SQL üretir."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema="public",
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Online mod: DB bağlantısı kurup uygular."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_schemas=False,  # 👈 sadece public şema
            include_object=lambda obj, name, type_, reflected, compare_to: True,
            version_table_schema="public",
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

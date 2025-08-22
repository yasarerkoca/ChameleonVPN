from __future__ import annotations

import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Alembic Config objesi
config = context.config

# /srv yolunu import path'e ekle (app.* içe aktarımı için)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Tüm modelleri yüke: target_metadata dolsun
from app.config.database import Base  # noqa: E402
from app import models  # noqa: F401,E402  (tüm paket yüklenir, tablolara kaydolur)

# .ini'deki url'yi ENV'den override et (Compose'dan gelen DATABASE_URL esas alınır)
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# Alembic metadata hedefi
target_metadata = Base.metadata

# (Opsiyonel) config dosyasında loglama varsa aktif et
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    """Offline mod: sadece SQL üretir."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Online mod: DB'ye bağlanır ve uygular."""
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
            include_schemas=False,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

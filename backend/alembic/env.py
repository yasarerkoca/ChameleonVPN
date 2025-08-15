# ~/ChameleonVPN/backend/alembic/env.py
import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, text
from alembic import context
import dotenv

# .env dosyasını yükle
dotenv.load_dotenv()

# app dizinini sys.path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# SQLAlchemy Base ve modeller
from app.config.database import Base
from app import models  # tüm modeller __init__.py içinde toplanmalı

print("---- Alembic başlıyor ----")
print("Alembic gördüğü tablolar:", list(Base.metadata.tables.keys()))

# Alembic config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# .env'den DATABASE_URL'i ayarla
if not config.get_main_option("sqlalchemy.url"):
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Offline migration."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Online migration."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        # PostgreSQL search_path ayarla (public + diğer şemalar)
        connection.execute(text("SET search_path TO public, pg_catalog"))
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

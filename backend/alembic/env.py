# ~/ChameleonVPN/backend/alembic/env.py
import os, sys
from logging import getLogger
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, text
from alembic import context
import dotenv

logger = getLogger(__name__)

# .env yükle (varsa)
dotenv.load_dotenv()

# app'i path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# SQLAlchemy Base ve modeller
from app.config.database import Base
from app import models  # modeller __init__.py içinde toplanmalı

# ---- Alembic config ----
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# DATABASE_URL'i env'den al ve alembic.ini'ye enjekte et
db_url = os.getenv("DATABASE_URL", "").strip()
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)
else:
    # Daha net hata için
    logger.error("DATABASE_URL env değişkeni tanımsız! Alembic çalışamaz.")
    raise SystemExit(1)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Offline migration."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        include_schemas=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Online migration."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        # PostgreSQL: search_path
        if connection.dialect.name == "postgresql":
            connection.execute(text("SET search_path TO public, pg_catalog"))
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

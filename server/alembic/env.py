import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
import sqlalchemy as sa
from alembic import context

# ---------------------------------------------------------------------
# 1. Fix import path so Alembic can find "app"
# ---------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ---------------------------------------------------------------------
# 2. Import Base + ALL models (via __init__.py autoload)
# ---------------------------------------------------------------------
from app.core.database import Base
import app.models         # <-- This imports all your model modules
from app.core.config import get_settings

# ---------------------------------------------------------------------
# 3. Alembic Config object
# ---------------------------------------------------------------------
# Alembic Config
config = context.config
settings = get_settings()

# Convert async DB URL to sync DB URL for Alembic
ASYNC_URL = settings.DATABASE_URL
SYNC_URL = ASYNC_URL.replace("+asyncpg", "")   # <-- FIX HERE

config.set_main_option("sqlalchemy.url", SYNC_URL)


# ---------------------------------------------------------------------
# 4. Configure logging
# ---------------------------------------------------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------
# 5. Target metadata for autogenerate
# ---------------------------------------------------------------------
target_metadata = Base.metadata


# ---------------------------------------------------------------------
# 6. Offline migration mode
# ---------------------------------------------------------------------
def run_migrations_offline():
    """Run migrations in 'offline' mode'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        include_schemas=True,         # <-- important for schema-based models
        dialect_opts={"paramstyle": "named"},
        version_table_schema="collab",
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------
# 7. Online migration mode
# ---------------------------------------------------------------------
def run_migrations_online():
    """Run migrations in 'online' mode'."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        # -------------------------------
        # CRITICAL FIX FOR YOUR PROJECT:
        # Alembic cannot compare metadata
        # for a schema that doesn't exist.
        # -------------------------------
        connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS collab"))

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            compare_type=True,
            compare_server_default=True,
            version_table_schema="collab",
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------------------
# 8. Entrypoint
# ---------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

import sys
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool, text
import sqlalchemy as sa

# ---------------------------------------------------------------------
# 1. Fix import path so Alembic can find "app"
# ---------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(f"[ENV] BASE_DIR added to path: {BASE_DIR}")

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ---------------------------------------------------------------------
# 2. Import Base + all models
# ---------------------------------------------------------------------
try:
    from app.core.database import Base
    import app.models        # auto-imports via __init__
    from app.core.config import get_settings
except Exception as e:
    print(f"[ENV] ERROR importing app modules: {e}")
    raise

# ---------------------------------------------------------------------
# 3. Alembic configuration
# ---------------------------------------------------------------------
config = context.config
settings = get_settings()

# Convert async URL → sync URL for Alembic
ASYNC_URL = settings.DATABASE_URL
if "+asyncpg" in ASYNC_URL:
    SYNC_URL = ASYNC_URL.replace("postgresql+asyncpg://", "postgresql://")
else:
    SYNC_URL = ASYNC_URL

config.set_main_option("sqlalchemy.url", SYNC_URL)
print(f"[ENV] Using SYNC DB URL for Alembic: {SYNC_URL}")

# Logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------
# 4. Metadata for autogenerate
# ---------------------------------------------------------------------
target_metadata = Base.metadata

print(f"[ENV] Metadata tables detected ({len(target_metadata.tables)}):")
for t in target_metadata.tables:
    print(f"   - {t}")

# ---------------------------------------------------------------------
# 5. Offline migration mode
# ---------------------------------------------------------------------
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        include_schemas=True,
        version_table_schema="collab",
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# ---------------------------------------------------------------------
# 6. Online migration mode
# ---------------------------------------------------------------------
def run_migrations_online():
    print("[ENV] Starting ONLINE migrations...")

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        print("[ENV] Ensuring schema 'collab' exists...")
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS collab"))
        connection.commit()

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
# 7. Entrypoint
# ---------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

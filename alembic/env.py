import asyncio
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.engine import Connection
import os
import sys
import ssl
from urllib.parse import urlparse, parse_qs

# This line ensures the 'app' module is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from alembic import context

# Import Base and import_models function to load all models
from app.db.base import Base, import_models

# Call the function to ensure all models are imported
import_models()

from app.config import settings

# This is the Alembic Config object, which provides access to the values within the .ini file
config = context.config

# Parse the database URL to handle SSL properly
db_url = settings.DATABASE_URL
parsed_url = urlparse(db_url)
query_params = parse_qs(parsed_url.query)

# Convert the PostgreSQL URL to AsyncPG format without any query parameters
base_url = db_url.split('?')[0]
asyncpg_url = base_url.replace("postgresql://", "postgresql+asyncpg://")

# Update sqlalchemy.url with cleaned URL
config.set_main_option("sqlalchemy.url", asyncpg_url)

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Set target metadata - this is used for generating migrations
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = asyncpg_url
    
    connect_args = {}
    if 'sslmode' in query_params and query_params['sslmode'][0] == 'require':
        print("Setting up SSL for database connection with certificate validation disabled")
        
        # Create SSL context that doesn't verify certificates
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        connect_args['ssl'] = ssl_context
    
    connectable = AsyncEngine(
        engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
            connect_args=connect_args
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    try:
        asyncio.run(run_migrations_online())
    except Exception as e:
        print(f"Error during migration: {e}")
        raise 
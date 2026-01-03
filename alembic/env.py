from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.repository.models import RootModel
from app.utils.generators import get_async_database_url

# Alembic config object
config = context.config

# Configure logging from alembic.ini
if config.config_file_name:
    fileConfig(config.config_file_name)

# Metadata for autogenerate support
target_metadata = RootModel.metadata

# Resolve database URL dynamically
db_url = get_async_database_url()


def run_migrations_offline() -> None:
    # Run migrations without a DB connection
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Create DB engine and bind connection
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Choose migration mode based on context
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

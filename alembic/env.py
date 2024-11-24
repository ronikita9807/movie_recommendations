from alembic import context
from sqlalchemy import engine_from_config, pool, MetaData
from logging.config import fileConfig

from apps.mappers import init_all_mappers

# Импорт моделей из вашего приложения
from apps.shared.infra.persistence.database.base import (
    Base,
)  # Импортируйте Base из вашего модуля с моделями

# Настройки для Alembic
config = context.config
fileConfig(config.config_file_name)


def get_decl_meta() -> MetaData:
    init_all_mappers()
    return Base.metadata


# Убедитесь, что target_metadata определено правильно
target_metadata = get_decl_meta()


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

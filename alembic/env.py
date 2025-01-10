"""Alembic env migration."""

import asyncio
from logging.config import fileConfig
from typing import Literal, Optional

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.sql.schema import SchemaItem

from alembic import context
from src.core.configs.env import settings
from src.core.infrastructure.database.schemas.activity import (
    Activity,
    OrganizationActivity,
)
from src.core.infrastructure.database.schemas.base import BaseModel
from src.core.infrastructure.database.schemas.buildings import Building
from src.core.infrastructure.database.schemas.organizations import Organization
from src.core.infrastructure.database.schemas.phones import PhoneNumber

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseModel.metadata

config.set_main_option("sqlalchemy.url", settings.db.get_url_database)


def include_object(
    object: SchemaItem,  # noqa
    name: Optional[str],
    type_: Literal[
        "schema",
        "table",
        "column",
        "index",
        "unique_constraint",
        "foreign_key_constraint",
    ],
    reflected: bool,
    compare_to: Optional[SchemaItem],
) -> bool:  # noqa : E501
    """Определяет, нужно ли включать объект в миграцию."""
    if type_ == "table" and name not in (
        Organization.__tablename__,
        Building.__tablename__,
        Activity.__tablename__,
        OrganizationActivity.__tablename__,
        PhoneNumber.__tablename__,
    ):
        return False
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        version_table_schema="public",
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migration."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,
        version_table_schema="public",
    )

    with context.begin_transaction():
        """Begin migration."""
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine and associate a connection with the context."""  # noqa : E501
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # do_run_migrations уже содержит include_object в своей конфигурации
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

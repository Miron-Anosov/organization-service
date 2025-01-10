"""Create connect to database session."""

import logging
from logging import Logger
from typing import Any

from src.core.configs.env import settings
from src.core.infrastructure.database.core.engine import (
    ClientDatabase,
    get_engine,
)
from src.core.infrastructure.database.cruds.crud import Crud

LOGGER: Logger = logging.getLogger("utils")


class Connector:
    """Database mq and _session management using context manager."""

    @staticmethod
    async def init_engine(
        url: str = settings.db.get_url_database,
        echo: bool = settings.db.ECHO,
    ) -> ClientDatabase:
        """Initialize the engine and connect to the database.

        :param url: url of the database
        :param echo: whether to echo the database connection
        :return: ClientDatabase: connect to the database.
        """
        return await get_engine(url=url, echo=echo)

    @staticmethod
    async def disconnect_db() -> None:
        """Disconnect crud.

        :return: None
        """
        connect = await get_engine(
            url=settings.db.get_url_database, echo=settings.db.ECHO
        )
        await connect.async_engine.dispose()
        LOGGER.debug("Disconnected database")

    async def __aenter__(self) -> "Connector":
        """Initialize the engine and connect to the database."""
        engine = await get_engine(
            url=settings.db.get_url_database, echo=settings.db.ECHO
        )
        async with engine.get_scoped_session() as __session:
            self.session = __session
            LOGGER.debug("Connected database")
            return self

    async def __aexit__(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Close _session when exiting the context."""
        if hasattr(self, "session") and self.session is not None:
            await self.session.close()
            self.session = None
            LOGGER.debug("Disconnected database")


class ClientDB(Connector):
    """Client database."""

    def __init__(self, crud: Crud) -> None:
        """Initialize the client database."""
        self.crud = crud


def db_client(crud: Crud) -> "Connector":
    """Create a Database worker.

    :return: Connector worker.
    """
    return ClientDB(crud=crud)

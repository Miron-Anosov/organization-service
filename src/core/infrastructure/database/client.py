"""Create connect to database session."""

import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.core.configs.env import settings
from src.core.infrastructure.database.core.engine import (
    ClientDatabase,
    get_engine,
)
from src.core.infrastructure.database.cruds.facade import Crud

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


class Connector(Crud):
    """Database mq and _session management using context manager."""

    @classmethod
    async def init_engine(
        cls,
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

    async def __aenter__(self) -> "AsyncSession":
        """Initialize the engine and connect to the database."""
        engine = await get_engine(
            url=settings.db.get_url_database, echo=settings.db.ECHO
        )
        async with engine.get_scoped_session() as __session:
            self.session = __session
            LOGGER.debug("Connected database")
            return self.session

    async def __aexit__(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Close _session when exiting the context."""
        if hasattr(self, "session") and self.session is not None:
            await self.session.close()
            self.session = None
            LOGGER.debug("Disconnected database")

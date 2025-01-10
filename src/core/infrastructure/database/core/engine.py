"""SQLAlchemy engine."""

from asyncio import current_task
from typing import Any, Dict, Optional, Tuple

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.core.configs.env import settings


class ClientDatabase:
    """Async engine manager."""

    _instance: Optional["ClientDatabase"] = None

    def __new__(
        cls, *args: Tuple[Any], **kwargs: Dict[str, Any]
    ) -> "ClientDatabase":
        """Create singleton API."""
        if cls._instance is None:
            cls._instance = super(ClientDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self, url: str, echo: bool) -> "None":
        """Init SQLAlchemy manager.

        :param url: SQLAlchemy url.
        :param echo: Echo mode.
        :return: None
        """
        self.__url = url
        self.__echo = echo
        self.async_engine = self.create_async_engine()
        self._session = self.create_session(self.async_engine)

    @staticmethod
    def create_session(
        engine: "AsyncEngine",
    ) -> "async_sessionmaker[AsyncSession]":
        """Create crud _session.

        :param engine: SQLAlchemy engine.
        :return: async_sessionmaker[AsyncSession]
        """
        return async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
            class_=AsyncSession,
        )

    @property
    def get_scoped_session(self) -> async_scoped_session[AsyncSession | Any]:
        """Return current scope.

        :return: current scope.
        """
        return async_scoped_session(
            session_factory=self.create_session(self.async_engine),
            scopefunc=current_task,
        )

    def create_async_engine(self) -> "AsyncEngine":
        """Create async engine.

        :return: async engine.
        """
        return create_async_engine(
            url=self.__url,
            echo=self.__echo,
            pool_pre_ping=True,
            pool_size=settings.db.POOL_SIZE_SQL_ALCHEMY_CONF,
            pool_timeout=settings.db.POOL_TIMEOUT,
            max_overflow=settings.db.MAX_OVERFLOW,
        )


async def get_engine(url: str, echo: bool) -> "ClientDatabase":
    """Create ORM _session/engine manager.

    :param url: SQLAlchemy url.
    :param echo: Echo mode.
    :return: async engine.
    """
    return ClientDatabase(url=url, echo=echo)

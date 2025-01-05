"""Configuration .env."""

from pathlib import Path
from typing import Literal

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class RetryDelayMQException(Exception):
    """Exception for tll mq."""

    pass


class CommonConfSettings:
    """Common configurate."""

    ENV_FILE_NAME = ".env"

    ENV = Path(__file__).parent.parent.parent.parent / ENV_FILE_NAME


class EnvironmentFileNotFoundError(ValueError):
    """Custom environment exception."""

    pass


class EnvironmentSetting(BaseSettings):
    """EnvironmentSettingMix uses type mode.

    SettingsConfigDict: dict : TEST, PROD env.
    """

    MODE: Literal["prod", "test", "dev"]

    model_config = SettingsConfigDict(
        env_file=CommonConfSettings.ENV,
        extra="ignore",
        env_file_encoding="utf-8",
    )


class DataBaseClientEnvConf(EnvironmentSetting):
    """Configuration for production environments.

    Attributes:
        POSTGRES_HOST (str): The hostname of the PostgresSQL server.
        POSTGRES_PORT (int): The port number for PostgresSQL.
        POSTGRES_USER (str): The username for connecting to PostgresSQL.
        POSTGRES_DB (str): The name of the PostgresSQL database.
        POSTGRES_PASSWORD (str): The password for the PostgresSQL user.
        ECHO (bool): A flag to enable or disable SQLAlchemy query logging.
    """

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    ECHO: bool
    POOL_TIMEOUT: int
    POOL_SIZE_SQL_ALCHEMY_CONF: int
    MAX_OVERFLOW: int
    MODE: Literal["prod", "test", "dev"]

    @property
    def get_url_database(self) -> str:
        """Return the database URL for SQLAlchemy.

        Constructs and returns a PostgresSQL URL using the asyncpg driver
        to be used by SQLAlchemy for database connections.

        Returns:
            str: The full database mq URL.
        """
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


class WebConfig(EnvironmentSetting):
    """Conf CORS from environment."""

    ALLOWED_ORIGINS: str
    PREFIX_API: str
    LOG_LEVEL: Literal[
        "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"
    ]

    def allowed_origins(self) -> list[str]:
        """Return allowed origins."""
        return self.ALLOWED_ORIGINS.split(",")


class Settings:
    """Common configs for environments."""

    def __init__(self) -> None:
        """Initialize the configs by loading environment variables."""
        try:
            self.db = DataBaseClientEnvConf()
            self.webconf = WebConfig()
        except ValidationError as e:
            raise EnvironmentFileNotFoundError(e)


settings = Settings()

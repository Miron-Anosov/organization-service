"""Trace db metadate."""

import logging
from typing import Optional

from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.trace import TracerProvider
from sqlalchemy.exc import SQLAlchemyError

from src.core.configs.env import settings
from src.core.infrastructure.database import db
from src.core.infrastructure.database.core.engine import ClientDatabase

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


class TraceDbError(SQLAlchemyError):
    """Children Base SQLAlchemy Error."""

    pass


async def setup_jaeger_of_database(
    service_name: str = settings.trace.SERVICE_NAME_DB,
    enable_commenter: bool = settings.trace.ENABLE_COMMENTER,
    tracer_provider: Optional[TracerProvider] = None,
    db_driver: bool = True,
    db_framework: bool = True,
    traceparent: bool = True,
) -> None:
    """Configure Jaeger tracing of database.

    :param service_name: Name of Jaeger tracer.
    :param enable_commenter: Enable Jaeger tracer.
    :param tracer_provider: Jaeger tracer provider.
    :param db_driver: Enable Jaeger tracer driver mode.
    :param db_framework: Enable Jaeger tracer framework mode.
    :param traceparent: Enable Jaeger tracer parent tracer mode.
    :return: None
    :raises: TraceDbError: Raise if any errors occur during tracing.
    """
    try:
        client: ClientDatabase = await db.init_engine()
        engine = client.create_async_engine()
        sync_engine = engine.sync_engine
        LOGGER.info("Engine initialized: %s", engine)
        SQLAlchemyInstrumentor().instrument(
            engine=sync_engine,
            service=service_name,
            tracer_provider=tracer_provider,
            enable_commenter=enable_commenter,
            commenter_options={
                "db_driver": db_driver,
                "db_framework": db_framework,
                "traceparent": traceparent,
            },
        )
        LOGGER.debug("Trace of database setup complete")
    except SQLAlchemyError as e:
        LOGGER.error(f"Error to setup trace for database: {e}")
        raise TraceDbError(f"Error to setup trace for database: {e}")
    except Exception as e:
        LOGGER.error("Unable to setup trace for database: %s", e)
        raise Exception(f"Unable to setup trace for database: {e}")

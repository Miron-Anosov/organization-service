"""Main Rest API module."""

import http
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator, Awaitable, Callable

import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response as StarletteResponse

from src.core.api.v1.routes.middlewars.log import logs_middleware
from src.core.api.v1.routes.organization.route import router as org
from src.core.configs.env import settings
from src.core.infrastructure.database import db
from src.core.infrastructure.tracer.trace_app import setup_jaeger
from src.core.infrastructure.tracer.trace_db import setup_jaeger_of_database

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Connect and close DB."""
    await setup_jaeger_of_database()
    yield
    await db.disconnect_db()
    LOGGER.debug("DB disconnected")


def create_app() -> FastAPI:
    """Maker FastAPI."""
    app_ = FastAPI(
        title="Organization Catalog API",
        lifespan=lifespan,
        root_path=settings.webconf.PREFIX_API,
        description=settings.webconf.DESCRIPTION,
        contact=settings.webconf.contact_swagger(),
    )

    setup_jaeger(app=app_)

    app_.add_middleware(
        middleware_class=CORSMiddleware,  # noqa
        allow_origins=settings.webconf.allowed_origins(),
        allow_credentials=True,
        allow_methods=[http.HTTPMethod.GET],
        allow_headers=["Content-Type", "X-API-Key"],
    )
    app_.include_router(router=org, prefix="/v1")

    @app_.middleware("http")
    async def wrap_api_key_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[StarletteResponse]],
    ) -> StarletteResponse:
        return await logs_middleware(request, call_next)

    return app_


def run_server(
    host: str = "127.0.0.1",
    port: int = 8080,
    log_level: str = "info",
    access_log: bool = False,
    reload: bool = True,
    workers: int = 1,
) -> None:
    """Run uvicorn server."""
    LOGGER.info(f"uvicorn started: http://{host}:{port}/")
    uvicorn.run(
        app="src.core.api.app:create_app",
        host=host,
        port=port,
        log_level=log_level,
        access_log=access_log,
        reload=reload,
        reload_dirs=["core"],
        reload_delay=0.25,
        workers=workers,
        timeout_keep_alive=5,
        factory=True,
        log_config=None,
    )
    LOGGER.info("uvicorn finished")


if __name__ == "__main__":
    from src.core.configs.logs import configure_logging

    configure_logging()
    run_server()

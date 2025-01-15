"""Entrypoint."""

import logging
import sys

from fastapi import FastAPI

from src.core.api.app import create_app
from src.core.configs.logs import configure_logging

configure_logging()

LOGGER = logging.getLogger("app")


def run() -> FastAPI:
    """Run RestAPI.

    :return: FastAPI
    """
    app = create_app()
    return app


if __name__ == "__main__":
    try:
        LOGGER.info("starting app")
        run()
    except KeyboardInterrupt:
        LOGGER.info("finished app")
        sys.exit(0)

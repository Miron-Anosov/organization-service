"""Entrypoint."""

import logging

from src.core.api.app import run_server
from src.core.configs.logs import configure_logging

configure_logging()

logger = logging.getLogger("app")

if __name__ == "__main__":
    run_server()
    logger.info("starting app")

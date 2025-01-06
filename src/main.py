"""Entrypoint."""

import logging

from src.core.configs.logs import configure_logging

configure_logging()

logger = logging.getLogger("app")

if __name__ == "__main__":
    logger.info("starting app")

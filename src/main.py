"""Entrypoint."""

import logging
import sys

from fastapi import FastAPI

from src.core.api.app import create_app
from src.core.configs.env import settings
from src.core.configs.logs import configure_logging

configure_logging()

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


def run() -> FastAPI:
    """Run RestAPI.

    :return: FastAPI
    """
    app = create_app()
    return app

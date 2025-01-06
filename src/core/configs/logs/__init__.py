"""Configurate logging."""

import logging.config
from typing import Any

from src.core.configs.logs.log_config import log_config


def configure_logging(log_conf: dict[str, Any] = log_config) -> None:
    """Configure logging.

    :param log_conf: Logging configuration.
    :type log_conf: dict[str, Any]
    :return: None
    """
    logging.config.dictConfig(log_conf)

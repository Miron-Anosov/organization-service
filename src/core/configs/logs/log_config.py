"""Configurate logging."""

import logging
import sys

from src.core.configs.env import settings
from src.core.configs.logs.filters import LevelFilter
from src.core.configs.logs.formatters import JSONFormatter
from src.core.configs.logs.handlers import HTTPHandlerCustom

formatter = settings.webconf.FORMATTER_STREAM_LOG

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"()": JSONFormatter, "datefmt": "%Y-%m-%d %H:%M:%S"},
        "base": {"format": formatter, "datefmt": "%Y-%m-%d %H:%M:%S"},
    },
    "handlers": {
        "stream_json": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "stream": sys.stdout,
            "formatter": "json",
            "filters": ["info_filter"],
        },
        "stream_base_stderr": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "stream": sys.stderr,
            "formatter": "base",
        },
        "http_handler": {
            "()": HTTPHandlerCustom,
            "host": settings.webconf.host_logs,
            "url": "/log",
            "method": "POST",
            "formatter": "json",
            "level": settings.webconf.HTTP_LOG_LEVEL,
        },
    },
    "filters": {
        "info_filter": {
            "()": LevelFilter,
            "level": logging.INFO,
        }
    },
    "loggers": {
        "json": {
            "level": "DEBUG",
            "handlers": ["stream_json"],
            "propagate": False,
        },
        "http": {
            "level": "INFO",
            "propagate": False,
            "handlers": ["http_handler"],
        },
        "all": {
            "level": "INFO",
            "propagate": False,
            "handlers": ["http_handler", "stream_json", "stream_base_stderr"],
        },
        "minimal": {
            "level": settings.webconf.STREAM_LOG_LEVEL,
            "propagate": False,
            "handlers": ["stream_base_stderr"],
        },
    },
}

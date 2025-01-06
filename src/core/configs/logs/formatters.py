"""Formatters of logging."""

import json
import logging
from datetime import datetime
from logging import LogRecord


class JSONFormatter(logging.Formatter):
    """Logging formatter for JSON serialization."""

    def format(self, record: LogRecord) -> str:
        """Format the given record as JSON.

        :param record: The record.
        :return: The formatted record.
        """
        log_data = {
            "level": record.levelname,
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "logger": record.name,
            "line": record.lineno,
            "message": record.msg,
            "filename": record.filename,
            "path": record.pathname,
            "args": record.args,
            "exc_info": record.exc_info,
            "stack_info": record.stack_info,
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)

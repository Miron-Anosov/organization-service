"""Logs filters."""

import logging


class LevelFilter(logging.Filter):
    """Фильтр для логов определенного уровня."""

    def __init__(self, level: int) -> None:
        """Init filter."""
        super().__init__()
        self.level = level

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter record."""
        return record.levelno == self.level

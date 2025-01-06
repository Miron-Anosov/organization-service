"""HTTP handlers for logs."""

import datetime
import http.client
import json
import logging
from logging.handlers import HTTPHandler
from typing import Dict

logger = logging.getLogger("root")


class HTTPHandlerCustom(HTTPHandler):
    """Кастомный HTTPHandler для отправки логов в формате JSON."""

    def __init__(
        self,
        host: str,
        url: str,
        method: str = "POST",
        timeout: int = 5,
        secure: bool = False,
    ) -> None:
        """
        Инициализация handler'а с дополнительными параметрами.

        Args:
            host: Хост для отправки логов
            url: URL эндпоинта
            method: HTTP метод (по умолчанию POST)
            timeout: Таймаут соединения в секундах
            secure: Использовать HTTPS вместо HTTP
        """
        super().__init__(host, url, method, secure)
        self.timeout = timeout

    def mapLogRecord(self, record: logging.LogRecord) -> Dict[str, str]:
        """Формирует словарь с логами в формате JSON."""
        created_datetime = datetime.datetime.fromtimestamp(record.created)
        log_data = {
            "level": record.levelname,
            "logger": record.name,
            "timestamp": str(created_datetime.isoformat()),
            "line": str(record.lineno),
            "message": record.msg,
        }
        return log_data

    def emit(self, record: logging.LogRecord) -> None:
        """Переопределяет стандартное поведение HTTPHandler для передачи JSON."""  # noqa E501
        try:
            host = self.host
            url = self.url
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "PythonLoggingHTTPHandler/1.0",
            }

            # Формируем данные лога
            data = self.mapLogRecord(record)
            json_data = json.dumps(data)

            # Устанавливаем соединение
            connection = http.client.HTTPConnection(host, timeout=self.timeout)
            connection.request(
                self.method, url, body=json_data, headers=headers
            )

            response = connection.getresponse()
            response.read()
            if response.status >= 400:
                self.handleError(record)

            connection.close()
        except ConnectionRefusedError as connection_error:
            logging.error(
                "HTTPHandler connection refused: %s", str(connection_error)
            )
            self.handleError(record)
        except TimeoutError as timeout_error:
            logger.error("HTTPHandler timeout: %s", str(timeout_error))
            self.handleError(record)
        except Exception as exception:
            logging.error("HTTPHandler exception: %s", str(exception))

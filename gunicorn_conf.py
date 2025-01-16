"""Конфигурация Gunicorn."""

from src.core.configs.env import settings

# Количество рабочих процессов Gunicorn
workers = settings.gunicorn.GUNICORN_WORKERS

# Привязка к адресу
bind = settings.gunicorn.GUNICORN_BIND

# Уровень логирования
loglevel = settings.gunicorn.GUNICORN_LOG_LEVEL

# Путь к приложению
wsgi_app = settings.gunicorn.GUNICORN_WSGI_APP

# Класс рабочего процесса
worker_class = settings.gunicorn.GUNICORN_WORKER_CLASS

# Дополнительные параметры (если нужно)
timeout = settings.gunicorn.GUNICORN_TIMEOUT  # Таймаут для запросов
accesslog = (
    settings.gunicorn.GUNICORN_ACCESSLOG
)  # Логирование доступа в stdout
errorlog = settings.gunicorn.GUNICORN_ERRORLOG  # Логирование ошибок в stdout

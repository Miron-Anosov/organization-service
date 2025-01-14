"""Logging middleware."""

import logging
from typing import Awaitable, Callable

from fastapi import Request
from starlette.responses import Response as StarletteResponse

from src.core.configs.env import settings

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


async def logs_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[StarletteResponse]],
) -> StarletteResponse:
    """Middleware logger.

    :param request: Request object.
    :type request: StarletteRequest
    :param call_next: Call method.
    :type call_next: Callable[[Request], Awaitable[StarletteResponse]]
    :return: StarletteResponse object.
    :rtype: StarletteResponse
    """
    LOGGER.info(f"Request received: {request.method} {request.url}")
    response = await call_next(request)
    return response

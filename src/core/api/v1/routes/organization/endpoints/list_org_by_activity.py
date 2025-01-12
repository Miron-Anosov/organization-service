"""Endpoint for organization by activity."""

import logging
from typing import Annotated

from fastapi import Path
from starlette.responses import JSONResponse

from src.core.configs.env import settings

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


async def org_by_activity(
    activity: Annotated[
        int,
        Path(
            ...,
            description="The activity of the target organization",
            alias="activity",
        ),
    ]
) -> JSONResponse:
    """
    Вывод информации об организации по её идентификатору.

    :param activity: The activity of the target organization
    :type activity: int
    :return: JSONResponse
    """
    LOGGER.info("activity = %s", activity)
    return JSONResponse(content={"activity": activity})

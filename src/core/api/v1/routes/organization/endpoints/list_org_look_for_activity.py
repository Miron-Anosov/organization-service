"""Искать организации по виду деятельности."""

import logging
from typing import Annotated

from fastapi import Path
from starlette.responses import JSONResponse

from src.core.configs.env import settings

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


async def org_by_activities_tree(
    activity: Annotated[
        int,
        Path(
            ...,
            description="The activities tree by root activity",
            alias="activity",
        ),
    ]
) -> JSONResponse:
    """
    Искать организации по виду деятельности.

    Например, поиск по виду деятельности «Еда»,
    которая находится на первом уровне дерева, и чтобы нашлись все организации,
    которые относятся к видам деятельности, лежащим внутри.
    Т.е. в результатах поиска должны отобразиться организации
    с видом деятельности Еда, Мясная продукция, Молочная продукция.

    :param activity:
    :type activity: int
    :return: JSONResponse
    """
    LOGGER.info("activity = %s", activity)
    return JSONResponse(content={"activity": activity})

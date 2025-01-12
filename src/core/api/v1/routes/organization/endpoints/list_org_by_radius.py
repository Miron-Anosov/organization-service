"""Endpoint for organization by location."""

import logging
from typing import Annotated, Tuple

from fastapi import Path
from starlette.responses import JSONResponse

from src.core.configs.env import settings

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


async def org_by_location(
    lon: Annotated[
        float,
        Path(
            ...,
            description="The location of the target organization",
            alias="lon",
        ),
    ],
    lat: Annotated[
        float,
        Path(
            ...,
            description="The location of the target organization",
            alias="lat",
        ),
    ],
) -> JSONResponse:
    """
    Вывод список организаций.

    Которые находятся в заданном радиусе/прямоугольной области
    относительно указанной точки на карте. список зданий.

    :param lon: longitude
    :type lon: float
    :param lat: latitude
    :type lat: float
    :return: JSONResponse
    """
    loc = lat, lon
    LOGGER.info("location = %s", f"{loc!r}")
    return JSONResponse(content={"location": f"{loc!r}"})

"""Endpoint for organization by location."""

import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from src.core.api.v1.presentation.requests.location import (
    LocationRadiusRequest,
    LocationRectangleRequest,
)
from src.core.api.v1.routes.utils.resp_error import error_404_not_found
from src.core.api.v1.routes.utils.resp_org_full_data import resp_org_full_data
from src.core.configs.env import settings
from src.core.infrastructure.database import db

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


async def get_orgs_by_location(
    radius: Annotated[LocationRadiusRequest, Depends(LocationRadiusRequest)],
    rectangle: Annotated[
        LocationRectangleRequest, Depends(LocationRectangleRequest)
    ],
) -> JSONResponse:
    """Вывод список организаций.

    Которые находятся в заданном радиусе/прямоугольной области
    относительно указанной точки на карте. список зданий.
    :param radius:  Organizations by radius.
    :type radius: LocationRadiusRequest
    :param rectangle:  Organizations by rectangle.
    :type rectangle: LocationRectangleRequest
    :return: JSONResponse
    """
    try:
        if bool(radius) == bool(rectangle):
            raise error_404_not_found()

        async with db as session:

            if rectangle:
                validated_rec = rectangle.validate()

                if not validated_rec:
                    LOGGER.error(
                        "bad request location by rectangle: %s",
                        validated_rec,
                    )
                    raise error_404_not_found()

                organizations = await db.location.get_objects_in_rectangle(
                    bounds=validated_rec.to_tuple(),
                    session=session,
                )
            else:
                validated_rad = radius.validate()
                if not validated_rad:
                    LOGGER.error(
                        "bad request location by radius: %s",
                        validated_rad,
                    )
                    raise error_404_not_found()

                organizations = await db.location.get_objects_in_radius(
                    point=validated_rad.to_tuple_location(),
                    radius=validated_rad.to_float_radius(),
                    session=session,
                )

            if not organizations:
                LOGGER.info(
                    "organization not found by location. Location: %s",
                    validated_rad,
                )
                raise error_404_not_found()

            return JSONResponse(
                content=[
                    resp_org_full_data(organization=organization)
                    for organization in organizations
                ],
                status_code=status.HTTP_200_OK,
                media_type="application/json",
            )

    except HTTPException as http_exception:
        LOGGER.error(http_exception)
        raise http_exception

    except Exception as e:
        LOGGER.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

"""Endpoint for listing organizations by building."""

import logging
from typing import Annotated

from fastapi.params import Depends
from starlette import status
from starlette.responses import JSONResponse

from src.core.api.v1.presentation.requests.biulding import BuildingIDRequest
from src.core.api.v1.routes.utils.resp_error import error_404_not_found
from src.core.api.v1.routes.utils.resp_org_full_data import resp_org_full_data
from src.core.configs.env import settings
from src.core.infrastructure.database import db

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


async def org_by_building(
    req: Annotated[BuildingIDRequest, Depends(BuildingIDRequest)]
) -> JSONResponse:
    """Получить список всех организаций находящихся в конкретном здании.

    :param req:
    :type req: BuildingIDRequest
    :return: JSONResponse
    """
    async with db as session:
        org = await db.org.get_by_building(building_id=req.id, session=session)

    if org is None:
        LOGGER.info("organization not found. ID: %s", req.id)
        raise error_404_not_found()

    LOGGER.info(
        "Organization found in building. ID: %s",
        req.id,
    )

    return JSONResponse(
        content=[
            resp_org_full_data(organization=organization)
            for organization in org
        ],
        status_code=status.HTTP_200_OK,
        media_type="application/json",
    )

"""Endpoint for information about organization by ID."""

import logging
from typing import Annotated

from fastapi import Depends
from starlette import status
from starlette.responses import JSONResponse

from src.core.api.v1.presentation.requests.organization import (
    OrganizationByIDRequest,
)
from src.core.api.v1.routes.utils.resp_error import error_404_not_found
from src.core.api.v1.routes.utils.resp_org_full_data import resp_org_full_data
from src.core.configs.env import settings
from src.core.infrastructure.database import db

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


async def org_by_id(
    organization: Annotated[
        OrganizationByIDRequest, Depends(OrganizationByIDRequest)
    ],
) -> JSONResponse:
    """
    Вывод информации об организации по её идентификатору.

    :param organization: The ID of the target organization
    :type organization: OrganizationByIDRequest
    :return: JSONResponse
    """
    async with db as session:
        org = await db.org.get_by_id(id_obj=organization.id, session=session)

    if org is None:
        LOGGER.info("organization not found. ID: %s", organization.id)
        raise error_404_not_found()

    LOGGER.info("Organization found. ID: %s, Name: %s", org.id, org.name)

    return JSONResponse(
        content=resp_org_full_data(organization=org),
        status_code=status.HTTP_200_OK,
        media_type="application/json",
    )

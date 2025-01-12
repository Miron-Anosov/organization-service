"""Endpoint for getting organizations by name."""

import logging
from typing import Annotated

from fastapi import Query
from starlette import status
from starlette.responses import JSONResponse

from src.core.api.v1.routes.utils.resp_error import error_404_not_found
from src.core.api.v1.routes.utils.resp_org_full_data import resp_org_full_data
from src.core.configs.env import settings
from src.core.infrastructure.database import db

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


async def org_by_name(
    org_name: Annotated[
        str,
        Query(..., description="Look for organization by name", alias="name"),
    ]
) -> JSONResponse:
    """Поиск организации по названию.

    :param org_name: The name of the organization.
    :type org_name: str
    :return: JSONResponse
    """
    async with db as session:
        org = await db.org.get_by_name(name=org_name, session=session)

    if org is None:
        LOGGER.info("""organization "%s" not found.""", org_name)
        raise error_404_not_found()

    LOGGER.info("Organization found. Name: %s, Name: %s", org.id, org.name)

    return JSONResponse(
        content=resp_org_full_data(organization=org),
        status_code=status.HTTP_200_OK,
        media_type="application/json",
    )

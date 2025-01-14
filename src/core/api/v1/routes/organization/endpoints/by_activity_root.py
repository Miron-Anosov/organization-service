"""Endpoint for tree of activity organization."""

import logging
from typing import Annotated

from fastapi import Depends
from starlette import status
from starlette.responses import JSONResponse

from src.core.api.v1.presentation.requests.activity import ActivityRequest
from src.core.api.v1.routes.utils.resp_error import error_404_not_found
from src.core.api.v1.routes.utils.resp_orgs_by_activity import (
    resp_org_by_activity_data,
)
from src.core.configs.env import settings
from src.core.infrastructure.database import db

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


async def get_orgs_by_activity_root(
    req: Annotated[ActivityRequest, Depends(ActivityRequest)]
) -> JSONResponse:
    """
    Искать организации которые относятся к указанному виду деятельности.

    :param req: The activity of the target organization
    :type req: ActivityRequest
    :return: JSONResponse
    """
    async with db as session:
        root_activity = await db.activity.get_activity(
            activity_name=req.name, session=session
        )

    if root_activity is None:
        LOGGER.info("organization not found. Activity: %s", req.name)
        raise error_404_not_found()

    LOGGER.info("Organization found in activity. Activity: %s", req.name)

    return JSONResponse(
        content=resp_org_by_activity_data(activity=root_activity),
        status_code=status.HTTP_200_OK,
        media_type="application/json",
    )

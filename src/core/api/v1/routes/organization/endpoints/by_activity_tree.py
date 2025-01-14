"""Endpoint for activity with children."""

import logging
from typing import Annotated

from fastapi import Depends
from starlette import status
from starlette.responses import JSONResponse

from src.core.api.v1.presentation.requests.activity import ActivityRequest
from src.core.api.v1.routes.utils.resp_error import error_404_not_found
from src.core.api.v1.routes.utils.resp_org_full_data import resp_org_full_data
from src.core.configs.env import settings
from src.core.infrastructure.database import db

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


async def get_activity_with_children(
    req: Annotated[ActivityRequest, Depends(ActivityRequest)],
) -> JSONResponse:
    """
    Искать организации по виду деятельности.

    Например, поиск по виду деятельности «Еда»,
    которая находится на первом уровне дерева, и чтобы нашлись все организации,
    которые относятся к видам деятельности, лежащим внутри.
    Т.е. в результатах поиска должны отобразиться организации
    с видом деятельности Еда, Мясная продукция, Молочная продукция.

    :param req:
    :type req: ActivityRequest
    :return: JSONResponse
    """
    async with db as session:
        activity = await db.activity.get_activity(
            activity_name=req.name, session=session, with_children=True
        )

        if activity is None:
            LOGGER.info(
                "organization not found. Activity: %s",
                req.name,
            )

            raise error_404_not_found()

        LOGGER.info("Organization found in activity. Activity: %s", req.name)

        all_organizations = set(activity.organizations)

        for child in activity.children:
            all_organizations.update(child.organizations)
            for grandchild in child.children:
                all_organizations.update(grandchild.organizations)

        return JSONResponse(
            content=[
                resp_org_full_data(organization=organization)
                for organization in all_organizations
            ],
            status_code=status.HTTP_200_OK,
            media_type="application/json",
        )

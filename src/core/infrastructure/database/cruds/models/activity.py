"""Activity CRUD API."""

import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.configs.env import settings
from src.core.infrastructure.database.cruds.models.base import (
    CRUDWithOneSubModel,
)
from src.core.infrastructure.database.schemas.activity import Activity
from src.core.infrastructure.database.schemas.organizations import Organization

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)


class ActivityCRUD(CRUDWithOneSubModel[Activity, Organization]):
    """Activity CRUD."""

    async def get_activity(
        self,
        activity_name: str,
        session: AsyncSession,
        with_children: bool = False,
    ) -> Activity | None:
        """Return Organization by activity type.

        :param activity_name: Activity name.
        :param session: SQLAlchemy session.
        :param with_children: Return children activities.
        :return: Organization by activity type.
        """
        try:

            stmt = select(self.model).where(self.model.name == activity_name)

            if with_children:
                stmt = stmt.options(
                    selectinload(self.model.organizations).selectinload(
                        self.submodel.activities
                    ),
                    selectinload(self.model.children)
                    .selectinload(self.model.organizations)
                    .selectinload(self.submodel.activities),
                    selectinload(self.model.children)
                    .selectinload(self.model.children)
                    .selectinload(self.model.organizations)
                    .selectinload(self.submodel.activities),
                )

            result = await session.execute(stmt)
            activity = result.scalar_one_or_none()
            return activity if activity else None
        except SQLAlchemyError as e:
            LOGGER.error("Error retrieving activity by name: %s", str(e))
            return None

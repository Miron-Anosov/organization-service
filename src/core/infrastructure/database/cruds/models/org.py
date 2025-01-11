"""Organization CRUD API."""

import logging
from typing import Any, List, Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.infrastructure.database.cruds.models.base import CRUDBase
from src.core.infrastructure.database.schemas.organizations import Organization

LOGGER = logging.getLogger(__name__)


class OrganizationCRUD(CRUDBase[Organization]):
    """Organization CRUD."""

    async def get_by_id(
        self, session: AsyncSession, id_obj: Any
    ) -> Optional[Organization]:
        """Get Organization by ID."""
        try:
            return await session.get(self.model, id_obj)
        except SQLAlchemyError as e:
            LOGGER.error("Error retrieving object: %s", str(e))
            return None

    async def get_by_name(
        self, session: AsyncSession, name: str
    ) -> Optional[Organization]:
        """Get Organization by name."""
        try:
            stmt = select(self.model).where(self.model.name == name)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            LOGGER.error("Error retrieving organization by name: %s", str(e))
            return None

    async def get_by_building(
        self,
        building_id: int,
        session: AsyncSession,
    ) -> List[Organization]:
        """Return Organization by building ID."""
        try:
            stmt = select(self.model).where(
                self.model.building_id == building_id
            )
            result = await session.execute(stmt)
            d = result.scalars().all()
            return list(d) if d else []
        except SQLAlchemyError as e:
            LOGGER.error("Error retrieving organization by name: %s", str(e))
            return []

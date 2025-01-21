"""Organization CRUD API."""

import logging
from typing import Any, List, Optional

from opentelemetry import trace
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.infrastructure.database.cruds.models.base import CRUDBase
from src.core.infrastructure.database.schemas.organizations import Organization

LOGGER = logging.getLogger(__name__)
TRACER = trace.get_tracer(__name__)


class OrganizationCRUD(CRUDBase[Organization]):
    """Organization CRUD."""

    async def get_by_id(
        self, session: AsyncSession, id_obj: Any
    ) -> Optional[Organization]:
        """Get Organization by ID."""
        with TRACER.start_as_current_span("get_organization_by_id") as span:
            span.set_attribute("organization.id", id_obj)
            try:
                organization = await session.get(self.model, id_obj)
                span.set_attribute(
                    "db.result", "success" if organization else "not_found"
                )
                return organization
            except SQLAlchemyError as e:
                span.record_exception(e)
                span.set_status(
                    trace.status.Status(trace.status.StatusCode.ERROR)
                )
                LOGGER.error("Error retrieving object: %s", str(e))
                return None

    async def get_by_name(
        self, session: AsyncSession, name: str
    ) -> Optional[Organization]:
        """Get Organization by name."""
        with TRACER.start_as_current_span("get_organization_by_name") as span:
            span.set_attribute("organization.name", name)
            try:
                stmt = select(self.model).where(self.model.name == name)
                result = await session.execute(stmt)
                organization = result.scalar_one_or_none()
                span.set_attribute(
                    "db.result", "success" if organization else "not_found"
                )
                return organization
            except SQLAlchemyError as e:
                span.record_exception(e)
                span.set_status(
                    trace.status.Status(trace.status.StatusCode.ERROR)
                )
                LOGGER.error(
                    "Error retrieving organization by name: %s", str(e)
                )
                return None

    async def get_by_building(
        self,
        building_id: int,
        session: AsyncSession,
    ) -> List[Organization]:
        """Return Organization by building ID."""
        with TRACER.start_as_current_span(
            "get_organization_by_building"
        ) as span:
            span.set_attribute("building.id", building_id)
            try:
                stmt = select(self.model).where(
                    self.model.building_id == building_id
                )
                result = await session.execute(stmt)
                organizations = list(result.scalars().all())
                span.set_attribute("db.result_count", len(organizations))
                return organizations
            except SQLAlchemyError as e:
                span.record_exception(e)
                span.set_status(
                    trace.status.Status(trace.status.StatusCode.ERROR)
                )
                LOGGER.error(
                    "Error retrieving organization by building ID: %s", str(e)
                )
                return []

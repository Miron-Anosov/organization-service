"""Location CRUD API."""

import logging
from typing import List

from geoalchemy2.functions import (
    ST_Covers,
    ST_DWithin,
    ST_GeomFromText,
    ST_MakeEnvelope,
    ST_SetSRID,
    ST_Transform,
)
from opentelemetry import trace
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.configs.env import settings
from src.core.infrastructure.database.cruds.models.base import (
    CRUDWithOneSubModel,
)
from src.core.infrastructure.database.schemas.buildings import Building
from src.core.infrastructure.database.schemas.organizations import Organization

LOGGER = logging.getLogger(settings.webconf.LOG_OUT_COMMON)
TRACER = trace.get_tracer(__name__)


class OrganizationByLocationCRUD(CRUDWithOneSubModel[Organization, Building]):
    """Location CRUD."""

    async def get_objects_in_rectangle(
        self,
        bounds: tuple[float, float, float, float],
        session: AsyncSession,
    ) -> List[Organization]:
        """Return Organization by activity type.

        :param bounds: Rectangle by location
        :param session: SQLAlchemy session.
        :return: Organization by activity type.
        """
        with TRACER.start_as_current_span("get_objects_in_rectangle") as span:
            span.set_attribute("bounds", bounds)
            try:
                min_lon, max_lon, min_lat, max_lat = bounds
                rectangle = ST_SetSRID(
                    ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat),
                    4326,
                )

                stmt = (
                    select(self.model)
                    .join(self.submodel)
                    .where(ST_Covers(rectangle, self.submodel.location))
                )

                result = await session.execute(stmt)
                organizations = result.scalars().all()
                span.set_attribute(
                    "db.result", "success" if organizations else "not_found"
                )
                return list(organizations) if organizations else []
            except SQLAlchemyError as e:
                span.record_exception(e)
                span.set_status(
                    trace.status.Status(trace.status.StatusCode.ERROR)
                )
                LOGGER.error(
                    "Error retrieving organization by location: %s", str(e)
                )
                return []

    async def get_objects_in_radius(
        self,
        point: tuple[float, float],
        radius: float,
        session: AsyncSession,
    ) -> List[Organization]:
        """
        Найти объекты в заданном радиусе от точки.

        :param session: Сессия SQLAlchemy.
        :param point: Точка (широта, долгота).
        :param radius: Радиус в метрах.
        :return: Список объектов.
        """
        with TRACER.start_as_current_span("get_objects_in_radius") as span:
            span.set_attribute("radius", radius)
            try:
                point_wkt = f"SRID=4326;POINT({point[0]} {point[1]})"
                stmt = (
                    select(self.model)
                    .join(self.submodel)
                    .where(
                        ST_DWithin(
                            ST_Transform(self.submodel.location, 3857),
                            ST_Transform(ST_GeomFromText(point_wkt), 3857),
                            radius,
                        )
                    )
                )

                result = await session.execute(stmt)
                span.set_attribute(
                    "db.result", "success" if result else "not_found"
                )
                return list(result.scalars().unique().all())
            except SQLAlchemyError as e:
                span.record_exception(e)
                span.set_status(
                    trace.status.Status(trace.status.StatusCode.ERROR)
                )
                LOGGER.error(
                    "Error retrieving organization by location: %s", str(e)
                )
                return []

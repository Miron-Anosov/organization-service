"""Sqlalchemy models for buildings."""

from geoalchemy2 import Geometry
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.infrastructure.database.schemas.base import BaseModel


class Building(BaseModel):
    """Building model."""

    __tablename__ = "building"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    address: Mapped[str] = mapped_column(nullable=False, index=True)
    location: Mapped[str] = mapped_column(
        Geometry("POINT", srid=4326), nullable=False
    )

    organizations = relationship(
        "Organization",
        back_populates="building",
        lazy="selectin",
    )

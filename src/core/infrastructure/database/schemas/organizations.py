"""Sqlalchemy models for organization."""

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.infrastructure.database.schemas.base import BaseModel


class Organization(BaseModel):
    """Organization model."""

    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    building_id: Mapped[int] = mapped_column(
        ForeignKey("building.id", ondelete="CASCADE"), nullable=False
    )

    building = relationship(
        "Building",
        back_populates="organizations",
        lazy="selectin",
    )
    phone_numbers = relationship(
        "PhoneNumber",
        back_populates="organization",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    activities = relationship(
        "Activity",
        secondary="organization_activity",
        back_populates="organizations",
        lazy="selectin",
    )

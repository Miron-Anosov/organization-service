"""Organization's activity schema."""

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from src.core.infrastructure.database.schemas.base import BaseModel


class Activity(BaseModel):
    """Activity model."""

    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activity.id", ondelete="CASCADE"), nullable=True
    )
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    children = relationship(
        "Activity",
        backref=backref("parent", remote_side=[id]),
        cascade="all, delete-orphan",
        single_parent=True,
        lazy="selectin",
    )

    organizations = relationship(
        "Organization",
        secondary="organization_activity",
        back_populates="activities",
        lazy="selectin",
    )

    __table_args__ = (
        CheckConstraint(sqltext="level <= 3", name="check_max_level"),
    )


class OrganizationActivity(BaseModel):
    """Organization's activity model."""

    __tablename__ = "organization_activity"

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activity.id", ondelete="CASCADE"),
        primary_key=True,
    )

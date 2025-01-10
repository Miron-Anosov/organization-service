"""Organization's phone schema."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.infrastructure.database.schemas.base import BaseModel


class PhoneNumber(BaseModel):
    """Phone Number Model."""

    __tablename__ = "phone_number"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    number: Mapped[str] = mapped_column(String, nullable=False)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE"), nullable=False
    )

    organization = relationship(
        "Organization",
        back_populates="phone_numbers",
        lazy="selectin",
    )

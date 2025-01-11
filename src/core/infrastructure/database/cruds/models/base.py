"""Base CRUD."""

from typing import Type

from src.core.infrastructure.database.schemas.base import BaseModel


class CRUDBase[T: BaseModel]:  # noqa D101
    """Base class for all CRUD models.

    Provides basic CRUD operations for a given SQLAlchemy model.
    """

    def __init__(self, model: Type[T]):
        """Initialize CRUD model."""
        self.model = model

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


class CRUDWithOneSubModel[T: BaseModel, BaseModel]:  # noqa D101
    """Base class for sub query."""

    def __init__(self, model: Type[T], submodel: Type[BaseModel]) -> None:
        """Initialize CRUD model.

        :param model: SQLAlchemy model
        :param submodel: sub model
        :type model: Type[BaseModel]
        :type submodel: Type[BaseModel]
        """
        self.model = model
        self.submodel = submodel

"""Facade ORM models."""

from src.core.infrastructure.database.cruds.models.org import OrganizationCRUD


class Crud:
    """Combined interface for all CRUD operations."""

    def __init__(
        self,
        org: OrganizationCRUD,
    ) -> None:
        """Initialize Crud with specific CRUD instances."""
        self.org = org
        pass

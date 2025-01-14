"""Facade ORM models."""

from src.core.infrastructure.database.cruds.models.activity import ActivityCRUD
from src.core.infrastructure.database.cruds.models.location import (
    OrganizationByLocationCRUD,
)
from src.core.infrastructure.database.cruds.models.org import OrganizationCRUD


class Crud:
    """Combined interface for all CRUD operations."""

    def __init__(
        self,
        org: OrganizationCRUD,
        location: OrganizationByLocationCRUD,
        activity: ActivityCRUD,
    ) -> None:
        """Initialize Crud with specific CRUD instances.

        :param org: Organization CRUD
        :type org: OrganizationCRUD
        :param location: Location CRUD
        :type location: OrganizationByLocationCRUD
        :param activity: Activity CRUD
        :type activity: ActivityCRUD

        """
        self.org = org
        self.location = location
        self.activity = activity

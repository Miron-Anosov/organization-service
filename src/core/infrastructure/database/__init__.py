"""DB package."""

from src.core.infrastructure.database.client import Connector
from src.core.infrastructure.database.cruds.facade import Crud
from src.core.infrastructure.database.cruds.models.org import OrganizationCRUD
from src.core.infrastructure.database.schemas.activity import (
    Activity,
    OrganizationActivity,
)
from src.core.infrastructure.database.schemas.buildings import Building
from src.core.infrastructure.database.schemas.organizations import Organization
from src.core.infrastructure.database.schemas.phones import PhoneNumber


def db_client() -> Connector:
    """Create a Database worker.

    :return: Connector worker.
    """
    return Connector(org=OrganizationCRUD(Organization))


db = db_client()

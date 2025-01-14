"""Request requirements of organizations."""

from typing import Annotated

from fastapi import Path, Query


class OrganizationByNameRequest:
    """Request requirements of organization by name."""

    def __init__(
        self,
        name: Annotated[
            str,
            Query(
                ..., description="Look for organization by name", alias="name"
            ),
        ],
    ) -> None:
        """Query requirements of organization by name.

        :param name: Organization name.
        :type name: str
        :return None
        """
        self.name = name


class OrganizationByIDRequest:
    """Request requirements of organization by id."""

    def __init__(
        self,
        id_org: Annotated[
            int,
            Path(
                ...,
                example=1,
                description="The ID of the target organization",
                alias="id",
            ),
        ],
    ) -> None:
        """Path requirements of organization by id.

        :param id_org: ID of the target organization
        :type id_org: int
        :return None
        """
        self.id = id_org

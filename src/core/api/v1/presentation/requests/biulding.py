"""Path param for activity request."""

from typing import Annotated

from fastapi.params import Query


class BuildingIDRequest:
    """Http param for building request."""

    def __init__(
        self,
        building_id: Annotated[
            int,
            Query(
                ...,
                example=1,
                description="Get organization by building ID",
                alias="id",
            ),
        ],
    ) -> None:
        """Initialize ActivityRootRequest class.

        :param building_id: Building ID.
        :type building_id: int
        """
        self.id = building_id

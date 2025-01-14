"""Path param for activity request."""

from typing import Annotated

from fastapi import Path

from src.core.api.configs.v1.types_activity import ACTIVITIES


class ActivityRequest:
    """Http request param."""

    def __init__(
        self,
        name: Annotated[
            ACTIVITIES,
            Path(
                ...,
                description="The activity of the target organization",
                alias="activity",
            ),
        ],
    ) -> None:
        """Initialize ActivityRootRequest class.

        :param name: The name of the activity.
        :type name: ACTIVITIES
        """
        self.name = name

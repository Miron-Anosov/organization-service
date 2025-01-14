"""Path param for activity request."""

from typing import Annotated

from fastapi import Path

from src.core.api.configs.v1.types_activity import ACTIVITIES


class ActivityRequest:
    """Http request param."""

    def __init__(
        self,
        activity: Annotated[
            ACTIVITIES,
            Path(
                ...,
                description="The activity of the target organization",
                alias="activity",
            ),
        ],
    ) -> None:
        """Initialize ActivityRootRequest class."""
        self.activity = activity

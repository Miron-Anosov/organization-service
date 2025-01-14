"""Response util for organization data."""

from typing import Any, List

from src.core.api.v1.presentation.responses.organization import (
    ActivityResponse,
    BuildingResponse,
    Location,
    OrganizationResponse,
    PhoneNumberResponse,
)
from src.core.api.v1.routes.utils.extractor_geo import extract_coordinates
from src.core.infrastructure.database.schemas.activity import Activity


def resp_org_by_activity_data(
    activity: Activity,
) -> List[dict[str, Any]]:
    """Return OrganizationResponse data for json.

    :param activity: Orm Activity.
    :return: OrganizationResponse data.
    """
    return [
        OrganizationResponse(
            id=org.id,
            name=org.name,
            building=BuildingResponse(
                id=org.building.id,
                address=org.building.address,
                location=Location(
                    latitude=extract_coordinates(org.building.location)[1],
                    longitude=extract_coordinates(org.building.location)[0],
                ),
            ),
            phones=[
                PhoneNumberResponse(phone=phone.number)
                for phone in org.phone_numbers
            ],
            activity=[ActivityResponse(name=activity.name)],
        ).model_dump()
        for org in activity.organizations
    ]

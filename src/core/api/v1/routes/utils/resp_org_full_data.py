"""Response util for organization data."""

from typing import Any

from src.core.api.v1.presentation.responses.organization import (
    ActivityResponse,
    BuildingResponse,
    Location,
    OrganizationResponse,
    PhoneNumberResponse,
)
from src.core.api.v1.routes.utils.extractor_geo import extract_coordinates
from src.core.infrastructure.database.schemas.organizations import Organization


def resp_org_full_data(
    organization: Organization,
) -> dict[str, Any]:
    """Return OrganizationResponse data for json.

    :param organization: Orm Organization.
    :return: OrganizationResponse data.
    """
    return OrganizationResponse(
        id=organization.id,
        name=organization.name,
        building=BuildingResponse(
            id=organization.building.id,
            address=organization.building.address,
            location=Location(
                latitude=extract_coordinates(organization.building.location)[
                    1
                ],
                longitude=extract_coordinates(organization.building.location)[
                    0
                ],
            ),
        ),
        phones=[
            PhoneNumberResponse(phone=phone.number)
            for phone in organization.phone_numbers
        ],
        activity=[
            ActivityResponse(name=activity.name)
            for activity in organization.activities
        ],
    ).model_dump()

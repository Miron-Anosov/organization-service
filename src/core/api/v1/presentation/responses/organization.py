"""Response Organization model."""

from typing import List

import pydantic
from pydantic import BaseModel, Field


class ActivityResponse(BaseModel):
    """Activity response model."""

    name: str


class PhoneNumberResponse(BaseModel):
    """Phone Number response."""

    phone: str = Field(..., alias="phone")


class BuildingResponse(BaseModel):
    """Building response."""

    id: int = Field(..., alias="id")
    address: str = Field(..., alias="address")
    location: tuple[float, float] = Field(..., alias="location")


class OrganizationResponse(BaseModel):
    """Organization response."""

    id: int = Field(..., alias="id")
    name: str
    building: BuildingResponse
    phones: List[PhoneNumberResponse]
    activity: List[ActivityResponse]

    model_config = pydantic.ConfigDict(
        from_attributes=True,
        title="Organization Model",
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Verysell Акционерное общество",
                "building": {
                    "id": 11,
                    "address": "Задонск, Братцевская, д. 95",
                    "location": [-52.105232, -9.719463],
                },
                "phones": [
                    {"phone": "+7 (183) 468-16-28"},
                    {"phone": "+7 (348) 245-24-87"},
                ],
                "activity": [
                    {"name": "Еда"},
                    {"name": "Кондитерские изделия"},
                    {"name": "Легковые"},
                ],
            }
        },
    )

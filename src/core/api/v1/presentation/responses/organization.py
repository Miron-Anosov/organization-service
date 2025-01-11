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
        title="Organization Response",
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


class CollectionOrganizationResponse(BaseModel):
    """Collection organization response."""

    organizations: List[OrganizationResponse]

    model_config = pydantic.ConfigDict(
        from_attributes=True,
        title="Organizations Response",
        json_schema_extra={
            "example": [
                {
                    "id": 1,
                    "name": "«Мон’Дэлис Русь» Общество с ограниченной ответственностью",  # noqa E501
                    "building": {
                        "id": 11,
                        "address": "Нижний Новгород, Хорошевская, д. 74",
                        "location": [37.205475, 3.463513],
                    },
                    "phones": [
                        {"phone": "+7 (453) 901-05-32"},
                        {"phone": "+7 (737) 328-54-24"},
                        {"phone": "+7 (489) 318-09-95"},
                    ],
                    "activity": [{"name": "Легковые"}, {"name": "Запчасти"}],
                },
                {
                    "id": 6,
                    "name": "Трата-та 25",
                    "building": {
                        "id": 11,
                        "address": "Нижний Новгород, Хорошевская, д. 74",
                        "location": [37.205475, 3.463513],
                    },
                    "phones": [],
                    "activity": [],
                },
            ]
        },
    )

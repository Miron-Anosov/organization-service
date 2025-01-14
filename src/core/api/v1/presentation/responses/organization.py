"""Response Organization model."""

from typing import List

import pydantic
from pydantic import BaseModel, Field


class Location(BaseModel):
    """Location model."""

    longitude: float = Field(..., alias="longitude")
    latitude: float = Field(..., alias="latitude")


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
    location: Location


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
                "name": "«Швабе» Общество с ограниченной ответственностью",
                "building": {
                    "id": 6,
                    "address": "Дудинка, Черкасский М., д. 39",
                    "location": {
                        "longitude": 58.067381,
                        "latitude": 113.130354,
                    },
                },
                "phones": [
                    {"phone": "+7 (561) 115-61-70"},
                    {"phone": "+7 (463) 315-91-93"},
                    {"phone": "+7 (593) 611-16-72"},
                ],
                "activity": [
                    {"name": "Внедорожники"},
                    {"name": "Почтовая"},
                    {"name": "Срочный"},
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
                    "id": 24,
                    "name": "ГК ПИК Публичное акционерное общество",
                    "building": {
                        "id": 1,
                        "address": "Дудинка, Черкасский М., д. 39",
                        "location": {
                            "longitude": -9.263891,
                            "latitude": -150.676573,
                        },
                    },
                    "phones": [{"phone": "+7 (716) 065-56-96"}],
                    "activity": [{"name": "Грузовые"}],
                },
                {
                    "id": 27,
                    "name": "«Водоканал Санкт-Петербурга» Публичное акционерное общество",  # noqa E501
                    "building": {
                        "id": 1,
                        "address": "Дудинка, Черкасский М., д. 39",
                        "location": {
                            "longitude": -9.263891,
                            "latitude": -150.676573,
                        },
                    },
                    "phones": [
                        {"phone": "+7 (913) 229-53-87"},
                        {"phone": "+7 (546) 681-68-78"},
                        {"phone": "+7 (336) 392-43-24"},
                    ],
                    "activity": [
                        {"name": "Колбасы"},
                        {"name": "Экспресс"},
                        {"name": "Фуры"},
                    ],
                },  # noqa E501
                {
                    "id": 29,
                    "name": "Евросиб Акционерное общество",
                    "building": {
                        "id": 1,
                        "address": "Дудинка, Черкасский М., д. 39",
                        "location": {
                            "longitude": -9.263891,
                            "latitude": -150.676573,
                        },
                    },
                    "phones": [
                        {"phone": "+7 (158) 064-37-24"},
                        {"phone": "+7 (322) 482-65-45"},
                        {"phone": "+7 (531) 441-12-73"},
                    ],
                    "activity": [{"name": "Еда"}],
                },
                {
                    "id": 32,
                    "name": "«Тактическое ракетное вооружение» Акционерное общество",  # noqa E501
                    "building": {
                        "id": 1,
                        "address": "Дудинка, Черкасский М., д. 39",
                        "location": {
                            "longitude": -9.263891,
                            "latitude": -150.676573,
                        },
                    },
                    "phones": [
                        {"phone": "+7 (839) 123-64-04"},
                        {"phone": "+7 (841) 136-25-68"},
                    ],
                    "activity": [{"name": "Конфеты"}],
                },
                {
                    "id": 37,
                    "name": "Акционерный банк «Россия» Публичное акционерное общество",  # noqa E501
                    "building": {
                        "id": 1,
                        "address": "Дудинка, Черкасский М., д. 39",
                        "location": {
                            "longitude": -9.263891,
                            "latitude": -150.676573,
                        },
                    },
                    "phones": [{"phone": "+7 (876) 592-35-45"}],
                    "activity": [{"name": "Еда"}],
                },
            ]
        },
    )

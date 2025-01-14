"""Request objects by location."""

from typing import Annotated, Optional

from fastapi import Query

from src.core.api.v1.routes.utils.dto.location import (
    LocationRadiusDTO,
    LocationRectangleDTO,
)


class LocationRadiusRequest:
    """LocationRadiusRequest."""

    def __init__(
        self,
        lon: Annotated[
            float | None,
            Query(
                ...,
                description="Radius. Longitude of the target",
                alias="lon",
                ge=-180,
                le=180,
            ),
        ] = None,
        lat: Annotated[
            float | None,
            Query(
                ...,
                description="Radius. Latitude of the target",
                alias="lat",
                ge=-90,
                le=90,
            ),
        ] = None,
        radius: Annotated[
            float | None,
            Query(
                ...,
                description="Radius. Target range in meters",
                alias="radius",
                gt=0,
            ),
        ] = None,
    ) -> None:
        """Location by radius.

        :param lon: Longitude of the target
        :param lat: Latitude of the target
        :param radius: Target range in meters
        :type lon: Annotated[float, float]
        :type lat: Annotated[float, float]
        :type radius: Annotated[float, float]
        :return None
        """
        self.lon = lon
        self.lat = lat
        self.radius = radius

    def __bool__(self) -> bool:
        """Return True if all params are valid.

        :return: True if all params are valid.
        :rtype: bool
        """
        return all(
            isinstance(value, (float, int))
            for value in (
                self.lon,
                self.lat,
            )
        )

    def validate(self) -> Optional["LocationRadiusDTO"]:
        """Validate if all params are valid.

        :return: True if all params are valid.
        :rtype: Optional["LocationRadiusDTO"]
        """
        if self.lon is None or self.lat is None or self.radius is None:
            return None

        return LocationRadiusDTO(
            lon=self.lon, lat=self.lat, radius=self.radius
        )


class LocationRectangleRequest:
    """Location query params."""

    def __init__(
        self,
        lon_min: Annotated[
            float | None,
            Query(
                ...,
                description="Rectangle. Min longitude",
                alias="lon_min",
                ge=-180,
                le=180,
            ),
        ] = None,
        lat_min: Annotated[
            float | None,
            Query(
                ...,
                description="Rectangle. Min latitude",
                alias="lat_min",
                ge=-90,
                le=90,
            ),
        ] = None,
        lon_max: Annotated[
            float | None,
            Query(
                ...,
                description="Rectangle. Max longitude",
                alias="lon_max",
                ge=-180,
                le=180,
            ),
        ] = None,
        lat_max: Annotated[
            float | None,
            Query(
                ...,
                description="Rectangle. Max latitude",
                alias="lat_max",
                ge=-90,
                le=90,
            ),
        ] = None,
    ) -> None:
        """Location query params.

        :param lon_min: Min longitude
        :param lon_max: Max longitude
        :param lat_min: Min latitude
        :param lat_max: Max latitude
        :type lon_min: Annotated[float, float]
        :type lon_max: Annotated[float, float]
        :type lat_min: Annotated[float, float]
        :type lon_max: Annotated[float, float]
        ;:return None
        """
        self.lon_min = lon_min
        self.lat_min = lat_min
        self.lon_max = lon_max
        self.lat_max = lat_max

    def __bool__(self) -> bool:
        """Return True if the coordinates are valid.

        :return: True if the coordinates are valid.
        :rtype: bool
        """
        return all(
            isinstance(value, (float, int))
            for value in (
                self.lon_min,
                self.lat_min,
                self.lon_max,
                self.lat_max,
            )
        )

    def validate(self) -> Optional[LocationRectangleDTO]:
        """Validate the coordinates.

        :return: True if the coordinates are valid.
        :rtype: Optional[LocationRectangleDTO]
        """
        if (
            self.lon_max is None
            or self.lat_max is None
            or self.lon_min is None
            or self.lat_min is None
        ):
            return None

        return LocationRectangleDTO(
            lon_min=self.lon_min,
            lon_max=self.lon_max,
            lat_min=self.lat_min,
            lat_max=self.lat_max,
        )

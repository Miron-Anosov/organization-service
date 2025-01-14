"""Location's DTO models."""

from typing import Tuple

from pydantic import BaseModel


class LocationRectangleDTO(BaseModel):
    """Location's DTO models by rectangles."""

    lon_min: float
    lon_max: float
    lat_min: float
    lat_max: float

    def to_tuple(self) -> tuple[float, float, float, float]:
        """Serialize to tuple.

        :return: Longitude and Latitude
        :rtype: Tuple[float, float, float, float]
        """
        return self.lon_min, self.lon_max, self.lat_min, self.lat_max


class LocationRadiusDTO(BaseModel):
    """Location's DTO models by radius."""

    lon: float
    lat: float
    radius: float

    def to_tuple_location(self) -> Tuple[float, float]:
        """Serialize to tuple.

        :return: Longitude and Latitude
        :rtype: Tuple[float, float]
        """
        return self.lon, self.lat

    def to_float_radius(self) -> float:
        """Serialize to float.

        :return: Longitude and Latitude
        :rtype: float
        """
        return self.radius

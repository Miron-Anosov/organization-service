"""Util for extracting geographical coordinates from geographical data."""

from typing import Tuple

from geoalchemy2 import WKBElement, WKTElement
from geoalchemy2.shape import to_shape
from shapely.geometry.point import Point


def extract_coordinates(
    location: WKBElement | WKTElement,
) -> Tuple[float, float]:
    """Extract coordinates from a WKBElement or WKTElement."""
    shape: Point = to_shape(location)
    return shape.x, shape.y

"""Swagger docs."""

from typing import Any

from starlette import status

from src.core.api.v1.presentation.exceptions.core_error import DetailError


class ResponseError:
    """Typical Errors."""

    RESPONSES: dict[int | str, dict[str, Any]] = {
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden",
            "content": DetailError.CONTENT,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content": DetailError.CONTENT,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Invalid credentials",
            "content": DetailError.CONTENT,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation Error",
            "content": DetailError.CONTENT,
        },
    }

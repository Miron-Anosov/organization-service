"""Error 404 response util."""

from fastapi import HTTPException
from starlette import status

from src.core.api.v1.presentation.responses.error import ErrResponse


def error_404_not_found() -> HTTPException:
    """Return 404 Not Found.

    :return HTTPException: HTTP Not Found.
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ErrResponse(
            error_type="BadRequest",
            error_message="Organization not found.",
        ).model_dump(),
    )

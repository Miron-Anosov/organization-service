"""Static API key."""

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from src.core.api.v1.presentation.responses.error import ErrResponse
from src.core.configs.env import settings

API_KEY = settings.webconf.API_KEY
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(
    api_key_header_req: str = Security(api_key_header),
) -> None:
    """Check header of X-API-Key.

    :param api_key_header_req:
    :type api_key_header_req: str
    :return: None
    :rtype: type[None]
    :raises HTTPException: Could not validate API key
    """
    if api_key_header_req != API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=ErrResponse(
                error_type="AuthenticationError",
                error_message="X-API-Key header is incorrect.",
            ).model_dump(),
        )

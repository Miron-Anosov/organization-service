"""Common detail error codes."""

from typing import Any


class DetailError:
    """Default Error model to response."""

    CONTENT: dict[str, Any] = {
        "application/json": {
            "example": {
                "detail": {
                    "result": False,
                    "error_type": "String",
                    "error_message": "String",
                }
            }
        }
    }

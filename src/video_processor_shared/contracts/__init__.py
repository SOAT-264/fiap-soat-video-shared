"""API Contracts for inter-service communication."""

from video_processor_shared.contracts.api_responses import (
    ErrorResponse,
    PaginatedResponse,
    SuccessResponse,
)

__all__ = [
    "SuccessResponse",
    "ErrorResponse",
    "PaginatedResponse",
]

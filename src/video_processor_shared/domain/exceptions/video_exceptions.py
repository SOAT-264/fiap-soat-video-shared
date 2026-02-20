"""Video-related Domain Exceptions."""
from video_processor_shared.domain.exceptions.base import DomainError


class InvalidVideoFormatError(DomainError):
    """Raised when video format is not supported."""
    pass


class VideoTooLargeError(DomainError):
    """Raised when video exceeds maximum allowed size."""
    pass


class VideoNotFoundError(DomainError):
    """Raised when a video is not found."""
    pass

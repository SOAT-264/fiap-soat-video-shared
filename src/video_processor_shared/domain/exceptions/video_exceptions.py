"""Video-related Domain Exceptions."""
from video_processor_shared.domain.exceptions.base import DomainException


class InvalidVideoFormatError(DomainException):
    """Raised when video format is not supported."""
    pass


class VideoTooLargeError(DomainException):
    """Raised when video exceeds maximum allowed size."""
    pass


class VideoNotFoundError(DomainException):
    """Raised when a video is not found."""
    pass

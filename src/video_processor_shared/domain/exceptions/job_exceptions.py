"""Job-related Domain Exceptions."""
from video_processor_shared.domain.exceptions.base import DomainException


class InvalidJobTransitionError(DomainException):
    """Raised when attempting an invalid job status transition."""
    pass


class JobNotFoundError(DomainException):
    """Raised when a job is not found."""
    pass


class JobAlreadyCompletedError(DomainException):
    """Raised when trying to modify a completed job."""
    pass

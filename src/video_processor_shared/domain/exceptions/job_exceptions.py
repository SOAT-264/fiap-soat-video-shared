"""Job-related Domain Exceptions."""
from video_processor_shared.domain.exceptions.base import DomainError


class InvalidJobTransitionError(DomainError):
    """Raised when attempting an invalid job status transition."""
    pass


class JobNotFoundError(DomainError):
    """Raised when a job is not found."""
    pass


class JobAlreadyCompletedError(DomainError):
    """Raised when trying to modify a completed job."""
    pass

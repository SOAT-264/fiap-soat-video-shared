"""Domain layer shared components."""

from video_processor_shared.domain.value_objects import Email, Password, JobStatus
from video_processor_shared.domain.events import (
    DomainEvent,
    VideoUploadedEvent,
    JobStartedEvent,
    JobCompletedEvent,
    JobFailedEvent,
)
from video_processor_shared.domain.exceptions import (
    DomainException,
    InvalidEmailError,
    WeakPasswordError,
    InvalidJobTransitionError,
)

__all__ = [
    # Value Objects
    "Email",
    "Password",
    "JobStatus",
    # Events
    "DomainEvent",
    "VideoUploadedEvent",
    "JobStartedEvent",
    "JobCompletedEvent",
    "JobFailedEvent",
    # Exceptions
    "DomainException",
    "InvalidEmailError",
    "WeakPasswordError",
    "InvalidJobTransitionError",
]

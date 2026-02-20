"""Domain layer shared components."""

from video_processor_shared.domain.events import (
    DomainEvent,
    JobCompletedEvent,
    JobFailedEvent,
    JobStartedEvent,
    VideoUploadedEvent,
)
from video_processor_shared.domain.exceptions import (
    DomainError,
    InvalidEmailError,
    InvalidJobTransitionError,
    WeakPasswordError,
)
from video_processor_shared.domain.value_objects import Email, JobStatus, Password

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
    "DomainError",
    "InvalidEmailError",
    "WeakPasswordError",
    "InvalidJobTransitionError",
]

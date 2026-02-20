"""Domain Exceptions for the Video Processor."""

from video_processor_shared.domain.exceptions.base import DomainError
from video_processor_shared.domain.exceptions.job_exceptions import (
    InvalidJobTransitionError,
    JobAlreadyCompletedError,
    JobNotFoundError,
)
from video_processor_shared.domain.exceptions.user_exceptions import (
    InvalidCredentialsError,
    InvalidEmailError,
    UserAlreadyExistsError,
    UserInactiveError,
    UserNotFoundError,
    WeakPasswordError,
)
from video_processor_shared.domain.exceptions.video_exceptions import (
    InvalidVideoFormatError,
    VideoNotFoundError,
    VideoTooLargeError,
)

__all__ = [
    # Base
    "DomainError",
    # User
    "UserAlreadyExistsError",
    "InvalidCredentialsError",
    "UserNotFoundError",
    "UserInactiveError",
    "InvalidEmailError",
    "WeakPasswordError",
    # Job
    "InvalidJobTransitionError",
    "JobNotFoundError",
    "JobAlreadyCompletedError",
    # Video
    "InvalidVideoFormatError",
    "VideoTooLargeError",
    "VideoNotFoundError",
]

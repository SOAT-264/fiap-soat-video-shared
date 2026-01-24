"""Domain Exceptions for the Video Processor."""

from video_processor_shared.domain.exceptions.base import DomainException
from video_processor_shared.domain.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError,
    UserInactiveError,
    InvalidEmailError,
    WeakPasswordError,
)
from video_processor_shared.domain.exceptions.job_exceptions import (
    InvalidJobTransitionError,
    JobNotFoundError,
    JobAlreadyCompletedError,
)
from video_processor_shared.domain.exceptions.video_exceptions import (
    InvalidVideoFormatError,
    VideoTooLargeError,
    VideoNotFoundError,
)

__all__ = [
    # Base
    "DomainException",
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

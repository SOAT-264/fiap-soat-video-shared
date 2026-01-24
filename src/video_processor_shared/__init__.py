"""Video Processor Shared Library.

Shared components for FIAP SOAT Video Processor microservices.
Contains value objects, domain events, exceptions, and DTOs.
"""

from video_processor_shared.domain.value_objects.email import Email
from video_processor_shared.domain.value_objects.password import Password
from video_processor_shared.domain.value_objects.job_status import JobStatus
from video_processor_shared.domain.events.base_event import DomainEvent
from video_processor_shared.domain.events.video_uploaded import VideoUploadedEvent
from video_processor_shared.domain.events.job_started import JobStartedEvent
from video_processor_shared.domain.events.job_completed import JobCompletedEvent
from video_processor_shared.domain.events.job_failed import JobFailedEvent

__version__ = "0.1.0"

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
]

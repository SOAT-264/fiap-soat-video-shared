"""Domain Events for the Video Processor."""

from video_processor_shared.domain.events.base_event import DomainEvent
from video_processor_shared.domain.events.job_completed import JobCompletedEvent
from video_processor_shared.domain.events.job_failed import JobFailedEvent
from video_processor_shared.domain.events.job_started import JobStartedEvent
from video_processor_shared.domain.events.video_uploaded import VideoUploadedEvent

__all__ = [
    "DomainEvent",
    "VideoUploadedEvent",
    "JobStartedEvent",
    "JobCompletedEvent",
    "JobFailedEvent",
]

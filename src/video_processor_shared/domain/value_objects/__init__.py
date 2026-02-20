"""Value Objects for the Video Processor domain."""

from video_processor_shared.domain.value_objects.email import Email
from video_processor_shared.domain.value_objects.job_status import JobStatus
from video_processor_shared.domain.value_objects.password import Password

__all__ = ["Email", "Password", "JobStatus"]

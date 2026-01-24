"""Job Started Event."""
from dataclasses import dataclass
from uuid import UUID

from video_processor_shared.domain.events.base_event import DomainEvent


@dataclass(frozen=True)
class JobStartedEvent(DomainEvent):
    """
    Event raised when a job starts processing.

    Attributes:
        job_id: ID of the job.
        video_id: ID of the video being processed.
        user_id: ID of the video owner.
    """

    job_id: UUID = None  # type: ignore
    video_id: UUID = None  # type: ignore
    user_id: UUID = None  # type: ignore

    def to_dict(self) -> dict:
        """Convert event to dictionary for serialization."""
        data = super().to_dict()
        data.update({
            "job_id": str(self.job_id),
            "video_id": str(self.video_id),
            "user_id": str(self.user_id),
        })
        return data

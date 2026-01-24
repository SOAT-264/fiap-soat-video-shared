"""Job Completed Event."""
from dataclasses import dataclass
from uuid import UUID

from video_processor_shared.domain.events.base_event import DomainEvent


@dataclass(frozen=True)
class JobCompletedEvent(DomainEvent):
    """
    Event raised when a job completes successfully.

    Attributes:
        job_id: ID of the completed job.
        video_id: ID of the processed video.
        user_id: ID of the video owner.
        frame_count: Number of frames extracted.
        zip_path: Path to the output ZIP file.
    """

    job_id: UUID = None  # type: ignore
    video_id: UUID = None  # type: ignore
    user_id: UUID = None  # type: ignore
    frame_count: int = 0
    zip_path: str = ""

    def to_dict(self) -> dict:
        """Convert event to dictionary for serialization."""
        data = super().to_dict()
        data.update({
            "job_id": str(self.job_id),
            "video_id": str(self.video_id),
            "user_id": str(self.user_id),
            "frame_count": self.frame_count,
            "zip_path": self.zip_path,
        })
        return data

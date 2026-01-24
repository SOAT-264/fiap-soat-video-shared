"""Video Uploaded Event."""
from dataclasses import dataclass
from uuid import UUID

from video_processor_shared.domain.events.base_event import DomainEvent


@dataclass(frozen=True)
class VideoUploadedEvent(DomainEvent):
    """
    Event raised when a video is uploaded.

    Attributes:
        video_id: ID of the uploaded video.
        user_id: ID of the user who uploaded.
        filename: Original filename.
        file_size: Size in bytes.
    """

    video_id: UUID = None  # type: ignore
    user_id: UUID = None  # type: ignore
    filename: str = ""
    file_size: int = 0

    def to_dict(self) -> dict:
        """Convert event to dictionary for serialization."""
        data = super().to_dict()
        data.update({
            "video_id": str(self.video_id),
            "user_id": str(self.user_id),
            "filename": self.filename,
            "file_size": self.file_size,
        })
        return data

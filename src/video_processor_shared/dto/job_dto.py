"""Job Data Transfer Objects."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from video_processor_shared.domain.value_objects.job_status import JobStatus


class JobCreateDTO(BaseModel):
    """DTO for job creation request."""
    video_id: UUID
    user_id: UUID


class JobDTO(BaseModel):
    """DTO for job representation."""
    id: UUID
    video_id: UUID
    user_id: UUID
    status: JobStatus
    progress: int
    frame_count: Optional[int] = None
    zip_path: Optional[str] = None
    zip_size: Optional[int] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    @property
    def zip_size_mb(self) -> Optional[float]:
        """Get ZIP size in megabytes."""
        if self.zip_size is None:
            return None
        return self.zip_size / (1024 * 1024)

    @property
    def is_terminal(self) -> bool:
        """Check if job is in a terminal state."""
        return self.status.is_terminal

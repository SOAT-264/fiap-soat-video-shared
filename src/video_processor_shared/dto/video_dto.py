"""Video Data Transfer Objects."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator


class VideoUploadDTO(BaseModel):
    """DTO for video upload request."""
    filename: str
    content_type: str
    file_size: int

    @field_validator('filename')
    @classmethod
    def validate_filename(cls, v: str) -> str:
        allowed_extensions = ['mp4', 'avi', 'mov', 'mkv', 'webm']
        ext = v.rsplit('.', 1)[-1].lower() if '.' in v else ''
        if ext not in allowed_extensions:
            raise ValueError(f'File format not supported. Allowed: {", ".join(allowed_extensions)}')
        return v

    @field_validator('file_size')
    @classmethod
    def validate_file_size(cls, v: int) -> int:
        max_size = 500 * 1024 * 1024  # 500MB
        if v > max_size:
            raise ValueError(f'File size exceeds maximum allowed ({max_size // (1024*1024)}MB)')
        return v


class VideoDTO(BaseModel):
    """DTO for video representation."""
    id: UUID
    user_id: UUID
    original_filename: str
    file_path: str
    file_size: int
    format: str
    duration: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

    @property
    def file_size_mb(self) -> float:
        """Get file size in megabytes."""
        return self.file_size / (1024 * 1024)

"""Data Transfer Objects for inter-service communication."""

from video_processor_shared.dto.job_dto import JobCreateDTO, JobDTO
from video_processor_shared.dto.user_dto import UserCreateDTO, UserDTO
from video_processor_shared.dto.video_dto import VideoDTO, VideoUploadDTO

__all__ = [
    "UserDTO",
    "UserCreateDTO",
    "VideoDTO",
    "VideoUploadDTO",
    "JobDTO",
    "JobCreateDTO",
]

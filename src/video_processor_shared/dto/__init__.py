"""Data Transfer Objects for inter-service communication."""

from video_processor_shared.dto.user_dto import UserDTO, UserCreateDTO
from video_processor_shared.dto.video_dto import VideoDTO, VideoUploadDTO
from video_processor_shared.dto.job_dto import JobDTO, JobCreateDTO

__all__ = [
    "UserDTO",
    "UserCreateDTO",
    "VideoDTO",
    "VideoUploadDTO",
    "JobDTO",
    "JobCreateDTO",
]

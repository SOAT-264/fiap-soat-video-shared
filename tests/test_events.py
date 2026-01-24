"""Tests for Domain Events."""
from uuid import uuid4

from video_processor_shared.domain.events import (
    DomainEvent,
    VideoUploadedEvent,
    JobStartedEvent,
    JobCompletedEvent,
    JobFailedEvent,
)


class TestDomainEvent:
    """Tests for base DomainEvent."""

    def test_event_has_id(self):
        event = DomainEvent()
        assert event.event_id is not None

    def test_event_has_occurred_at(self):
        event = DomainEvent()
        assert event.occurred_at is not None

    def test_event_type(self):
        event = DomainEvent()
        assert event.event_type == "DomainEvent"

    def test_to_dict(self):
        event = DomainEvent()
        data = event.to_dict()
        assert "event_id" in data
        assert "event_type" in data
        assert "occurred_at" in data


class TestVideoUploadedEvent:
    """Tests for VideoUploadedEvent."""

    def test_video_uploaded_event(self):
        video_id = uuid4()
        user_id = uuid4()
        event = VideoUploadedEvent(
            video_id=video_id,
            user_id=user_id,
            filename="test.mp4",
            file_size=1024,
        )
        assert event.video_id == video_id
        assert event.user_id == user_id
        assert event.filename == "test.mp4"
        assert event.file_size == 1024

    def test_to_dict(self):
        event = VideoUploadedEvent(
            video_id=uuid4(),
            user_id=uuid4(),
            filename="test.mp4",
            file_size=1024,
        )
        data = event.to_dict()
        assert "video_id" in data
        assert "user_id" in data
        assert "filename" in data
        assert "file_size" in data


class TestJobEvents:
    """Tests for Job events."""

    def test_job_started_event(self):
        job_id = uuid4()
        video_id = uuid4()
        user_id = uuid4()
        event = JobStartedEvent(
            job_id=job_id,
            video_id=video_id,
            user_id=user_id,
        )
        assert event.job_id == job_id
        assert event.video_id == video_id
        assert event.event_type == "JobStartedEvent"

    def test_job_completed_event(self):
        event = JobCompletedEvent(
            job_id=uuid4(),
            video_id=uuid4(),
            user_id=uuid4(),
            frame_count=100,
            zip_path="/output/frames.zip",
        )
        assert event.frame_count == 100
        assert event.zip_path == "/output/frames.zip"

    def test_job_failed_event(self):
        event = JobFailedEvent(
            job_id=uuid4(),
            video_id=uuid4(),
            user_id=uuid4(),
            error_message="Processing failed",
        )
        assert event.error_message == "Processing failed"

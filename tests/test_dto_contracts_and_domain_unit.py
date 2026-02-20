"""Unit tests for DTOs, contracts and remaining domain branches."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from video_processor_shared.contracts import ErrorResponse, PaginatedResponse, SuccessResponse
from video_processor_shared.domain.events import JobCompletedEvent, JobFailedEvent, JobStartedEvent
from video_processor_shared.domain.exceptions.base import DomainException
from video_processor_shared.domain.value_objects import Email, JobStatus, Password
from video_processor_shared.dto import JobCreateDTO, JobDTO, UserCreateDTO, UserDTO, VideoDTO, VideoUploadDTO


def test_success_and_error_response_contracts():
    ok = SuccessResponse[int](data=10, message="done")
    assert ok.success is True
    assert ok.data == 10

    err = ErrorResponse(error="bad request", code="BAD_REQ")
    assert err.success is False
    assert err.error == "bad request"
    assert err.code == "BAD_REQ"


def test_paginated_response_create_and_zero_page_size():
    page = PaginatedResponse[int].create(items=[1, 2], total=5, page=1, page_size=2)
    assert page.total_pages == 3
    assert page.data == [1, 2]

    page_zero = PaginatedResponse[int].create(items=[], total=5, page=1, page_size=0)
    assert page_zero.total_pages == 0


def test_user_create_dto_validations_and_user_dto():
    valid = UserCreateDTO(email="user@test.com", password="ValidPass1", full_name="  Test User  ")
    assert valid.full_name == "Test User"

    with pytest.raises(ValueError):
        UserCreateDTO(email="user@test.com", password="short1A", full_name="Name")

    with pytest.raises(ValueError):
        UserCreateDTO(email="user@test.com", password="lowercase123", full_name="Name")

    with pytest.raises(ValueError):
        UserCreateDTO(email="user@test.com", password="UPPERCASE123", full_name="Name")

    with pytest.raises(ValueError):
        UserCreateDTO(email="user@test.com", password="NoDigitsHere", full_name="Name")

    with pytest.raises(ValueError):
        UserCreateDTO(email="user@test.com", password="ValidPass1", full_name=" ")

    user = UserDTO(
        id=uuid4(),
        email="user@test.com",
        full_name="User",
        is_active=True,
        created_at=datetime.now(UTC),
    )
    assert user.is_active is True


def test_video_upload_dto_validations_and_video_dto_property():
    upload = VideoUploadDTO(filename="video.mp4", content_type="video/mp4", file_size=10)
    assert upload.filename == "video.mp4"

    with pytest.raises(ValueError):
        VideoUploadDTO(filename="video.txt", content_type="text/plain", file_size=10)

    with pytest.raises(ValueError):
        VideoUploadDTO(filename="video.mp4", content_type="video/mp4", file_size=600 * 1024 * 1024)

    dto = VideoDTO(
        id=uuid4(),
        user_id=uuid4(),
        original_filename="video.mp4",
        file_path="videos/x/video.mp4",
        file_size=2 * 1024 * 1024,
        format="mp4",
        created_at=datetime.now(UTC),
    )
    assert dto.file_size_mb == 2.0


def test_job_dto_properties_and_job_create_dto():
    create = JobCreateDTO(video_id=uuid4(), user_id=uuid4())
    assert create.video_id is not None

    job = JobDTO(
        id=uuid4(),
        video_id=uuid4(),
        user_id=uuid4(),
        status=JobStatus.COMPLETED,
        progress=100,
        zip_size=3 * 1024 * 1024,
        created_at=datetime.now(UTC),
    )
    assert job.zip_size_mb == 3.0
    assert job.is_terminal is True

    no_zip = JobDTO(
        id=uuid4(),
        video_id=uuid4(),
        user_id=uuid4(),
        status=JobStatus.PROCESSING,
        progress=50,
        created_at=datetime.now(UTC),
    )
    assert no_zip.zip_size_mb is None
    assert no_zip.is_terminal is False


def test_domain_exception_and_additional_value_object_branches():
    exc = DomainException("domain error")
    assert str(exc) == "domain error"

    assert str(Email("test@example.com")) == "test@example.com"
    assert repr(Email("test@example.com")) == "Email('test@example.com')"
    assert (Email("test@example.com") == "test@example.com") is False

    with pytest.raises(Exception):
        Email(123)  # type: ignore[arg-type]

    with pytest.raises(Exception):
        Email("a" * 250 + "@e.com")

    created = Password.create("ValidPass1")
    assert repr(created) == "Password(***)"
    assert (created == "x") is False

    raw = Password("raw-hash")
    assert raw.salt == ""
    assert raw.value.endswith("$")


def test_job_event_to_dict_payloads():
    started = JobStartedEvent(job_id=uuid4(), video_id=uuid4(), user_id=uuid4()).to_dict()
    assert "job_id" in started and "video_id" in started and "user_id" in started

    completed = JobCompletedEvent(
        job_id=uuid4(),
        video_id=uuid4(),
        user_id=uuid4(),
        frame_count=42,
        zip_path="/tmp/out.zip",
    ).to_dict()
    assert completed["frame_count"] == 42
    assert completed["zip_path"] == "/tmp/out.zip"

    failed = JobFailedEvent(
        job_id=uuid4(),
        video_id=uuid4(),
        user_id=uuid4(),
        error_message="boom",
    ).to_dict()
    assert failed["error_message"] == "boom"

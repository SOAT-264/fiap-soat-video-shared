"""Integration-style tests for end-to-end shared workflow."""

import asyncio
from datetime import UTC, datetime
from io import BytesIO
from unittest.mock import Mock
from uuid import uuid4

from video_processor_shared.aws.s3_storage import S3StorageService
from video_processor_shared.aws.ses_service import SESService
from video_processor_shared.aws.sns_service import SNSService
from video_processor_shared.contracts import SuccessResponse
from video_processor_shared.domain.value_objects import JobStatus
from video_processor_shared.dto import JobDTO, VideoUploadDTO


def test_processing_completion_pipeline_integration(monkeypatch):
    s3_client = Mock()
    s3_client.generate_presigned_url.return_value = "https://download/url"
    ses_client = Mock()
    ses_client.send_email.return_value = {"MessageId": "ses-msg"}
    sns_client = Mock()
    sns_client.publish.return_value = {"MessageId": "sns-msg"}

    monkeypatch.setattr("video_processor_shared.aws.s3_storage.get_s3_client", lambda: s3_client)
    monkeypatch.setattr("video_processor_shared.aws.ses_service.get_ses_client", lambda: ses_client)
    monkeypatch.setattr("video_processor_shared.aws.sns_service.get_sns_client", lambda: sns_client)
    monkeypatch.setattr(
        "video_processor_shared.aws.sns_service.get_sns_topic_arn",
        lambda topic_name: f"arn:test:{topic_name}",
    )

    upload = VideoUploadDTO(filename="movie.mp4", content_type="video/mp4", file_size=12_000)
    assert upload.filename.endswith(".mp4")

    s3 = S3StorageService(input_bucket="uploads", output_bucket="outputs")
    ses = SESService(from_email="noreply@test.local")
    sns = SNSService(topic_name="job-events")

    uploaded_key = asyncio.run(s3.upload_video(BytesIO(b"video"), upload.filename, "user-1"))
    zip_key = asyncio.run(s3.upload_frames_zip("frames.zip", "job-1"))
    download_url = s3.get_download_url(zip_key)

    email_id = asyncio.run(
        ses.send_job_completed_email(
            to="user@test.local",
            video_filename=upload.filename,
            frame_count=120,
            download_url=download_url,
        )
    )
    notification_id = asyncio.run(
        sns.publish_job_completed(
            job_id="job-1",
            user_id="user-1",
            video_id="video-1",
            output_url=download_url,
            frame_count=120,
        )
    )

    job = JobDTO(
        id=uuid4(),
        video_id=uuid4(),
        user_id=uuid4(),
        status=JobStatus.COMPLETED,
        progress=100,
        frame_count=120,
        zip_path=zip_key,
        created_at=datetime.now(UTC),
    )
    response = SuccessResponse[JobDTO](data=job, message="completed")

    assert uploaded_key.startswith("videos/user-1/")
    assert zip_key == "frames/job-1/frames.zip"
    assert download_url == "https://download/url"
    assert email_id == "ses-msg"
    assert notification_id == "sns-msg"
    assert response.success is True
    assert response.data.is_terminal is True

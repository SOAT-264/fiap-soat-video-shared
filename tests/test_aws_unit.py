"""Unit tests for AWS helpers and services."""

import asyncio
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import Mock

from video_processor_shared.aws import (
    get_aws_client,
    get_aws_resource,
    get_s3_client,
    get_ses_client,
    get_sns_client,
    get_sqs_client,
    get_sns_topic_arn,
    get_sqs_queue_url,
)
from video_processor_shared.aws.s3_storage import S3StorageService
from video_processor_shared.aws.ses_service import SESService
from video_processor_shared.aws.sns_service import SNSService
from video_processor_shared.aws.sqs_service import SQSService


def test_get_aws_client_with_localstack_env(monkeypatch):
    captured = {}

    def fake_client(**kwargs):
        captured.update(kwargs)
        return "client"

    monkeypatch.setenv("AWS_ENDPOINT_URL", "http://localhost:4566")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "key")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "secret")
    monkeypatch.setattr("video_processor_shared.aws.boto3.client", fake_client)

    result = get_aws_client("s3", region_name="us-west-2")

    assert result == "client"
    assert captured["service_name"] == "s3"
    assert captured["region_name"] == "us-west-2"
    assert captured["endpoint_url"] == "http://localhost:4566"
    assert captured["aws_access_key_id"] == "key"
    assert captured["aws_secret_access_key"] == "secret"
    assert "config" in captured


def test_get_aws_client_without_endpoint(monkeypatch):
    captured = {}

    def fake_client(**kwargs):
        captured.update(kwargs)
        return "client"

    monkeypatch.delenv("AWS_ENDPOINT_URL", raising=False)
    monkeypatch.setattr("video_processor_shared.aws.boto3.client", fake_client)

    get_aws_client("sns")

    assert captured["service_name"] == "sns"
    assert "endpoint_url" not in captured
    assert "aws_access_key_id" not in captured


def test_get_aws_resource_with_and_without_endpoint(monkeypatch):
    first = {}
    second = {}

    def fake_resource(**kwargs):
        if not first:
            first.update(kwargs)
        else:
            second.update(kwargs)
        return SimpleNamespace(**kwargs)

    monkeypatch.setattr("video_processor_shared.aws.boto3.resource", fake_resource)
    monkeypatch.setenv("AWS_ENDPOINT_URL", "http://localhost:4566")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "abc")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "def")

    get_aws_resource("s3")
    monkeypatch.delenv("AWS_ENDPOINT_URL", raising=False)
    get_aws_resource("s3")

    assert first["endpoint_url"] == "http://localhost:4566"
    assert first["aws_access_key_id"] == "abc"
    assert "endpoint_url" not in second


def test_cached_clients_use_lru_cache(monkeypatch):
    calls = {"count": 0}

    def fake_get_aws_client(service_name):
        calls["count"] += 1
        return {"service": service_name, "idx": calls["count"]}

    monkeypatch.setattr("video_processor_shared.aws.get_aws_client", fake_get_aws_client)
    get_s3_client.cache_clear()
    get_sqs_client.cache_clear()
    get_sns_client.cache_clear()
    get_ses_client.cache_clear()

    first = get_s3_client()
    second = get_s3_client()
    assert first is second

    assert get_sqs_client()["service"] == "sqs"
    assert get_sns_client()["service"] == "sns"
    assert get_ses_client()["service"] == "ses"


def test_queue_url_and_topic_arn_helpers(monkeypatch):
    monkeypatch.setenv("AWS_ENDPOINT_URL", "http://localhost:4566")
    assert get_sqs_queue_url("my-queue") == "http://localhost:4566/000000000000/my-queue"

    monkeypatch.delenv("AWS_ENDPOINT_URL", raising=False)
    monkeypatch.setenv("AWS_ACCOUNT_ID", "123456789012")
    monkeypatch.setenv("AWS_REGION", "sa-east-1")
    assert get_sqs_queue_url("my-queue") == "https://sqs.sa-east-1.amazonaws.com/123456789012/my-queue"
    assert get_sns_topic_arn("job-events") == "arn:aws:sns:sa-east-1:123456789012:job-events"


def test_s3_storage_service_methods(monkeypatch):
    client = Mock()
    client.generate_presigned_url.return_value = "https://signed-url"
    monkeypatch.setattr("video_processor_shared.aws.s3_storage.get_s3_client", lambda: client)

    service = S3StorageService(input_bucket="in-bucket", output_bucket="out-bucket")

    key = asyncio.run(service.upload_video(BytesIO(b"abc"), "video.mp4", "user-1"))
    assert key.startswith("videos/user-1/")
    assert key.endswith("/video.mp4")

    asyncio.run(service.download_video("path/key", "dest.file"))
    client.download_file.assert_called_once_with("in-bucket", "path/key", "dest.file")

    zip_key = asyncio.run(service.upload_frames_zip("file.zip", "job-1"))
    assert zip_key == "frames/job-1/frames.zip"

    url = service.get_download_url("frames/job-1/frames.zip", expires_in=120)
    assert url == "https://signed-url"
    client.generate_presigned_url.assert_called_once()

    asyncio.run(service.delete_video("path/key"))
    client.delete_object.assert_called_once_with(Bucket="in-bucket", Key="path/key")


def test_ses_service_send_email_and_notifications(monkeypatch):
    client = Mock()
    client.send_email.return_value = {"MessageId": "msg-1"}
    monkeypatch.setattr("video_processor_shared.aws.ses_service.get_ses_client", lambda: client)

    service = SESService(from_email="noreply@test.local")
    message_id = asyncio.run(
        service.send_email(
            to="user@test.local",
            subject="Hello",
            body_text="Body",
            body_html="<b>Body</b>",
        )
    )
    assert message_id == "msg-1"
    sent_message = client.send_email.call_args.kwargs["Message"]
    assert "Html" in sent_message["Body"]

    client.send_email.reset_mock()
    asyncio.run(
        service.send_job_completed_email(
            to="user@test.local",
            video_filename="video.mp4",
            frame_count=12,
            download_url="https://download",
        )
    )
    completed = client.send_email.call_args.kwargs["Message"]
    assert "Video Processing Complete" in completed["Subject"]["Data"]

    client.send_email.reset_mock()
    asyncio.run(
        service.send_job_failed_email(
            to="user@test.local",
            video_filename="video.mp4",
            error_message="boom",
        )
    )
    failed = client.send_email.call_args.kwargs["Message"]
    assert "Video Processing Failed" in failed["Subject"]["Data"]


def test_sns_service_publish_and_specialized_events(monkeypatch):
    client = Mock()
    client.publish.return_value = {"MessageId": "sns-1"}
    monkeypatch.setattr("video_processor_shared.aws.sns_service.get_sns_client", lambda: client)
    monkeypatch.setattr(
        "video_processor_shared.aws.sns_service.get_sns_topic_arn",
        lambda name: f"arn:test:{name}",
    )

    service = SNSService(topic_name="events")
    assert asyncio.run(service.publish({"a": 1})) == "sns-1"
    first_args = client.publish.call_args.kwargs
    assert first_args["TopicArn"] == "arn:test:events"
    assert "Subject" not in first_args

    asyncio.run(service.publish_job_completed("j1", "u1", "v1", "url", 10))
    completed_args = client.publish.call_args.kwargs
    assert completed_args["Subject"] == "Video Processing Completed"

    asyncio.run(service.publish_job_failed("j1", "u1", "v1", "error"))
    failed_args = client.publish.call_args.kwargs
    assert failed_args["Subject"] == "Video Processing Failed"


def test_sqs_service_send_receive_delete_and_size(monkeypatch):
    client = Mock()
    client.send_message.return_value = {"MessageId": "sqs-1"}
    client.receive_message.return_value = {
        "Messages": [
            {
                "MessageId": "m1",
                "Body": '{"job_id":"j1"}',
                "ReceiptHandle": "rh-1",
            }
        ]
    }
    client.get_queue_attributes.return_value = {
        "Attributes": {"ApproximateNumberOfMessages": "7"}
    }
    monkeypatch.setattr("video_processor_shared.aws.sqs_service.get_sqs_client", lambda: client)
    monkeypatch.setattr(
        "video_processor_shared.aws.sqs_service.get_sqs_queue_url",
        lambda name: f"https://queue/{name}",
    )

    service = SQSService(queue_name="jobs")
    msg_id = asyncio.run(service.send_message({"job": "x"}, delay_seconds=5))
    assert msg_id == "sqs-1"

    messages = asyncio.run(service.receive_messages(max_messages=2, wait_time_seconds=1))
    assert messages == [{"message_id": "m1", "body": {"job_id": "j1"}, "receipt_handle": "rh-1"}]

    asyncio.run(service.delete_message("rh-1"))
    client.delete_message.assert_called_once_with(QueueUrl="https://queue/jobs", ReceiptHandle="rh-1")

    size = asyncio.run(service.get_queue_size())
    assert size == 7

"""AWS Client Factory for LocalStack and AWS.

This module provides a unified way to create boto3 clients that work with
both LocalStack (local development) and real AWS services (production).
"""
import os
from functools import lru_cache
from typing import Any, Optional

import boto3  # type: ignore[import-untyped]
from botocore.config import Config  # type: ignore[import-untyped]


def get_aws_client(
    service_name: str,
    region_name: str = "us-east-1",
    endpoint_url: Optional[str] = None,
) -> Any:
    """
    Get a boto3 client configured for LocalStack or AWS.

    Args:
        service_name: AWS service name (s3, sqs, sns, ses, etc.)
        region_name: AWS region (default: us-east-1)
        endpoint_url: Custom endpoint URL (for LocalStack)

    Returns:
        boto3 client instance

    Usage:
        # Auto-detects LocalStack if AWS_ENDPOINT_URL is set
        s3 = get_aws_client('s3')
        sqs = get_aws_client('sqs')

        # Explicit LocalStack endpoint
        s3 = get_aws_client('s3', endpoint_url='http://localhost:4566')
    """
    # Check for LocalStack endpoint in environment
    if endpoint_url is None:
        endpoint_url = os.getenv("AWS_ENDPOINT_URL")

    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        connect_timeout=5,
        read_timeout=60,
    )

    client_kwargs = {
        "service_name": service_name,
        "region_name": region_name,
        "config": config,
    }

    # If using LocalStack, configure endpoint and dummy credentials
    if endpoint_url:
        client_kwargs["endpoint_url"] = endpoint_url
        # LocalStack accepts any credentials
        client_kwargs["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID", "test")
        client_kwargs["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY", "test")

    return boto3.client(**client_kwargs)


def get_aws_resource(
    service_name: str,
    region_name: str = "us-east-1",
    endpoint_url: Optional[str] = None,
) -> Any:
    """
    Get a boto3 resource configured for LocalStack or AWS.

    Similar to get_aws_client but returns a resource object for
    higher-level abstractions.
    """
    if endpoint_url is None:
        endpoint_url = os.getenv("AWS_ENDPOINT_URL")

    resource_kwargs = {
        "service_name": service_name,
        "region_name": region_name,
    }

    if endpoint_url:
        resource_kwargs["endpoint_url"] = endpoint_url
        resource_kwargs["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID", "test")
        resource_kwargs["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY", "test")

    return boto3.resource(**resource_kwargs)


# Cached client getters for common services
@lru_cache()
def get_s3_client() -> Any:
    """Get cached S3 client."""
    return get_aws_client("s3")


@lru_cache()
def get_sqs_client() -> Any:
    """Get cached SQS client."""
    return get_aws_client("sqs")


@lru_cache()
def get_sns_client() -> Any:
    """Get cached SNS client."""
    return get_aws_client("sns")


@lru_cache()
def get_ses_client() -> Any:
    """Get cached SES client."""
    return get_aws_client("ses")


# Queue and topic URL helpers
def get_sqs_queue_url(queue_name: str) -> str:
    """Get SQS queue URL by name."""
    endpoint = os.getenv("AWS_ENDPOINT_URL", "")
    account_id = os.getenv("AWS_ACCOUNT_ID", "000000000000")
    region = os.getenv("AWS_REGION", "us-east-1")

    if endpoint:  # LocalStack
        return f"{endpoint}/000000000000/{queue_name}"
    else:  # Real AWS
        return f"https://sqs.{region}.amazonaws.com/{account_id}/{queue_name}"


def get_sns_topic_arn(topic_name: str) -> str:
    """Get SNS topic ARN by name."""
    account_id = os.getenv("AWS_ACCOUNT_ID", "000000000000")
    region = os.getenv("AWS_REGION", "us-east-1")

    return f"arn:aws:sns:{region}:{account_id}:{topic_name}"

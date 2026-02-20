"""SQS Queue Service using boto3.

Works with both LocalStack and real AWS SQS.
"""
import json
import os
from typing import Any, Dict, List, Optional

from video_processor_shared.aws import get_sqs_client, get_sqs_queue_url


class SQSService:
    """SQS message queue service."""

    def __init__(self, queue_name: Optional[str] = None) -> None:
        self.client = get_sqs_client()
        self.queue_name: str = queue_name or os.getenv("SQS_QUEUE_NAME") or "job-queue"
        self.queue_url = get_sqs_queue_url(self.queue_name)

    async def send_message(
        self,
        message: Dict[str, Any],
        delay_seconds: int = 0,
    ) -> str:
        """
        Send a message to the queue.

        Args:
            message: Dictionary to send as JSON
            delay_seconds: Delay before message becomes visible (0-900)

        Returns:
            Message ID
        """
        response = self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(message),
            DelaySeconds=delay_seconds,
        )
        return str(response["MessageId"])

    async def receive_messages(
        self,
        max_messages: int = 1,
        wait_time_seconds: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Receive messages from the queue.

        Args:
            max_messages: Maximum number of messages to receive (1-10)
            wait_time_seconds: Long polling wait time (0-20)

        Returns:
            List of messages with body and receipt_handle
        """
        response = self.client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time_seconds,
            AttributeNames=["All"],
            MessageAttributeNames=["All"],
        )

        messages = []
        for msg in response.get("Messages", []):
            messages.append({
                "message_id": msg["MessageId"],
                "body": json.loads(msg["Body"]),
                "receipt_handle": msg["ReceiptHandle"],
            })

        return messages

    async def delete_message(self, receipt_handle: str) -> None:
        """Delete a message from the queue after processing."""
        self.client.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle,
        )

    async def get_queue_size(self) -> int:
        """Get approximate number of messages in queue."""
        response = self.client.get_queue_attributes(
            QueueUrl=self.queue_url,
            AttributeNames=["ApproximateNumberOfMessages"],
        )
        return int(response["Attributes"]["ApproximateNumberOfMessages"])

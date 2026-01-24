"""SNS Notification Service using boto3.

Works with both LocalStack and real AWS SNS.
"""
import json
import os
from typing import Any, Dict, Optional

from video_processor_shared.aws import get_sns_client, get_sns_topic_arn


class SNSService:
    """SNS notification service for publishing events."""
    
    def __init__(self, topic_name: Optional[str] = None):
        self.client = get_sns_client()
        self.topic_name = topic_name or os.getenv("SNS_TOPIC_NAME", "job-events")
        self.topic_arn = get_sns_topic_arn(self.topic_name)
    
    async def publish(
        self,
        message: Dict[str, Any],
        subject: Optional[str] = None,
    ) -> str:
        """
        Publish a message to the SNS topic.
        
        Args:
            message: Dictionary to send as JSON
            subject: Optional email subject (for email subscribers)
        
        Returns:
            Message ID
        """
        publish_args = {
            "TopicArn": self.topic_arn,
            "Message": json.dumps(message),
        }
        
        if subject:
            publish_args["Subject"] = subject
        
        response = self.client.publish(**publish_args)
        return response["MessageId"]
    
    async def publish_job_completed(
        self,
        job_id: str,
        user_id: str,
        video_id: str,
        output_url: str,
        frame_count: int,
    ) -> str:
        """Publish a job completed event."""
        return await self.publish(
            message={
                "event_type": "job_completed",
                "job_id": job_id,
                "user_id": user_id,
                "video_id": video_id,
                "output_url": output_url,
                "frame_count": frame_count,
            },
            subject="Video Processing Completed",
        )
    
    async def publish_job_failed(
        self,
        job_id: str,
        user_id: str,
        video_id: str,
        error_message: str,
    ) -> str:
        """Publish a job failed event."""
        return await self.publish(
            message={
                "event_type": "job_failed",
                "job_id": job_id,
                "user_id": user_id,
                "video_id": video_id,
                "error_message": error_message,
            },
            subject="Video Processing Failed",
        )

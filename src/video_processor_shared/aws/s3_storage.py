"""S3 Storage Service using boto3.

Works with both LocalStack and real AWS S3.
"""
import os
from typing import BinaryIO, Optional
from uuid import uuid4

from video_processor_shared.aws import get_s3_client


class S3StorageService:
    """S3-compatible storage service."""
    
    def __init__(
        self,
        input_bucket: Optional[str] = None,
        output_bucket: Optional[str] = None,
    ):
        self.client = get_s3_client()
        self.input_bucket = input_bucket or os.getenv("S3_INPUT_BUCKET", "video-uploads")
        self.output_bucket = output_bucket or os.getenv("S3_OUTPUT_BUCKET", "video-outputs")
    
    async def upload_video(
        self,
        file: BinaryIO,
        filename: str,
        user_id: str,
    ) -> str:
        """
        Upload a video file to S3.
        
        Returns the S3 key of the uploaded file.
        """
        key = f"videos/{user_id}/{uuid4()}/{filename}"
        
        self.client.upload_fileobj(
            file,
            self.input_bucket,
            key,
            ExtraArgs={"ContentType": "video/mp4"},
        )
        
        return key
    
    async def download_video(self, key: str, destination: str) -> None:
        """Download a video from S3 to local path."""
        self.client.download_file(self.input_bucket, key, destination)
    
    async def upload_frames_zip(
        self,
        file_path: str,
        job_id: str,
    ) -> str:
        """
        Upload processed frames ZIP to output bucket.
        
        Returns the S3 key of the uploaded file.
        """
        key = f"frames/{job_id}/frames.zip"
        
        self.client.upload_file(
            file_path,
            self.output_bucket,
            key,
            ExtraArgs={"ContentType": "application/zip"},
        )
        
        return key
    
    def get_download_url(self, key: str, expires_in: int = 3600) -> str:
        """
        Generate a presigned URL for downloading a file.
        
        Args:
            key: S3 object key
            expires_in: URL expiration time in seconds (default: 1 hour)
        
        Returns:
            Presigned URL string
        """
        url = self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.output_bucket, "Key": key},
            ExpiresIn=expires_in,
        )
        return url
    
    async def delete_video(self, key: str) -> None:
        """Delete a video from S3."""
        self.client.delete_object(Bucket=self.input_bucket, Key=key)

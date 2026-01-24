"""SES Email Service using boto3.

Works with both LocalStack and real AWS SES.
"""
import os
from typing import List, Optional

from video_processor_shared.aws import get_ses_client


class SESService:
    """SES email sending service."""
    
    def __init__(self, from_email: Optional[str] = None):
        self.client = get_ses_client()
        self.from_email = from_email or os.getenv(
            "SES_FROM_EMAIL", "noreply@videoprocessor.local"
        )
    
    async def send_email(
        self,
        to: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
    ) -> str:
        """
        Send an email via SES.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body_text: Plain text body
            body_html: Optional HTML body
        
        Returns:
            Message ID
        """
        message_body = {"Text": {"Data": body_text, "Charset": "UTF-8"}}
        
        if body_html:
            message_body["Html"] = {"Data": body_html, "Charset": "UTF-8"}
        
        response = self.client.send_email(
            Source=self.from_email,
            Destination={"ToAddresses": [to]},
            Message={
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": message_body,
            },
        )
        
        return response["MessageId"]
    
    async def send_job_completed_email(
        self,
        to: str,
        video_filename: str,
        frame_count: int,
        download_url: str,
    ) -> str:
        """Send a job completed notification email."""
        subject = f"✅ Video Processing Complete: {video_filename}"
        
        body_text = f"""
Hello!

Your video "{video_filename}" has been processed successfully!

📊 Processing Results:
- Frames extracted: {frame_count}
- Status: COMPLETED

📥 Download your frames:
{download_url}

Thank you for using Video Processor!

Best regards,
Video Processor Team
        """.strip()
        
        body_html = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <h2 style="color: #22c55e;">✅ Video Processing Complete</h2>
    <p>Your video <strong>"{video_filename}"</strong> has been processed successfully!</p>
    
    <div style="background: #f3f4f6; padding: 16px; border-radius: 8px; margin: 16px 0;">
        <h3 style="margin-top: 0;">📊 Processing Results</h3>
        <ul>
            <li>Frames extracted: <strong>{frame_count}</strong></li>
            <li>Status: <strong style="color: #22c55e;">COMPLETED</strong></li>
        </ul>
    </div>
    
    <a href="{download_url}" style="display: inline-block; background: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 16px 0;">
        📥 Download Frames
    </a>
    
    <p style="color: #6b7280; font-size: 14px; margin-top: 32px;">
        Thank you for using Video Processor!<br>
        Best regards,<br>
        <strong>Video Processor Team</strong>
    </p>
</body>
</html>
        """.strip()
        
        return await self.send_email(to, subject, body_text, body_html)
    
    async def send_job_failed_email(
        self,
        to: str,
        video_filename: str,
        error_message: str,
    ) -> str:
        """Send a job failed notification email."""
        subject = f"❌ Video Processing Failed: {video_filename}"
        
        body_text = f"""
Hello!

Unfortunately, we encountered an error processing your video "{video_filename}".

❌ Error Details:
{error_message}

Please try uploading your video again. If the problem persists,
please contact our support team.

We apologize for the inconvenience.

Best regards,
Video Processor Team
        """.strip()
        
        return await self.send_email(to, subject, body_text)

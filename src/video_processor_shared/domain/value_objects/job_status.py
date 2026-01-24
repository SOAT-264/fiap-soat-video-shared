"""Job Status Value Object."""
from enum import Enum
from typing import List


class JobStatus(str, Enum):
    """
    Enumeration of possible job statuses.

    Inherits from str to allow JSON serialization.
    """

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

    def can_transition_to(self, new_status: "JobStatus") -> bool:
        """
        Check if transition to new status is valid.

        Valid transitions:
        - PENDING -> PROCESSING, CANCELLED, FAILED
        - PROCESSING -> COMPLETED, FAILED, CANCELLED
        - COMPLETED -> (none)
        - FAILED -> (none)
        - CANCELLED -> (none)

        Args:
            new_status: The target status.

        Returns:
            bool: True if transition is valid.
        """
        valid_transitions: dict[JobStatus, List[JobStatus]] = {
            JobStatus.PENDING: [JobStatus.PROCESSING, JobStatus.CANCELLED, JobStatus.FAILED],
            JobStatus.PROCESSING: [
                JobStatus.COMPLETED,
                JobStatus.FAILED,
                JobStatus.CANCELLED
            ],
            JobStatus.COMPLETED: [],
            JobStatus.FAILED: [],
            JobStatus.CANCELLED: [],
        }
        return new_status in valid_transitions.get(self, [])

    @property
    def is_terminal(self) -> bool:
        """Check if this is a terminal (final) status."""
        return self in (
            JobStatus.COMPLETED,
            JobStatus.FAILED,
            JobStatus.CANCELLED
        )

    @property
    def is_active(self) -> bool:
        """Check if job is actively being processed."""
        return self == JobStatus.PROCESSING

    @property
    def is_pending(self) -> bool:
        """Check if job is waiting to be processed."""
        return self == JobStatus.PENDING

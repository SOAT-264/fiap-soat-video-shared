"""Tests for Value Objects."""
import pytest

from video_processor_shared.domain.value_objects import Email, Password, JobStatus
from video_processor_shared.domain.exceptions import InvalidEmailError, WeakPasswordError


class TestEmail:
    """Tests for Email value object."""

    def test_valid_email(self):
        email = Email("test@example.com")
        assert email.value == "test@example.com"

    def test_email_normalized_lowercase(self):
        email = Email("TEST@EXAMPLE.COM")
        assert email.value == "test@example.com"

    def test_email_stripped(self):
        email = Email("  test@example.com  ")
        assert email.value == "test@example.com"

    def test_invalid_email_format(self):
        with pytest.raises(InvalidEmailError):
            Email("invalid-email")

    def test_empty_email(self):
        with pytest.raises(InvalidEmailError):
            Email("")

    def test_email_equality(self):
        email1 = Email("test@example.com")
        email2 = Email("TEST@example.com")
        assert email1 == email2

    def test_email_hash(self):
        email = Email("test@example.com")
        assert hash(email) == hash("test@example.com")


class TestPassword:
    """Tests for Password value object."""

    def test_create_valid_password(self):
        password = Password.create("ValidPass1")
        assert password.hashed_value is not None
        assert password.salt is not None

    def test_password_verification(self):
        password = Password.create("ValidPass1")
        assert password.verify("ValidPass1") is True
        assert password.verify("WrongPass1") is False

    def test_weak_password_too_short(self):
        with pytest.raises(WeakPasswordError):
            Password.create("Short1")

    def test_weak_password_no_uppercase(self):
        with pytest.raises(WeakPasswordError):
            Password.create("lowercase123")

    def test_weak_password_no_lowercase(self):
        with pytest.raises(WeakPasswordError):
            Password.create("UPPERCASE123")

    def test_weak_password_no_digit(self):
        with pytest.raises(WeakPasswordError):
            Password.create("NoDigitsHere")

    def test_password_from_hash(self):
        original = Password.create("ValidPass1")
        restored = Password.from_hash(original.hashed_value, original.salt)
        assert restored.verify("ValidPass1") is True


class TestJobStatus:
    """Tests for JobStatus value object."""

    def test_pending_can_transition_to_processing(self):
        assert JobStatus.PENDING.can_transition_to(JobStatus.PROCESSING) is True

    def test_pending_can_transition_to_cancelled(self):
        assert JobStatus.PENDING.can_transition_to(JobStatus.CANCELLED) is True

    def test_pending_cannot_transition_to_completed(self):
        assert JobStatus.PENDING.can_transition_to(JobStatus.COMPLETED) is False

    def test_processing_can_transition_to_completed(self):
        assert JobStatus.PROCESSING.can_transition_to(JobStatus.COMPLETED) is True

    def test_processing_can_transition_to_failed(self):
        assert JobStatus.PROCESSING.can_transition_to(JobStatus.FAILED) is True

    def test_completed_cannot_transition(self):
        assert JobStatus.COMPLETED.can_transition_to(JobStatus.PENDING) is False
        assert JobStatus.COMPLETED.can_transition_to(JobStatus.PROCESSING) is False

    def test_is_terminal(self):
        assert JobStatus.COMPLETED.is_terminal is True
        assert JobStatus.FAILED.is_terminal is True
        assert JobStatus.CANCELLED.is_terminal is True
        assert JobStatus.PENDING.is_terminal is False
        assert JobStatus.PROCESSING.is_terminal is False

    def test_is_active(self):
        assert JobStatus.PROCESSING.is_active is True
        assert JobStatus.PENDING.is_active is False

    def test_is_pending(self):
        assert JobStatus.PENDING.is_pending is True
        assert JobStatus.PROCESSING.is_pending is False

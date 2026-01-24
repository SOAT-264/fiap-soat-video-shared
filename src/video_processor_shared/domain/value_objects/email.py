"""Email Value Object."""
import re
from typing import Any

from video_processor_shared.domain.exceptions import InvalidEmailError


class Email:
    """
    Value Object for Email - Immutable.

    Validates and normalizes email addresses.
    """

    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    MAX_LENGTH = 255

    def __init__(self, value: str):
        """
        Create an Email value object.

        Args:
            value: The email address string.

        Raises:
            InvalidEmailError: If the email format is invalid.
        """
        self._value = self._validate(value)

    def _validate(self, value: str) -> str:
        """Validate and normalize email."""
        if not isinstance(value, str):
            raise InvalidEmailError("Email must be a string")

        value = value.strip().lower()

        if not value:
            raise InvalidEmailError("Email cannot be empty")

        if len(value) > self.MAX_LENGTH:
            raise InvalidEmailError(
                f"Email too long (max {self.MAX_LENGTH} characters)"
            )

        if not re.match(self.EMAIL_REGEX, value):
            raise InvalidEmailError(f"Invalid email format: {value}")

        return value

    @property
    def value(self) -> str:
        """Get the email value."""
        return self._value

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"Email('{self._value}')"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Email):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

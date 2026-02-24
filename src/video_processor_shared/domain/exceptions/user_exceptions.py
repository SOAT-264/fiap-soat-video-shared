"""User-related Domain Exceptions."""
from video_processor_shared.domain.exceptions.base import DomainError


class UserAlreadyExistsError(DomainError):
    """Raised when attempting to create a user that already exists."""
    pass


class InvalidCredentialsError(DomainError):
    """Raised when login credentials are invalid."""
    pass


class UserNotFoundError(DomainError):
    """Raised when a user is not found."""
    pass


class UserInactiveError(DomainError):
    """Raised when an inactive user tries to perform an action."""
    pass


class InvalidEmailError(DomainError):
    """Raised when email format is invalid."""
    pass


class WeakPasswordError(DomainError):
    """Raised when password does not meet strength requirements."""
    pass

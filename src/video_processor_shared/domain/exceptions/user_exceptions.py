"""User-related Domain Exceptions."""
from video_processor_shared.domain.exceptions.base import DomainException


class UserAlreadyExistsError(DomainException):
    """Raised when attempting to create a user that already exists."""
    pass


class InvalidCredentialsError(DomainException):
    """Raised when login credentials are invalid."""
    pass


class UserNotFoundError(DomainException):
    """Raised when a user is not found."""
    pass


class UserInactiveError(DomainException):
    """Raised when an inactive user tries to perform an action."""
    pass


class InvalidEmailError(DomainException):
    """Raised when email format is invalid."""
    pass


class WeakPasswordError(DomainException):
    """Raised when password does not meet strength requirements."""
    pass

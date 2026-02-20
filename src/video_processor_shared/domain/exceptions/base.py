"""Base Domain Exception."""


class DomainError(Exception):
    """
    Base exception for all domain-related errors.

    All domain exceptions should inherit from this class.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message

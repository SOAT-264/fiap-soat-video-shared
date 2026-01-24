"""Password Value Object."""
import hashlib
import secrets
from typing import Any

from video_processor_shared.domain.exceptions import WeakPasswordError


class Password:
    """
    Value Object for Password - Immutable.

    Handles password hashing and verification using PBKDF2.
    Note: In production, consider using bcrypt via passlib in the infrastructure layer.
    This implementation uses only Python stdlib for domain purity.
    """

    MIN_LENGTH = 8
    ITERATIONS = 100000
    HASH_NAME = 'sha256'
    SEPARATOR = '$'

    def __init__(self, value: str):
        """
        Create a Password value object from stored value.

        The value should be in format: hash$salt
        Use Password.create() to create a new password from plain text.

        Args:
            value: The stored password value (hash$salt format).
        """
        if self.SEPARATOR in value:
            parts = value.split(self.SEPARATOR)
            self._hashed_value = parts[0]
            self._salt = parts[1] if len(parts) > 1 else ''
        else:
            self._hashed_value = value
            self._salt = ''

    @classmethod
    def create(cls, plain_password: str) -> "Password":
        """
        Create a new Password from plain text.

        Args:
            plain_password: The plain text password.

        Returns:
            Password: A new Password instance with hashed value.

        Raises:
            WeakPasswordError: If password doesn't meet strength requirements.
        """
        cls._validate_strength(plain_password)

        salt = secrets.token_hex(32)
        hashed = cls._hash_password(plain_password, salt)

        return cls(f"{hashed}{cls.SEPARATOR}{salt}")

    @classmethod
    def from_hash(cls, hashed_value: str, salt: str) -> "Password":
        """
        Create a Password from existing hash and salt.

        Used when loading from database.

        Args:
            hashed_value: The stored hash.
            salt: The stored salt.

        Returns:
            Password: A Password instance.
        """
        return cls(f"{hashed_value}{cls.SEPARATOR}{salt}")

    @classmethod
    def _validate_strength(cls, password: str) -> None:
        """
        Validate password strength.

        Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit

        Raises:
            WeakPasswordError: If password is weak.
        """
        if len(password) < cls.MIN_LENGTH:
            raise WeakPasswordError(
                f"Password must be at least {cls.MIN_LENGTH} characters"
            )

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)

        if not (has_upper and has_lower and has_digit):
            raise WeakPasswordError(
                "Password must contain uppercase, lowercase, and numbers"
            )

    @classmethod
    def _hash_password(cls, password: str, salt: str) -> str:
        """Hash password using PBKDF2."""
        return hashlib.pbkdf2_hmac(
            cls.HASH_NAME,
            password.encode('utf-8'),
            salt.encode('utf-8'),
            cls.ITERATIONS
        ).hex()

    def verify(self, plain_password: str) -> bool:
        """
        Verify if plain password matches the hash.

        Args:
            plain_password: The plain text password to verify.

        Returns:
            bool: True if password matches, False otherwise.
        """
        hashed = self._hash_password(plain_password, self._salt)
        return secrets.compare_digest(self._hashed_value, hashed)

    @property
    def value(self) -> str:
        """Get the stored value (hash$salt format)."""
        return f"{self._hashed_value}{self.SEPARATOR}{self._salt}"

    @property
    def hashed_value(self) -> str:
        """Get the hashed password value."""
        return self._hashed_value

    @property
    def salt(self) -> str:
        """Get the salt."""
        return self._salt

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Password):
            return False
        return (
            self._hashed_value == other._hashed_value
            and self._salt == other._salt
        )

    def __hash__(self) -> int:
        return hash((self._hashed_value, self._salt))

    def __repr__(self) -> str:
        return "Password(***)"

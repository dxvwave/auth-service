"""Custom exceptions for the auth service."""


class AuthServiceException(Exception):
    """Base exception for auth service."""

    pass


class UserAlreadyExistsError(AuthServiceException):
    """Raised when trying to create a user that already exists."""

    pass


class UserNotFoundError(AuthServiceException):
    """Raised when a user is not found."""

    pass


class InvalidCredentialsError(AuthServiceException):
    """Raised when credentials are invalid."""

    pass


class InvalidTokenError(AuthServiceException):
    """Raised when a token is invalid."""

    pass


class TokenExpiredError(InvalidTokenError):
    """Raised when a token has expired."""

    pass


class InvalidTokenTypeError(InvalidTokenError):
    """Raised when token type doesn't match expected type."""

    def __init__(self, expected: str, actual: str | None):
        self.expected = expected
        self.actual = actual
        super().__init__(f"Expected {expected} token, got {actual}")

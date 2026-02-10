import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Literal

import jwt

from core.config import settings
from core.exceptions import TokenExpiredError, InvalidTokenError, InvalidTokenTypeError

logger = logging.getLogger(__name__)

TokenType = Literal["access", "refresh"]


class TokenService:
    """Service for creating and validating JWT tokens."""

    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_expire_minutes: int,
        refresh_token_expire_days: int,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def _create_token(
        self,
        payload: dict,
        token_type: TokenType,
        expires_delta: timedelta | None = None,
    ) -> str:
        """Create a JWT token with the given payload and type."""
        to_encode = payload.copy()

        if expires_delta is None:
            expires_delta = (
                timedelta(minutes=self.access_token_expire_minutes)
                if token_type == "access"
                else timedelta(days=self.refresh_token_expire_days)
            )

        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update(
            {
                "exp": expire,
                "iat": datetime.now(timezone.utc),
                "jti": str(uuid.uuid4()),
                "type": token_type,
            }
        )

        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_access_token(
        self,
        payload: dict,
        expires_delta: timedelta | None = None,
    ) -> str:
        """Create an access token."""
        return self._create_token(payload, "access", expires_delta)

    def create_refresh_token(
        self,
        payload: dict,
        expires_delta: timedelta | None = None,
    ) -> str:
        """Create a refresh token."""
        return self._create_token(payload, "refresh", expires_delta)

    def decode_token(
        self,
        token: str,
        expected_type: TokenType | None = None,
    ) -> dict:
        """
        Decode and validate a JWT token.

        Args:
            token: The JWT token to decode
            expected_type: Optional token type to validate against

        Returns:
            The decoded token payload

        Raises:
            TokenExpiredError: If the token has expired
            InvalidTokenTypeError: If the token type doesn't match expected_type
            InvalidTokenError: If the token is invalid
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            # Validate token type if specified
            if expected_type:
                actual_type = payload.get("type")
                if actual_type != expected_type:
                    logger.warning(
                        f"Token type mismatch: expected {expected_type}, got {actual_type}"
                    )
                    raise InvalidTokenTypeError(expected_type, actual_type)

            return payload

        except jwt.ExpiredSignatureError as e:
            logger.debug(f"Token expired: {str(e)}")
            raise TokenExpiredError("Token has expired") from e
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            raise InvalidTokenError("Invalid token") from e

    def create_token_pair(self, payload: dict) -> tuple[str, str]:
        """Create both access and refresh tokens."""
        access_token = self.create_access_token(payload)
        refresh_token = self.create_refresh_token(payload)
        return access_token, refresh_token


token_service = TokenService(
    secret_key=settings.jwt_secret_key,
    algorithm=settings.jwt_algorithm,
    access_token_expire_minutes=settings.jwt_access_token_expire_minutes,
    refresh_token_expire_days=settings.jwt_refresh_token_expire_days,
)

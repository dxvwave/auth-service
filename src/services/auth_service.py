import logging
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from core.schemas.user import UserCreate, TokenResponse
from core.security import verify_password
from core.exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
)
from services.user_service import user_service, UserService
from services.token_service import token_service, TokenService

logger = logging.getLogger(__name__)


class AuthService:
    """Service for authentication operations."""

    def __init__(
        self,
        user_service: UserService,
        token_service: TokenService,
    ):
        self.user_service = user_service
        self.token_service = token_service

    def _create_user_payload(self, user: User) -> dict:
        """Create a standardized token payload from a user."""
        return {
            "sub": str(user.id),
            "email": user.email,
        }

    async def register_user(
        self,
        user_data: UserCreate,
        session: AsyncSession,
    ) -> User:
        """
        Register a new user.

        Args:
            user_data: User registration data
            session: Database session

        Returns:
            Created user object

        Raises:
            UserAlreadyExistsError: If user already exists
        """
        return await self.user_service.create_user(session, user_data)

    async def authenticate_user(
        self,
        email: str,
        password: str,
        session: AsyncSession,
    ) -> TokenResponse:
        """
        Authenticate a user and return tokens.

        Args:
            email: User email
            password: Plain text password
            session: Database session

        Returns:
            Token response with access and refresh tokens

        Raises:
            InvalidCredentialsError: If credentials are invalid
        """
        user = await self.user_service.get_user_by_email(session, email)

        if not user or not verify_password(password, user.hashed_password):
            logger.warning(f"Failed authentication attempt for email: {email}")
            raise InvalidCredentialsError("Invalid email or password")

        if not user.is_active:
            logger.warning(f"Inactive user attempted login: {email}")
            raise InvalidCredentialsError("User account is inactive")

        payload = self._create_user_payload(user)
        access_token, refresh_token = self.token_service.create_token_pair(payload)

        logger.info(f"User authenticated successfully: {email}")

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh_access_token(
        self,
        refresh_token: str,
        session: AsyncSession,
    ) -> TokenResponse:
        """
        Refresh an access token using a refresh token.

        Args:
            refresh_token: Refresh token
            session: Database session

        Returns:
            Token response with new access token

        Raises:
            InvalidTokenError: If refresh token is invalid
            UserNotFoundError: If user is not found
        """
        # Decode and validate the refresh token (checks type automatically)
        payload = self.token_service.decode_token(
            refresh_token, expected_type="refresh"
        )

        user_id = payload.get("sub")
        if not user_id:
            logger.warning("Refresh token missing 'sub' claim")
            raise InvalidTokenError("Invalid refresh token")

        # Get user and verify they exist and are active
        user = await self.user_service.get_user_by_id(session, int(user_id))

        if not user.is_active:
            logger.warning(f"Inactive user attempted token refresh: {user.email}")
            raise InvalidCredentialsError("User account is inactive")

        # Create new access token
        payload = self._create_user_payload(user)
        access_token = self.token_service.create_access_token(payload)

        logger.info(f"Access token refreshed for user: {user.email}")

        return TokenResponse(access_token=access_token)

    async def get_user_from_token(
        self,
        token: str,
        session: AsyncSession,
    ) -> User:
        """
        Get user from an access token.

        Args:
            token: Access token
            session: Database session

        Returns:
            User object

        Raises:
            InvalidTokenError: If token is invalid or not an access token
            UserNotFoundError: If user is not found
        """
        # Decode and validate the access token (checks type automatically)
        payload = self.token_service.decode_token(token, expected_type="access")

        user_id = payload.get("sub")
        if not user_id:
            logger.warning("Access token missing 'sub' claim")
            raise InvalidTokenError("Invalid access token")

        # Get user
        user = await self.user_service.get_user_by_id(session, int(user_id))

        if not user.is_active:
            logger.warning(f"Inactive user attempted to use access token: {user.email}")
            raise InvalidCredentialsError("User account is inactive")

        return user


auth_service = AuthService(
    user_service=user_service,
    token_service=token_service,
)

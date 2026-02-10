import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from core.schemas.user import UserCreate
from core.security import get_password_hash
from core.exceptions import UserAlreadyExistsError, UserNotFoundError

logger = logging.getLogger(__name__)


class UserService:
    """Service for user management operations."""

    async def get_user_by_id(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> User:
        """
        Get a user by their ID.

        Args:
            session: Database session
            user_id: User ID

        Returns:
            User object

        Raises:
            UserNotFoundError: If user is not found
        """
        user = await session.get(User, user_id)
        if not user:
            logger.debug(f"User not found with id: {user_id}")
            raise UserNotFoundError(f"User with id {user_id} not found")
        return user

    async def get_user_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> User | None:
        """
        Get a user by their email.

        Args:
            session: Database session
            email: User email

        Returns:
            User object or None if not found
        """
        result = await session.scalar(select(User).where(User.email == email))
        return result

    async def get_user_by_username(
        self,
        session: AsyncSession,
        username: str,
    ) -> User | None:
        """
        Get a user by their username.

        Args:
            session: Database session
            username: Username

        Returns:
            User object or None if not found
        """
        result = await session.scalar(select(User).where(User.username == username))
        return result

    async def create_user(
        self,
        session: AsyncSession,
        user_data: UserCreate,
    ) -> User:
        """
        Create a new user.

        Args:
            session: Database session
            user_data: User creation data

        Returns:
            Created user object

        Raises:
            UserAlreadyExistsError: If user with email or username already exists
        """
        # Check if user with email exists
        if await self.get_user_by_email(session, user_data.email):
            logger.warning(
                f"Attempt to create user with existing email: {user_data.email}"
            )
            raise UserAlreadyExistsError(
                f"User with email {user_data.email} already exists"
            )

        # Check if user with username exists
        if await self.get_user_by_username(session, user_data.username):
            logger.warning(
                f"Attempt to create user with existing username: {user_data.username}"
            )
            raise UserAlreadyExistsError(
                f"User with username {user_data.username} already exists"
            )

        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        logger.info(f"Created new user: {new_user.email}")
        return new_user


user_service = UserService()

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth_service import auth_service, AuthService
from services.user_service import user_service, UserService
from db import db_session_manager
from db.models import User
from core.exceptions import (
    InvalidTokenError,
    TokenExpiredError,
    UserNotFoundError,
    InvalidCredentialsError,
)

http_bearer = HTTPBearer()


def get_auth_service() -> AuthService:
    """Get the authentication service instance."""
    return auth_service


def get_user_service() -> UserService:
    """Get the user service instance."""
    return user_service


async def get_current_user(
    token: str = Depends(http_bearer),
    auth_service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(db_session_manager.get_async_session),
) -> User:
    """
    Dependency to get the current authenticated user from a token.
    
    Args:
        token: Bearer token from Authorization header
        auth_service: Injected authentication service
        session: Database session
    
    Returns:
        The authenticated user
    
    Raises:
        HTTPException: 401 if authentication fails
    """
    try:
        return await auth_service.get_user_from_token(token.credentials, session)
    except (InvalidTokenError, TokenExpiredError, UserNotFoundError, InvalidCredentialsError) as e:
        raise HTTPException(status_code=401, detail=str(e))


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to get the current active user.
    
    Args:
        current_user: The current authenticated user
    
    Returns:
        The current user if active
    
    Raises:
        HTTPException: 400 if user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


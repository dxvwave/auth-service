from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_auth_service
from core.schemas.user import UserResponse
from services.auth import AuthService
from db import db_session_manager

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    token: str,
    auth_service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(db_session_manager.get_async_session),
):
    user = await auth_service.validate_token_and_user(token, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return UserResponse(**user.__dict__)

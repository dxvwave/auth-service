from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_auth_service
from core.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
)
from services.auth import AuthService
from db import db_session_manager

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    user_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(db_session_manager.get_async_session),
):
    try:
        return await auth_service.authenticate_user(
            user_data.email,
            user_data.password,
            session,
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(db_session_manager.get_async_session),
):
    try:
        user = await auth_service.register_user(user_data, session)
        return UserResponse(**user.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str = Body(...),
    auth_service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(db_session_manager.get_async_session),
):
    try:
        return await auth_service.refresh_access_token(refresh_token, session)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

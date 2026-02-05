from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_auth_service
from core.schemas.user import UserCreateSchema, UserLoginSchema, UserSchema, TokenSchema
from services.auth import AuthService
from db import db_session_manager

router = APIRouter()


@router.post("/login", response_model=TokenSchema)
async def login(
    user_data: UserLoginSchema,
    auth_service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(db_session_manager.get_async_session),
):
    return await auth_service.authenticate_user(
        email=user_data.email,
        password=user_data.password,
        session=session,
    )


@router.post("/register", response_model=UserSchema)
async def register(
    user_data: UserCreateSchema,
    auth_service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(db_session_manager.get_async_session),
):
    user = await auth_service.register_user(user_data, session)
    return UserSchema(**user.__dict__)

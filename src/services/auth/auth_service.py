from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from core.schemas.user import UserCreateSchema, TokenSchema
from core.security import (
    verify_password,
    create_access_token,
    get_password_hash,
)


class AuthService:
    async def _check_user_exists(
        self,
        email: str,
        session: AsyncSession,
    ) -> bool:
        user = await session.scalar(select(User).where(User.email == email))
        if user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered",
            )
        return user

    async def register_user(
        self,
        user_data: UserCreateSchema,
        session: AsyncSession,
    ):
        await self._check_user_exists(user_data.email, session)

        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        session.add(new_user)
        await session.commit()
        return new_user

    async def authenticate_user(
        self,
        email: str,
        password: str,
        session: AsyncSession,
    ):
        user = await session.scalar(select(User).where(User.email == email))

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        payload = {
            "user_id": user.id,
            "email": user.email,
        }

        access_token = create_access_token(payload=payload)
        return TokenSchema(access_token=access_token)


auth_service_instance = AuthService()

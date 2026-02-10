from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from core.schemas.user import UserCreate, TokenResponse
from core.security import (
    verify_password,
    create_access_token,
    get_password_hash,
    decode_token,
)


class AuthService:
    async def get_user_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> User | None:
        return await session.scalar(select(User).where(User.email == email))

    async def get_user_by_id(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> User | None:
        return await session.get(User, user_id)

    async def register_user(
        self,
        user_data: UserCreate,
        session: AsyncSession,
    ) -> User:
        if await self.get_user_by_email(session, user_data.email):
            raise ValueError("User with this email already exists")

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
        return new_user

    async def authenticate_user(
        self,
        email: str,
        password: str,
        session: AsyncSession,
    ):
        user = await self.get_user_by_email(session, email)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        payload = {
            "sub": str(user.id),
            "email": user.email,
        }

        access_token = create_access_token(payload=payload)
        return TokenResponse(access_token=access_token)

    async def validate_token_and_user(
        self,
        token: str,
        session: AsyncSession,
    ) -> User | None:
        try:
            payload = decode_token(token)
            user_id = payload.get("sub")
            if not user_id:
                return None
            return await self.get_user_by_id(session, int(user_id))
        except Exception:
            return None


auth_service_instance = AuthService()

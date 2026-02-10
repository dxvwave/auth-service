from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Base user schema with common fields."""

    first_name: str
    last_name: str
    username: str
    email: EmailStr


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class UserCreate(UserBase):
    """Schema for user creation."""

    password: str


class UserResponse(UserBase):
    """Schema for user response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_superuser: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


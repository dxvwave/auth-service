from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserCreateSchema(UserBaseSchema):
    password: str


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool | None
    is_superuser: bool | None
    is_verified: bool | None


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

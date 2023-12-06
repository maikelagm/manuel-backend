from uuid import UUID

from fastapi_utils.api_model import APIModel
from pydantic import EmailStr

from .role import Role


class UserBase(APIModel):
    email: EmailStr
    ci: str
    username: str
    name: str
    surname: str
    role: Role


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    pass


class UserInDBBase(UserBase):
    id: UUID


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str

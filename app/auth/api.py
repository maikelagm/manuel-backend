import uuid

from fastapi_users import FastAPIUsers

from app.auth.backend import jwt_backend
from app.auth.db import User
from app.auth.user_manager import get_user_manager

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [jwt_backend],
)

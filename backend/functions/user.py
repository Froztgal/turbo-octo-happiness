from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import settings
from database.models.user import User
from exceptions.user import (
    UnauthorizedException,
    NotSuperUserException,
    InactiveUserException,
)

SECRET_KEY = settings.security.secret_key
ALGORITHM = settings.security.algorithm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(request: Request) -> User:
    # Get token
    token = request.cookies.get("bearer")
    if token is None:
        raise UnauthorizedException

    # Decode token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise UnauthorizedException

    # Get user from DB
    try:
        user_name: str = payload.get("user_name")
        user_db = await User.objects.aget(user_name=user_name)
    except User.DoesNotExist:
        raise UnauthorizedException

    return user_db


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise InactiveUserException
    return current_user


async def get_current_super_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise NotSuperUserException
    return current_user


def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

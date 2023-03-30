from datetime import datetime, timedelta
from typing import Annotated

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils import db_select
from config import settings
from database.base import get_session
from database.models.user import User
from schemas.token import Token, TokenData
from schemas.user import User as UserSchema
from schemas.user import UserCreate, UserDB, UserEmail, UserLogIn
from exceptions.user import UNAUTHORIZED
from exceptions.user import IVALID_CREDENTIALS

SECRET_KEY = settings.security.secret_key
ALGORITHM = settings.security.algorithm
TOKEN_EXPIRE = settings.security.token_expire

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(
    session: AsyncSession,
    user_name: str,
    email: str | None = None,
) -> User:

    # Generate query
    query = select(User).where(User.user_name == user_name)
    if email is not None:
        query = query.where(User.email == email)

    # Select from DB
    user_in_db = await db_select(query, session)

    # If not found return error response
    if user_in_db is not None:
        return user_in_db


async def get_current_user(
    reauest: Request,
    session: AsyncSession = Depends(get_session),
) -> UserDB:
    # Get token
    token = reauest.cookies.get("bearer")
    if token is None:
        raise UNAUTHORIZED

    # Decode token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise UNAUTHORIZED

    # Get user name from token
    user_name: str = payload.get("user_name")
    if user_name is None:
        raise UNAUTHORIZED

    # Get user from DB
    user_db = await get_user(session, user_name)
    if user_db is None:
        raise UNAUTHORIZED

    return user_db


async def get_current_active_user(
    current_user: UserDB = Depends(get_current_user),
) -> UserDB:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_super_user(
    current_user: UserDB = Depends(get_current_user),
) -> UserDB:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_token(data: dict, expire_minutes: int | None = None):
    to_encode = data.copy()
    if expire_minutes:
        delta = timedelta(minutes=expire_minutes)
    else:
        delta = timedelta(minutes=TOKEN_EXPIRE)
    expire = datetime.utcnow() + delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def login(session: AsyncSession, user: UserLogIn) -> UserDB:
    # Check user in DB
    user_db: User = await get_user(session, user.user_name)
    if user_db is None:
        return None

    # Check password
    login_state = pwd_context.verify(user.password, user_db.password_hash)
    if not login_state:
        return None

    # Update state to active
    user_db.is_active = True
    await session.commit()
    await session.refresh(user_db)

    return user_db


async def logout(
    session: AsyncSession,
    current_user: UserDB,
) -> UserDB:
    # Update state to active
    user = User(current_user.dict())
    user.is_active = False
    await session.commit()
    return


async def register(
    user: UserCreate, session: AsyncSession = Depends(get_session)
) -> User:
    # Generate password hash
    password_hash = pwd_context.hash(user.password)
    # Create user in DB
    user_db = User(**user.dict(exclude={"password"}), password_hash=password_hash)
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    return user_db

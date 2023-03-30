from datetime import datetime, timedelta
from typing import Annotated

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
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
from functions.user import (
    create_token,
    pwd_context,
    login,
    get_current_active_user,
    logout,
)
from exceptions.user import IVALID_CREDENTIALS


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/login/")
async def login_user(
    user: UserLogIn, session: AsyncSession = Depends(get_session)
) -> Response:
    user_db: UserDB = await login(session, user)
    if not user_db:
        raise IVALID_CREDENTIALS
    access_token = create_token(data={"user_name": user_db.user_name})
    response = Response(content="Login Success")
    response.set_cookie(key="bearer", value=access_token)
    return response


@router.get("/logout/")
async def logout_user(
    session: AsyncSession = Depends(get_session),
    current_user: UserDB = Depends(get_current_active_user),
) -> Response:
    await logout()
    response = Response(content="Logout Success")
    response.set_cookie(key="bearer", value=None)
    return response


@router.get("/")
async def get_users(
    page_size: int = 20, page: int = 0, session: AsyncSession = Depends(get_session)
) -> list[UserSchema]:
    query = select(User).offset(page * page_size).limit(page_size)
    result = await db_select(query, session)
    if result is None:
        return []
    elif isinstance(result, User):
        return [result]
    return result


@router.post("/register/")
async def register(
    user: UserCreate, session: AsyncSession = Depends(get_session)
) -> UserSchema:
    # Generate password hash
    password_hash = pwd_context.hash(user.password)
    # Create user in DB
    user_db = User(**user.dict(exclude={"password"}), password_hash=password_hash)
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)

    return user_db


@router.get("/me/items/")
async def read_own_items(current_user: UserDB = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.user_name}]


# @router.post("/reset-password")
# async def reset_password(user: UserEmail,
#                          session: AsyncSession = Depends(get_session)
#                          ) -> UserSchema:
#     obj = user.__dict__

#     query = select(User).\
#         where(User.user_name == obj["user_name"]).\
#         where(User.email == obj["email"])

#     user_in_db = await db_select(query, session)
#     if user_in_db is None:
#         return JSONResponse(content="Incorrect email or username",
#                             status_code=status.HTTP_404_NOT_FOUND)

#     return user_in_db

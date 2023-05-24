from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from api.utils import CommonQuery, get_common_query, filter_model
from database.models.user import User
from database.utils import many_to_pydantic
from exceptions.user import InvalidCredentialsException
from functions.user import (
    create_token,
    get_current_active_user,
    pwd_context,
)
from schemas.user import User as UserSchema
from schemas.user import UserCreate, UserLogIn, UserFlexible
from config import settings

router = APIRouter(prefix="/user", tags=["User"])

TOKEN_EXPIRE = settings.security.token_expire


@router.post("/login/")
async def login_user(user: UserLogIn) -> JSONResponse:
    # Check user exists
    try:
        user_db = await User.objects.aget(user_name=user.user_name)
    except User.DoesNotExist:
        raise InvalidCredentialsException

    # Check password
    login_state = pwd_context.verify(user.password, user_db.password_hash)
    if not login_state:
        raise InvalidCredentialsException

    # Update state to active
    user_db.is_active = True
    await user_db.asave()

    # Set token and return success message
    access_token = create_token(data={"user_name": user_db.user_name})
    response = JSONResponse(content="Login Success")
    response.set_cookie(key="bearer", value=access_token, expires=TOKEN_EXPIRE)
    return response


@router.get("/logout/")
async def logout_user(
    user: User = Depends(get_current_active_user),
) -> JSONResponse:
    # Update state to inactive
    user.is_active = False
    await user.asave()

    # Delete token and return success message
    response = JSONResponse(content="Logout Success")
    response.delete_cookie(key="bearer")
    return response


@router.get("/", response_model_exclude_none=True)
async def get_users(
    params: CommonQuery = Depends(get_common_query),
) -> list[UserFlexible]:
    result = filter_model(User, params)
    return many_to_pydantic(result, UserFlexible)


@router.post("/register/", response_model=None)
async def register(user: UserCreate) -> UserSchema | JSONResponse:
    # Generate password hash
    password_hash = pwd_context.hash(user.password)

    # Check user already exists and if not create a new one
    user_db, created = User.objects.get_or_create(
        user_name=user.user_name,
        email=user.email,
        defaults={"password_hash": password_hash},
    )

    if created:
        return user_db.to_pydantic(UserSchema)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": "User name or email already registered!"},
    )


@router.get("/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
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

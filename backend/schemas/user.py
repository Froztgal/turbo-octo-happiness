from pydantic import BaseModel, EmailStr, Field, UUID4


class UserBase(BaseModel):
    user_name: str


class UserEmail(UserBase):
    email: EmailStr


class UserCreate(UserEmail):
    password: str = Field(
        regex="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    )


class UserLogIn(UserBase):
    password: str = Field(
        regex="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    )


class UserUpdate(BaseModel):
    user_name: str | None
    email: EmailStr | None
    password: str | None = Field(
        regex="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    )


class User(UserEmail):
    id: UUID4
    is_active: bool
    is_superuser: bool


class UserDB(UserEmail):
    id: UUID4
    password_hash: str
    is_active: bool
    is_superuser: bool


class UserFlexible(UserEmail):
    id: UUID4 | None
    password_hash: str | None
    is_active: bool | None
    is_superuser: bool | None

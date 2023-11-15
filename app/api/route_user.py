from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.exceptions import UniqueUserEmailException
from app.exceptions import UniqueUsernameException
from app.orm.user import create_new_user
from app.orm.user import get_user_by_email
from app.orm.user import get_user_by_username
from app.orm.user import show_users
from app.schemas.user import GetUser
from app.schemas.user import UserCreate


api_router = APIRouter(prefix="/api", tags=["users"])


@api_router.post(
    "/create_user/",
    response_model=GetUser,
    status_code=status.HTTP_201_CREATED,
    description="Регистрация пользователя",
)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    """
    Маршрут для создания пользователя.
    При создании проверяется уникальность указанных имени пользователя и электронной почты.
    """

    find_user_by_email = await get_user_by_email(db, user.email)
    if find_user_by_email:
        raise UniqueUserEmailException

    find_user_by_username = await get_user_by_username(db, user.username)
    if find_user_by_username:
        raise UniqueUsernameException

    user = await create_new_user(user=user, db=db)
    return user


@api_router.get(
    "/get_users/",
    response_model=List[GetUser],
    status_code=status.HTTP_200_OK,
    description="Список зарегистрированных пользователей",
)
async def get_users(db: AsyncSession = Depends(get_async_session)):
    """
    Маршрут для получения списка зарегистрированных пользователей.
    """

    users = await show_users(async_db=db)
    return users

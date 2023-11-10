from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.exceptions import UniqueUserEmailException, UniqueUsernameException
from app.orm.user import create_new_user, get_user_by_email, get_user_by_username, show_users
from app.schemas.user import UserCreate, GetUser


api_router = APIRouter(prefix="/api", tags=["users"])


@api_router.post("/create_user/", response_model=GetUser,
                 status_code=status.HTTP_201_CREATED,
                 description='Регистрация пользователя')
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    """
    Маршрут для создания пользователя.
    При создании проверяется уникальность указанных имени пользователя и электронной почты.
    """

    db_user_email = await get_user_by_email(db, user.email)
    if db_user_email:
        raise UniqueUserEmailException

    db_user_username = await get_user_by_username(db, user.username)
    if db_user_username:
        raise UniqueUsernameException

    user = await create_new_user(user=user, db=db)
    return user


@api_router.get("/get_users/", response_model=List[GetUser],
                status_code=status.HTTP_200_OK,
                description="Список зарегистрированных пользователей")
async def get_users(db: AsyncSession = Depends(get_async_session)):
    """
    Маршрут для получения списка зарегистрированных пользователей.
    """

    users = await show_users(async_db=db)
    return users

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.repository.user import create_new_user, get_user_by_email, get_user_by_username
from app.schemas.user import UserCreate, GetUser


api_router = APIRouter(prefix="", tags=["users"])


@api_router.post("/", response_model=GetUser,
                 status_code=status.HTTP_201_CREATED,
                 description='Регистрация пользователя')
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    """
    Контроллер для создания пользователя.
    При создании проверяется уникальность указанных имени пользователя и электронной почты.
    """

    db_user_email = await get_user_by_email(db, user.email)
    if db_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Электронная почта '{user.email}' уже используется")

    db_user_username = await get_user_by_username(db, user.username)
    if db_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Имя пользователя '{user.username}' уже используется")

    user = await create_new_user(user=user, db=db)
    return user

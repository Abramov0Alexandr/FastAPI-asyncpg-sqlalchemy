from typing import Annotated
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.exceptions import UniqueUserEmailException
from app.exceptions import UniqueUsernameException
from app.exceptions import UserInstanceException
from app.orm.user import create_new_user
from app.orm.user import get_user_by_email
from app.orm.user import get_user_by_username
from app.orm.user import show_users
from app.schemas.user import GetUser
from app.schemas.user import TokenResponse
from app.schemas.user import UserCreate
from app.service.auth import create_access_token
from app.service.hashing import Hasher

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
@cache(expire=50, namespace="user_list")
async def get_users(db: AsyncSession = Depends(get_async_session)):
    """
    Маршрут для получения списка зарегистрированных пользователей.
    """

    users = await show_users(async_db=db)
    return users


@api_router.post(
    "/token/", status_code=status.HTTP_200_OK, response_model=TokenResponse
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_async_session),
):

    """
    Endpoint для получения токена доступа (JWT) при аутентификации пользователя.

    Args:
        db (AsyncSession): Сессия базы данных.
        form_data (OAuth2PasswordRequestForm): Форма для указания данных пользователя при аутентификации.

    Returns:
        Dict[str, str]: Токен доступа и тип токена.
    """

    _user = await get_user_by_username(username=form_data.username, db=db)
    if not _user:
        raise UserInstanceException

    if not Hasher.verify_password(form_data.password, _user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Проверьте правильность указанного пароля",
        )

    access_token = await create_access_token(_user)
    return {"access_token": access_token, "token_type": "bearer"}

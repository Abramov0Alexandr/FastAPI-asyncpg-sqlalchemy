from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas.user import UserCreate


async def get_user_by_email(db: AsyncSession, email: str):
    """
    Асинхронная функция, представляющая собой ORM запрос.
    При ее вызове происходит обращение к базе данных, результатом является пользователь, полученный по email.
    """

    query = select(User).filter(User.email == email)
    result = await db.execute(query)
    return result.first()


async def get_user_by_username(db: AsyncSession, username: str):
    """
    Асинхронная функция, представляющая собой ORM запрос.
    При ее вызове происходит обращение к базе данных, результатом является пользователь, полученный по username.
    """

    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    return result.first()


async def create_new_user(user: UserCreate, db: AsyncSession):
    """
    Асинхронная функция, представляющая собой ORM запрос.
    В ходе выполнения функции происходит создание нового пользователя.
    """

    query = insert(User).values(
        **user.model_dump(),
        is_active=True,
        is_superuser=False
    ).returning(User)

    result = await db.execute(query)
    created_user = result.scalar()
    await db.commit()
    return created_user


async def show_users(async_db: AsyncSession):
    """
    Асинхронная функция, представляющая собой ORM запрос.
    Результатом запроса является список зарегистрированных пользователей
    """

    query = select(User)
    user_list = await async_db.execute(query)
    return user_list.scalars().all()

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.config import DATABASE_URL


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Адаптер базы данных пользователей FastAPI обеспечивает связь между конфигурацией вашей базы данных и
# логикой пользователей. Он должен быть сгенерирован зависимостью FastAPI.
# https://fastapi-users.github.io/fastapi-users/12.1/configuration/databases/sqlalchemy/

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

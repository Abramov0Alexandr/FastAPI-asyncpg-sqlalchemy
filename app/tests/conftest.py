import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import test_db_settings
from app.database import get_async_session
from app.main import app
from app.models.base_class import Base
from app.models.base_class import metadata


# Настройки движка для тестовой базы данных.
engine_test = create_async_engine(test_db_settings.DATABASE_URL)
async_session = async_sessionmaker(
    engine_test, expire_on_commit=False, class_=AsyncSession
)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Функция для изменения зависимости подключения к тестовой базе данных.
    """

    async with async_session() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    """
    Функция, позволяющая создать таблицы перед выполнением тестов и удалить их после завершения.
    """

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Асинхронный объект Client, который будет использоваться для обращения к маршрутам.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

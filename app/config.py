import os

from dotenv import load_dotenv

load_dotenv()


# Settings of project information.
project_settings = {
    "title": "Fast API application",
    "version": "1.0",
    "description": "Fast API application. Application include asyncpg+sqlalchemy technologies",
}


# Settings for database connection
class ProdDBSettings:
    """
    Класс, содержащий основные настройки для подключения к рабочей базе данных.
    """

    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT", 5432)
    DB_NAME: str = os.getenv("DB_NAME")
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class JWTTokenSettings:
    """
    Класс, содержащий основные настройки для созданий JWT токена.
    """

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    TOKEN_LIFESPAN: int = int(os.getenv("TOKEN_LIFESPAN"))
    VERIFY_SIGNATURE: str = os.getenv("VERIFY_SIGNATURE")


class TestDBSettings:
    """
    Класс, содержащий основные настройки для подключения к тестовой базе данных.
    """

    DB_USER: str = "postgres"
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "db_test_api"
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


prod_db_settings = ProdDBSettings()
jwt_token_settings = JWTTokenSettings()
test_db_settings = TestDBSettings()

import os
from dotenv import load_dotenv


# Settings of project information.
project_settings = {
    "title": "My app",
    "version": "1.0",
    "description": "Мое новое тестовое приложение"
}


# Settings for database connection
load_dotenv()

DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_HOST: str = os.getenv("DB_HOST")
DB_PORT: str = os.getenv("DB_PORT", 5432)
DB_NAME: str = os.getenv("DB_NAME")
DATABASE_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

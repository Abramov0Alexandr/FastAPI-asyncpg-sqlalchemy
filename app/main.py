from fastapi import FastAPI
from app.api.user import api_router
from app.config import project_settings
from app.database import engine
from app.models.base_class import Base


def include_router(app):
    app.include_router(api_router)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def start_application():
    target_app = FastAPI(**project_settings)
    create_db_and_tables()
    include_router(target_app)
    return target_app


start_app = start_application()


@start_app.get("/", tags=["test routes"])
async def home():
    return {"msg": "Hello FastAPI🚀"}

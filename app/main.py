from fastapi import FastAPI
from app.config import project_settings
from app.database import engine
from app.models.base_class import Base


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def start_application():
    target_app = FastAPI(**project_settings)
    create_db_and_tables()
    return target_app


app = start_application()


@app.get("/")
def home():
    return {"msg": "Hello FastAPI🚀"}

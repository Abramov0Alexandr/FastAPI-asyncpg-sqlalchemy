from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.api.route_blog import api_router as blog_route
from app.api.route_user import api_router as user_route
from app.config import project_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Настройки подключения брокера
    # https://github.com/long2ice/fastapi-cache#usage
    redis = aioredis.from_url("redis://localhost/")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    print("start app")
    yield
    print("close app")


app = FastAPI(lifespan=lifespan, **project_settings)
app.include_router(user_route)
app.include_router(blog_route)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

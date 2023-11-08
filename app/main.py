import uvicorn
from fastapi import FastAPI
from app.api.route_user import api_router as user_route
from app.api.route_blog import api_router as blog_route
from app.config import project_settings


app = FastAPI(**project_settings)
app.include_router(user_route)
app.include_router(blog_route)


@app.get("/", tags=["test routes"])
async def home():
    return {"msg": "Hello FastAPI🚀"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

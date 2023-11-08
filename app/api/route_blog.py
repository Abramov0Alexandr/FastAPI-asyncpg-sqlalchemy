from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.database import get_async_session
from app.orm.blog import create_new_blog
from app.schemas import ShowBlog, BlogCreate


api_router = APIRouter(prefix="/api", tags=["blog"])


@api_router.post("/create_blog", response_model=ShowBlog,
                 status_code=status.HTTP_201_CREATED,
                 description="Создание новой публикации для блога")
async def create_blog(creation_blog_schema: BlogCreate, db: AsyncSession = Depends(get_async_session)):
    """
    Маршрут для создания публикации в личном блоге.
    """

    blog = await create_new_blog(creation_blog_schema=creation_blog_schema, async_db=db, author_id=1)
    return blog

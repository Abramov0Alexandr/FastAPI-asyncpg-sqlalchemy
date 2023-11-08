from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Blog
from app.schemas import BlogCreate


async def create_new_blog(creation_blog_schema: BlogCreate, async_db: AsyncSession, author_id: int):

    """
    Асинхронная функция, представляющая собой ORM запрос.
    В ходе выполнения функции происходит создание нового блога.
    """

    query = insert(Blog).values(
        **creation_blog_schema.model_dump(),
        author_id=author_id
    ).returning(Blog)

    result = await async_db.execute(query)
    await async_db.commit()
    created_blog = result.scalar()
    return created_blog

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Blog
from app.schemas import BlogCreate


async def create_new_blog(blog_schema: BlogCreate, async_db: AsyncSession, author_id: int):
    """
    Асинхронная функция, представляющая собой ORM запрос.
    В ходе выполнения функции происходит создание нового блога.
    """

    query = insert(Blog).values(
        **blog_schema.model_dump(),
        author_id=author_id
    ).returning(Blog)

    result = await async_db.execute(query)
    await async_db.commit()
    created_blog = result.scalar()
    return created_blog


async def retrieve_blog(blog_id: int, async_db: AsyncSession):
    """
    Асинхронная функция, представляющая собой ORM запрос.
    В ходе выполнения функции происходит поиск блога по переданному в запросе id.
    """

    query = select(Blog).filter(Blog.id == blog_id)
    specific_blog = await async_db.execute(query)
    return specific_blog.scalar()


async def list_blog(async_db: AsyncSession):
    """
    Асинхронная функция, представляющая собой ORM запрос.
    Функция позволяет получить список объектов модели Blog со статусом "is_active".
    """

    query = select(Blog).filter(Blog.is_active)
    blog_list = await async_db.execute(query)
    return blog_list.scalars()

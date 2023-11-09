from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Blog
from app.schemas import BlogCreate, UpdateBlog


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
    created_blog = result.scalar()
    await async_db.commit()
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


async def update_specific_blog(blog_id: int, blog_schema: UpdateBlog, author_id: int, async_db: AsyncSession):
    query = update(Blog).where(Blog.id == blog_id).values(blog_schema.model_dump(exclude_unset=True)).returning(Blog)
    result = await async_db.execute(query)
    await async_db.commit()
    return result.scalar()

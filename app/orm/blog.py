from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import BlogInstanceException
from app.models.blog import Blog
from app.schemas.blog import BlogCreate
from app.schemas.blog import UpdateBlog


async def get_blog_by_title(blog_title: str, async_db: AsyncSession):
    """
    Асинхронная функция, представляющая собой ORM запрос.
    При ее вызове происходит обращение к базе данных, результатом является объект модели Blog с указанным полем title.
    """

    query = select(Blog).where(Blog.title == blog_title)
    result_blog = await async_db.execute(query)
    return result_blog.scalar()


async def create_new_blog(
    blog_schema: BlogCreate, async_db: AsyncSession, author_id: int
):
    """
    Асинхронная функция, представляющая собой ORM запрос.
    В ходе выполнения функции происходит создание нового блога.
    """

    query = (
        insert(Blog)
        .values(**blog_schema.model_dump(), author_id=author_id)
        .returning(Blog)
    )

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


async def update_specific_blog(
    blog_id: int, blog_schema: UpdateBlog, author_id: int, async_db: AsyncSession
):
    """
    Асинхронная функция, представляющая собой ORM запрос.
    Функция дл обновления объекта модели Blog.
    """

    query = (
        update(Blog)
        .where(Blog.id == blog_id)
        .values(blog_schema.model_dump(exclude_unset=True))
        .returning(Blog)
    )
    result = await async_db.execute(query)
    await async_db.commit()
    return result.scalar()


async def destroy_blog(blog_id: int, author_id: int, async_db: AsyncSession):
    """
    Асинхронная функция, представляющая собой ORM запрос.
    Результатам выполнения функции является удаление объекта модели Blog.
    """

    query = delete(Blog).where(Blog.id == blog_id)
    result = await async_db.execute(
        query.execution_options(synchronize_session="fetch")
    )

    if result.rowcount == 0:
        raise BlogInstanceException

    await async_db.commit()

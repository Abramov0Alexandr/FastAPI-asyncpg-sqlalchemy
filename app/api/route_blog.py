from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.database import get_async_session
from app.orm import blog as blog_orm
from app.schemas import ShowBlog, BlogCreate, UpdateBlog

api_router = APIRouter(prefix="/api", tags=["blog"])


@api_router.post("/create_blog/", response_model=ShowBlog,
                 status_code=status.HTTP_201_CREATED,
                 description="Создание новой публикации для блога")
async def create_blog(creation_blog_schema: BlogCreate, db: AsyncSession = Depends(get_async_session)):
    """
    Маршрут для создания публикации в личном блоге.
    """

    check_blog_title = await blog_orm.get_blog_by_title(creation_blog_schema.title, async_db=db)

    if check_blog_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Название для блога '{creation_blog_schema.title}' уже используется")

    blog = await blog_orm.create_new_blog(blog_schema=creation_blog_schema, async_db=db, author_id=1)
    return blog


@api_router.get("/detail_blog/{blog_id}/", response_model=ShowBlog,
                status_code=status.HTTP_200_OK, description='Получение информации о блоге')
async def get_blog(blog_id: int, db: AsyncSession = Depends(get_async_session)):
    blog = await blog_orm.retrieve_blog(blog_id=blog_id, async_db=db)

    if not blog:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Блога с ID: {blog_id} не существует")
    return blog


@api_router.get("/list_blog/", response_model=List[ShowBlog],
                status_code=status.HTTP_200_OK, description="Получение списка созданных блогов")
async def get_list_blog(db: AsyncSession = Depends(get_async_session)):
    blog_list = await blog_orm.list_blog(async_db=db)
    return blog_list


@api_router.put("/update_blog/{blog_id}/", response_model=ShowBlog,
                status_code=status.HTTP_200_OK, description="Редактирование блога")
async def update_blog(blog_id: int, schema: UpdateBlog, db: AsyncSession = Depends(get_async_session)):

    check_blog_title = await blog_orm.get_blog_by_title(schema.title, async_db=db)

    if check_blog_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Название для блога '{schema.title}' уже используется")

    blog = await blog_orm.update_specific_blog(blog_id=blog_id, blog_schema=schema, author_id=1, async_db=db)

    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Блог с ID: {blog_id} не найден")

    return blog


@api_router.delete("/delete_blog/{blog_id}/", status_code=status.HTTP_200_OK, description="Удаление блога")
async def delete_blog(blog_id: int, db: AsyncSession = Depends(get_async_session)):
    await blog_orm.destroy_blog(blog_id=blog_id, author_id=1, async_db=db)

    return {
        "status": status.HTTP_200_OK,
        "detail": f"Блог с ID {blog_id} успешно удален"}

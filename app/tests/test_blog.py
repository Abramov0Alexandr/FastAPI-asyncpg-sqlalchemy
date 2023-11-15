import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from starlette import status

from app.models.blog import Blog
from app.tests.conftest import async_session


@pytest.mark.parametrize(
    "user_payload, blog_payload, status_code",
    (
        (
            {
                "username": "test_author",
                "password": "123654",
                "email": "author@example.com",
            },
            {"title": "Test title", "content": "Some test content"},
            status.HTTP_201_CREATED,
        ),
    ),
)
async def test_create_blog(
    async_client: AsyncClient, user_payload, blog_payload, status_code
):
    """
    TestCase для проверки маршрута создания объекта модели Blog.
    """

    await async_client.post("/api/create_user/", json=user_payload)

    response = await async_client.post("/api/create_blog/", json=blog_payload)
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Test title"
    assert response.json()["slug"] == "test-title"
    assert response.json()["content"] == "Some test content"
    assert response.status_code == status_code


async def test_get_specific_blog(async_client: AsyncClient):
    """
    TestCase для проверки получения указанного объекта модели Blog.
    """

    response = await async_client.get("/api/detail_blog/1/")
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Test title"
    assert response.json()["slug"] == "test-title"
    assert response.json()["content"] == "Some test content"
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "user_payload, blog_payload, status_code",
    (
        (
            {
                "username": "test_author",
                "password": "123654",
                "email": "author@example.com",
            },
            {
                "author_id": 1,
                "title": "Blog title",
                "slug": "blog-title",
                "content": "Some test content",
                "is_active": True,
            },
            status.HTTP_200_OK,
        ),
    ),
)
async def test_get_list_blog(
    async_client: AsyncClient, blog_payload, user_payload, status_code
):
    """
    TestCase для проверки получения списка объектов модели Blog.
    """

    await async_client.post("/api/create_user/", json=user_payload)

    async with async_session() as session:
        smtp = insert(Blog).values(**blog_payload).returning(Blog)

        await session.execute(smtp)
        await session.commit()

    list_blog = await async_client.get("/api/list_blog/")
    assert list_blog.json()[0]["id"] == 2
    assert list_blog.json()[0]["title"] == "Blog title"
    assert list_blog.json()[0]["slug"] == "blog-title"
    assert list_blog.json()[0]["content"] == "Some test content"
    assert list_blog.status_code == status_code


@pytest.mark.parametrize(
    "update_blog_payload, status_code",
    (({"title": "Updated title"}, status.HTTP_200_OK),),
)
async def test_list_blog(async_client: AsyncClient, update_blog_payload, status_code):
    """
    TestCase для проверки маршрута обновления объекта модели Blog.
    """

    response = await async_client.put("/api/update_blog/1/", json=update_blog_payload)

    assert response.json()["id"] == 1
    assert response.json()["title"] == "Updated title"
    assert response.json()["slug"] == "updated-title"
    assert response.json()["content"] == "Some test content"
    assert response.status_code == status_code

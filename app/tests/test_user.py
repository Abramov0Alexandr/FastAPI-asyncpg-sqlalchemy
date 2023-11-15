import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.parametrize(
    "payload, status_code, schema_result",
    (
        (
            {
                "username": "test_user",
                "password": "123654",
                "email": "test@example.com",
            },
            status.HTTP_201_CREATED,
            {"email": "test@example.com", "is_active": True},
        ),
    ),
)
async def test_create_user(
    async_client: AsyncClient, payload, status_code, schema_result
):
    """
    TestCase для проверки маршрута создания объекта модели User.
    """

    response = await async_client.post("/api/create_user/", json=payload)
    assert response.json() == schema_result
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "payload, status_code, error_msg",
    (
        (
            {
                "username": "test_user",
                "password": "123654",
                "email": "test1@example.com",
            },
            status.HTTP_400_BAD_REQUEST,
            {"detail": "Указанное имя пользователя уже используется"},
        ),
    ),
)
async def test_failed_username(
    async_client: AsyncClient, payload, status_code, error_msg
):
    """
    TestCase для проверки уникальности поля username при создании объекта модели User.
    """

    response = await async_client.post("/api/create_user/", json=payload)
    assert response.json() == error_msg
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "payload, status_code, error_msg",
    (
        (
            {
                "username": "test_user1",
                "password": "123654",
                "email": "test@example.com",
            },
            status.HTTP_400_BAD_REQUEST,
            {"detail": "Указанная электронная почта уже используется"},
        ),
    ),
)
async def test_failed_user_email(
    async_client: AsyncClient, payload, status_code, error_msg
):
    """
    TestCase для проверки уникальности поля email при создании объекта модели User.
    """

    response = await async_client.post("/api/create_user/", json=payload)
    assert response.json() == error_msg
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "payload, status_code, schema_result",
    (
        (
            {
                "username": "test_user1",
                "password": "123654",
                "email": "test1@example.com",
            },
            status.HTTP_200_OK,
            [
                {"email": "author@example.com", "is_active": True},
                {"email": "test@example.com", "is_active": True},
                {"email": "test1@example.com", "is_active": True},
            ],
        ),
    ),
)
async def test_show_users(
    async_client: AsyncClient, payload, status_code, schema_result
):
    """
    TestCase для получения списка объектов модели User.
    """

    await async_client.post("/api/create_user/", json=payload)

    response = await async_client.get("/api/get_users/")
    assert response.json() == schema_result
    assert response.status_code == status_code

from fastapi import HTTPException
from starlette import status


class UserException(HTTPException):
    """
    Базовый класс исключения для объектов модели User.
    """

    pass


class BlogException(HTTPException):
    """
    Базовый класс исключения для объектов модели Blog.
    """

    pass


class UniqueUserEmailException(UserException):
    """
    Исключение вызывается при нарушении уникальности поля email у объектов модели User.
    """

    def __init__(self, *message):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
            if message
            else "Указанная электронная почта уже используется",
        )


class UniqueUsernameException(UserException):
    """
    Исключение вызывается при нарушении уникальности поля username у объектов модели User.
    """

    def __init__(self, *message):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
            if message
            else "Указанное имя пользователя уже используется",
        )


class UniqueBlogTitleException(BlogException):
    """
    Исключение вызывается при нарушении уникальности поля title у объектов модели Blog.
    """

    def __init__(self, *message):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message if message else "Указанное название блога уже используется",
        )


class BlogInstanceException(BlogException):
    """
    Исключение вызывается при передаче несуществующего значения ID объекта модели Blog.
    """

    def __init__(self, *message):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message if message else "Блог с указанным ID не существует",
        )

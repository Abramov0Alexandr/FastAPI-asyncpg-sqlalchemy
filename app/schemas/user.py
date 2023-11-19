from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserCreate(BaseModel):
    """
    Схема модели User, используется при создании нового пользователя.
    """

    username: str = Field(..., max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=6)


class GetUser(BaseModel):
    """
    Схема модели User, используется при выводе информации о новом пользователе после его создания.
    """

    email: EmailStr
    is_active: bool

    class ConfigDict:
        from_attributes = True


class UserLogin(BaseModel):
    """
    Схема для аутентификации пользователя.
    """

    username: str = Field(title="User’s nickname", description="User’s nickname")
    password: str = Field(title="User’s password", description="User’s password")

    class ConfigDict:
        from_attributes = True


class TokenResponse(BaseModel):
    """
    Схема используется при успешном создании токена.
    """

    access_token: str = Field(
        title="User’s access token", description="User’s access token"
    )
    token_type: str = Field(title="User’s token type", description="User’s token type")

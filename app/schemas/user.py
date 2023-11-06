from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """
    Схема модели User, используется при создании нового пользователя.
    """

    username: str
    email: EmailStr
    password: str = Field(..., min_length=6)


class GetUser(BaseModel):
    """
    Схема модели User, используется при выводе информации о новом пользователе после его создания.
    """

    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

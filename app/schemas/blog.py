from datetime import datetime
from pydantic import BaseModel, model_validator, Field
from typing_extensions import Optional


class BlogCreate(BaseModel):
    """
    Схема модели Blog, используется при создании новой публикации.
    """

    title: str = Field(..., min_length=3, max_length=30)
    slug: Optional[str] = None
    content: Optional[str] = None

    @model_validator(mode='before')
    def generate_slug(cls, values):
        """
        Метод для генерации поля "slug" для модели Blog.
        """

        if 'title' in values:
            values['slug'] = '-'.join(values['title'].split()).strip().lower()

        return values


class ShowBlog(BaseModel):
    """
    Схема модели Blog, используется при выводе информации о новой публикации после ее создания.
    """

    title: str = Field(..., min_length=3, max_length=30)
    slug: Optional[str] = None
    content: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

from typing import List
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base_class import Base


if TYPE_CHECKING:
    from .blog import Blog


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[EmailStr] = mapped_column(
        String, nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    blogs: Mapped[List["Blog"]] = relationship("Blog", back_populates="author")

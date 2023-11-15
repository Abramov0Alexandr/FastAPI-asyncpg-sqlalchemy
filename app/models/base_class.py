from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative


metadata = MetaData()


@as_declarative()
class Base:
    """
    Базовый класс, от которого будут наследоваться остальные классы.
    """

    id: Any
    __name__: str
    metadata = metadata

    # to generate tablename from classname
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

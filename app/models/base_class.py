from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative, mapped_column, Mapped


@as_declarative()
class Base:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    __name__: str

    # to generate tablename from classname
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

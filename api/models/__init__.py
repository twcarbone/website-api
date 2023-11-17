from __future__ import annotations

import decimal
import re

import sqlalchemy as sa
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.ext.hybrid as hybrid
import sqlalchemy.orm as orm
import typing_extensions

from config import Config

str_20 = typing_extensions.Annotated[str, 20]
str_100 = typing_extensions.Annotated[str, 100]
str_500 = typing_extensions.Annotated[str, 500]
byt_60 = typing_extensions.Annotated[bytes, 60]
num_6_3 = typing_extensions.Annotated[decimal.Decimal, 6]


def engine(user: str, password: str, host: str, port: int, database: str):
    url = sa.URL.create(
        Config.DB_DRIVER,
        username=user,
        password=password,
        host=host,
        port=port,
        database=database,
    )

    return sa.create_engine(url=url)


class Base(orm.DeclarativeBase):
    metadata = sa.MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s_%(referred_column_0_name)s",
            "pk": "pk_%(table_name)s",
        },
    )

    registry = orm.registry(
        type_annotation_map={
            str_20: sa.String(20),
            str_100: sa.String(100),
            str_500: sa.String(500),
            byt_60: sa.LargeBinary(60),
            num_6_3: sa.Numeric(6, 3),
        }
    )

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    def __repr__(self: Base) -> str:
        """
        Return '<TableName column1=value1, column2=value2, column3=value3>'
        representation of *self*.

        Example:
        ```
        >>> Dog(name="Cheese", breed="Schnoodle")
        >>> <Dog id=1, name='Cheese', breed='Schnoodle'>
        ```
        """
        class_name = type(self).__name__
        column_kvs = ", ".join([f"{c}={getattr(self, c)!r}" for c in self._columns()])
        return f"<{class_name} {column_kvs}>"

    def _columns(self: Base) -> list[str]:
        """
        Return all column names of *self* with 'id' column at front.

        Example:
        ```
        >>> Dog()._columns()
        >>> ['id', 'name', 'breed']
        ```
        """
        columns = self.__table__.columns.keys()
        columns.insert(0, columns.pop(columns.index("id")))  # Ensure 'id' is at front
        return columns

    @orm.declared_attr
    def __tablename__(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower() + "_"

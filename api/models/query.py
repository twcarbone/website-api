import typing

from api import db
from api.models import sa


class QueryMixin:
    """
    Query utilities.
    """

    @classmethod
    def _result(cls, column: str, order_by: str, **kwargs) -> sa.engine.Result:
        if column is None:
            query = sa.select(cls)
        else:
            query = sa.select(getattr(cls, column))

        return db.session.execute(query.filter_by(**kwargs).order_by(order_by))

    @classmethod
    def all(cls, column: str = None, order_by: str = None, **kwargs) -> list[sa.engine.Row]:
        """
        Return list of `Row` objects.
        """
        return cls._result(column, order_by, **kwargs).all()

    @classmethod
    def scalars(cls, column: str = None, order_by: str = None, **kwargs) -> list[typing.Any]:
        """
        Return list of column values.
        """
        return cls._result(column, order_by, **kwargs).scalars().all()

    @classmethod
    def scalar_one(cls, column: str = None, **kwargs) -> typing.Any:
        """
        Return exactly one scalar result.

        Raises `NoResultFound` if no results found.
        Raises `MultipleRestulsFound` if multiple results found.
        """
        return cls._result(column, None, **kwargs).scalar_one()

    @classmethod
    def scalar_one_or_none(cls, column: str = None, **kwargs) -> typing.Any | None:
        """
        Return exactly one scalar result or None.

        Raises `MultipleRestulsFound` if multiple results found.
        """
        return cls._result(column, None, **kwargs).scalar_one_or_none()

from __future__ import annotations

from api.models import Base
from api.models import date
from api.models import money
from api.models import orm
from api.models import sa
from api.models import str_20
from api.models import str_100
from api.models import str_500
from api.models.query import QueryMixin


class _CapitalOneBase(QueryMixin, Base):
    __abstract__ = True
    __table_args__ = {"schema": "capitalone"}


class Card(_CapitalOneBase):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    number: orm.Mapped[str_20] = orm.mapped_column(unique=True)
    name: orm.Mapped[str_100] = orm.mapped_column(unique=True)


class Category(_CapitalOneBase):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str_100] = orm.mapped_column(unique=True)


class Merchant(_CapitalOneBase):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str_100] = orm.mapped_column(unique=True)
    category_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(Category.id))


class Description(_CapitalOneBase):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str_100] = orm.mapped_column(unique=True)
    merchant_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(Merchant.id))


class TransactionType(_CapitalOneBase):
    DEBIT = 1
    CREDIT = 2

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str_20] = orm.mapped_column(unique=True)


class Transaction(_CapitalOneBase):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    date: orm.Mapped[date] = orm.mapped_column()
    post_date: orm.Mapped[date] = orm.mapped_column()
    card_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(Card.id))
    description_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(Description.id))
    transactiontype_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(TransactionType.id))
    amount: orm.Mapped[money]

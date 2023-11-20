from __future__ import annotations

import decimal

from api import db
from api.models import Base
from api.models import date
from api.models import money
from api.models import num_6_3
from api.models import orm
from api.models import sa
from api.models import str_20
from api.models import str_100
from api.models import str_500
from api.models.query import QueryMixin


class _ShopriteBase(QueryMixin, Base):
    __abstract__ = True
    __table_args__ = {"schema": "grocery"}


class ShopriteRateType(_ShopriteBase):
    PER_LB = 1
    PER_QTY = 2

    rate: orm.Mapped[str_20] = orm.mapped_column(unique=True)


class ShopriteOrder(_ShopriteBase):
    date: orm.Mapped[date] = orm.mapped_column(unique=True)


class ShopriteProduct(_ShopriteBase):
    code: orm.Mapped[str_20] = orm.mapped_column(unique=True)
    name: orm.Mapped[str_100]


class ShopriteProductDetail(_ShopriteBase):
    shopriteproduct_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(ShopriteProduct.id), unique=True)
    name: orm.Mapped[str_100]
    description: orm.Mapped[str_500]
    brand: orm.Mapped[str_100]
    sku: orm.Mapped[str_20] = orm.mapped_column(unique=True)


class ShopriteTransaction(_ShopriteBase):
    shopriteorder_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(ShopriteOrder.id))
    shopriteproduct_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(ShopriteProduct.id))
    shopriteratetype_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(ShopriteRateType.id))
    rate: orm.Mapped[money]
    qty: orm.Mapped[num_6_3]
    final: orm.Mapped[money]


class ShopriteDiscount(_ShopriteBase):
    shopritetransaction_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(ShopriteTransaction.id))
    amount: orm.Mapped[money]

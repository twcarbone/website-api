from __future__ import annotations

import datetime
import decimal
import itertools
import logging
import pathlib
import re
import typing

import requests

from api import db
from api.models import Base
from api.models import date
from api.models import exc
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

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)


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


# -----
# Views
# -----


class _ViewBase(QueryMixin, Base):
    __abstract__ = True
    __table_args__ = {"schema": "grocery"}


class ProductView(_ViewBase):
    id = sa.Column(sa.Integer(), primary_key=True)
    sku = sa.Column(sa.String(20))
    short_name = sa.Column(sa.String(100))
    long_name = sa.Column(sa.String(100))
    brand = sa.Column(sa.String(500))
    description = sa.Column(sa.String(500))


class OrderView(_ViewBase):
    id = sa.Column(sa.Integer(), primary_key=True)
    date = sa.Column(sa.Date())
    order_total = sa.Column(sa.Numeric())


class TransactionView(_ViewBase):
    id = sa.Column(sa.Integer(), primary_key=True)
    date = sa.Column(sa.Date())
    sku = sa.Column(sa.String(20))
    short_name = sa.Column(sa.String(100))
    long_name = sa.Column(sa.String(100))
    rate = sa.Column(sa.Numeric(8, 2))
    rate_type = sa.Column(sa.String(20))
    qty = sa.Column(sa.Numeric(6, 3))
    discount = sa.Column(sa.Numeric(8, 2))
    final = sa.Column(sa.Numeric(8, 2))


# -----
# Other
# -----


class ShopriteReceiptParser:
    MONEY_REGEX = "\$(\d+\.\d{2})"

    @staticmethod
    def re_group(pattern: str, line: str, cast=str) -> typing.Any:
        """
        If *pattern* is found in *line*, return the first matching group cast as *cast*.
        Otherwise, return an empty string.
        """
        try:
            return cast(re.search(pattern, line).group(1))
        except AttributeError:  # If no group matched
            return ""

    @classmethod
    def serialize_receipt_transactions(cls, receipt: pathlib.Path) -> list[dict]:
        """
        Serialize lines in *receipt* file.
        """
        with open(receipt, "r") as f:
            lines = [line.strip() for line in f.readlines()]

        # Join lines for each transaction as comma-separated list
        groups = [",".join(group) for k, group in itertools.groupby(lines, lambda x: x == "") if not k]

        serialized_receipt_transactions = []
        for group in groups:
            serialized = {
                "name": cls.re_group("^(.*?),", group),
                "code": cls.re_group(",(\d+),", group),
                "qty": cls.re_group(f",(\d+) . {cls.MONEY_REGEX},", group, int),
                "per_qty": cls.re_group(f",\d+ . {cls.MONEY_REGEX},", group, float),
                "lb": cls.re_group("Qty: (\d+(?:\.\d{1,2})?)lb", group, float),
                "per_lb": cls.re_group(f"Price: {cls.MONEY_REGEX}/lb", group, float),
                "discount": cls.re_group(f"\*\*SC\*\*.*{cls.MONEY_REGEX},", group, float),
                "final": cls.re_group(f",{cls.MONEY_REGEX}.*$", group, float),
            }
            serialized_receipt_transactions.append(serialized)
        return serialized_receipt_transactions

    @staticmethod
    def commit(row: _ShopriteBase, unique_column: str = None) -> int:
        """
        Try to add *row* to session and commit, returning the assigned id of *row*. If a
        unique constraint violation occurs, query for the row by column *unique_column*.
        """
        try:
            db.session.add(row)
            db.session.commit()
            return row.id
        except exc.IntegrityError:
            db.session.rollback()
            mapped = type(row)
            column = getattr(mapped, unique_column)
            value = getattr(row, unique_column)
            return db.session.execute(sa.select(mapped.id).filter(column == value)).scalar_one()

    @staticmethod
    def fetch(sku: str, store_id: int = 354):
        """
        GET product details for *sku* from *store_id* from Wakefern API.
        """
        url = f"https://storefrontgateway.brands.wakefern.com/api/stores/{store_id}/products/{sku}"
        return requests.get(url=url, headers={"x-site-host": "https://www.shoprite.com"})

    @classmethod
    def details(cls, code: str) -> None | dict:
        """
        Return product details, if any are found.
        """
        json_data = None
        if len(code) == 14 and (response := cls.fetch(sku=code)).status_code == 200:
            json_data = response.json()
        else:
            for i in range(10):
                if (response := cls.fetch(sku=code.zfill(13) + str(i))).status_code == 200:
                    json_data = response.json()
                    break

        if json_data is None:
            logging.warning(f"Did not find details for product code {code}")
            return

        return {
            "name": json_data.get("name"),
            "description": json_data.get("description"),
            "sku": json_data.get("sku"),
            "brand": json_data.get("brand"),
        }

    @classmethod
    def parse(cls, path: pathlib.Path) -> None:
        """
        Parse all receipt files matching the glob pattern *path*.
        """
        for receipt in sorted(path.parent.glob(path.stem + path.suffix)):
            logging.info(f"Parsing receipt '{receipt}' ...")
            order_id = cls.commit(ShopriteOrder(date=datetime.datetime.strptime(receipt.stem, r"%Y%m%d").date()))
            for serialized in cls.serialize_receipt_transactions(receipt):
                product_id = cls.commit(
                    ShopriteProduct(
                        name=serialized["name"],
                        code=serialized["code"],
                    ),
                    unique_column="code",
                )

                transaction_id = cls.commit(
                    ShopriteTransaction(
                        shopriteorder_id=order_id,
                        shopriteproduct_id=product_id,
                        shopriteratetype_id=1 if serialized["per_lb"] else 2,
                        rate=serialized["per_lb"] if serialized["per_lb"] else serialized["per_qty"],
                        qty=serialized["lb"] if serialized["lb"] else serialized["qty"],
                        final=serialized["final"],
                    ),
                )

                if ShopriteProductDetail.scalar_one_or_none(shopriteproduct_id=product_id) is None:
                    if (details := cls.details(code=serialized["code"])) is not None:
                        cls.commit(
                            ShopriteProductDetail(
                                shopriteproduct_id=product_id,
                                name=details["name"],
                                description=details["description"][:500],
                                brand=details["brand"],
                                sku=details["sku"],
                            )
                        )

                if serialized["discount"]:
                    cls.commit(
                        ShopriteDiscount(
                            shopritetransaction_id=transaction_id,
                            amount=serialized["discount"],
                        ),
                    )

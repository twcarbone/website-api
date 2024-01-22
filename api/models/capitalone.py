from __future__ import annotations

import csv
import datetime
import logging
import pathlib

from api import db
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

    @classmethod
    def print_choices(cls):
        models = cls.scalars(order_by="name")
        for a, b, c in zip(models[::3], models[1::3], models[2::3]):
            print(f"{a.name:<40}{b.name:<40}{c.name:<}")


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


# -----
# Views
# -----


class TransactionView(_CapitalOneBase):
    id = sa.Column(sa.Integer(), primary_key=True)
    date = sa.Column(sa.Date())
    post_date = sa.Column(sa.Date())
    card_number = sa.Column(sa.String(100))
    card_name = sa.Column(sa.String(100))
    merchant = sa.Column(sa.String(100))
    category = sa.Column(sa.String(100))
    transaction_type = sa.Column(sa.String(100))
    amount = sa.Column(sa.Numeric(8, 2))


class MerchantView(_CapitalOneBase):
    id = sa.Column(sa.Integer(), primary_key=True)
    merchant = sa.Column(sa.String(100))
    category = sa.Column(sa.String(100))


class TransactionCSVParser:
    @staticmethod
    def choose_category():
        while True:
            choice = input(f"Enter category (L to show all): ")
            if choice == "L":
                Category.print_choices()

            elif (category := Category.scalar_one_or_none(name=choice)) is not None:
                return category.id

            else:
                print(f"{choice!r} not found. Try again")

    @staticmethod
    def choose_merchant():
        while True:
            choice = input("Enter Merchant (L to show all, N to create new): ")
            if choice == "L":
                Merchant.print_choices()

            elif choice == "N":
                merchant = Merchant(
                    name=input("Enter new Merchant name: "),
                    category_id=TransactionCSVParser.choose_category(),
                )
                db.session.add(merchant)
                db.session.flush()
                return merchant.id

            elif (merchant := Merchant.scalar_one_or_none(name=choice)) is not None:
                return merchant.id

            else:
                print(f"{choice!r} not found. Try again")

    @staticmethod
    def main(path: pathlib.Path):
        logging.info(f"Parsing {path!r}")

        with open(path, "r") as f:
            rows = [row for row in csv.DictReader(f)]

        for row in rows:
            card = Card.scalar_one(number=row["Card No."])

            if (description := Description.scalar_one_or_none(name=row["Description"])) is None:
                print(f"{row['Description']!r} has no matching <Description>")
                description = Description(
                    name=row["Description"],
                    merchant_id=TransactionCSVParser.choose_merchant(),
                )
                db.session.add(description)
                db.session.flush()

            transaction = Transaction(
                date=datetime.datetime.strptime(row["Transaction Date"], "%Y-%m-%d"),
                post_date=datetime.datetime.strptime(row["Posted Date"], "%Y-%m-%d"),
                card_id=card.id,
                description_id=description.id,
                transactiontype_id=TransactionType.DEBIT if row["Debit"] else TransactionType.CREDIT,
                amount=row["Debit"] or row["Credit"],
            )

            db.session.add(transaction)
        db.session.commit()

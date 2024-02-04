"""Add CapitalOne tables

Revision ID: e8f575cde460
Revises: a90b354062ba
Create Date: 2024-01-21 19:28:17.332881

"""
import csv
import datetime
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

from api.models.capitalone import Card
from api.models.capitalone import Category
from api.models.capitalone import Description
from api.models.capitalone import Merchant
from api.models.capitalone import Transaction
from api.models.capitalone import TransactionType

# revision identifiers, used by Alembic.
revision: str = "e8f575cde460"
down_revision: Union[str, None] = "a90b354062ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def _upgrade_schema() -> None:
    op.execute("create schema capitalone")

    op.create_table(
        "card_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("number", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_card_")),
        sa.UniqueConstraint("name", name=op.f("uq_card__name")),
        sa.UniqueConstraint("number", name=op.f("uq_card__number")),
        schema="capitalone",
    )

    op.create_table(
        "category_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_category_")),
        sa.UniqueConstraint("name", name=op.f("uq_category__name")),
        schema="capitalone",
    )

    op.create_table(
        "merchant_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["capitalone.category_.id"],
            name=op.f("fk_merchant__category_id_category__id"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_merchant_")),
        sa.UniqueConstraint("name", name=op.f("uq_merchant__name")),
        schema="capitalone",
    )

    op.create_table(
        "description_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("merchant_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["merchant_id"],
            ["capitalone.merchant_.id"],
            name=op.f("fk_description__merchant_id_merchant__id"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_description_")),
        sa.UniqueConstraint("name", name=op.f("uq_description__name")),
        schema="capitalone",
    )

    op.create_table(
        "transaction_type_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_transaction_type_")),
        sa.UniqueConstraint("name", name=op.f("uq_transaction_type__name")),
        schema="capitalone",
    )

    op.create_table(
        "transaction_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("post_date", sa.Date(), nullable=False),
        sa.Column("card_id", sa.Integer(), nullable=False),
        sa.Column("description_id", sa.Integer(), nullable=False),
        sa.Column("transactiontype_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=8, scale=2), nullable=False),
        sa.ForeignKeyConstraint(
            ["card_id"],
            ["capitalone.card_.id"],
            name=op.f("fk_transaction__card_id_card__id"),
        ),
        sa.ForeignKeyConstraint(
            ["description_id"],
            ["capitalone.description_.id"],
            name=op.f("fk_transaction__description_id_description__id"),
        ),
        sa.ForeignKeyConstraint(
            ["transactiontype_id"],
            ["capitalone.transaction_.id"],
            name=op.f("fk_transaction__transactiontype_id_transaction_type__id"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_transaction_")),
        schema="capitalone",
    )


def _sync_sequence(table: str):
    op.execute(f"select setval(pg_get_serial_sequence('{table}', 'id'), (select max(id) from {table}))")


def _sync_sequences():
    _sync_sequence("capitalone.card_")
    _sync_sequence("capitalone.category_")
    _sync_sequence("capitalone.merchant_")
    _sync_sequence("capitalone.description_")


def _upgrade_dev_prod_data() -> None:
    with open("./migrations/data/Card.csv", "r") as f:
        op.bulk_insert(Card.__table__, [row for row in csv.DictReader(f)])

    with open("./migrations/data/Category.csv", "r") as f:
        op.bulk_insert(Category.__table__, [row for row in csv.DictReader(f)])

    with open("./migrations/data/Merchant.csv", "r") as f:
        op.bulk_insert(Merchant.__table__, [row for row in csv.DictReader(f)])

    with open("./migrations/data/Description.csv", "r") as f:
        op.bulk_insert(Description.__table__, [row for row in csv.DictReader(f)])


def _upgrade_test_data() -> None:
    op.bulk_insert(
        Card.__table__,
        [
            {"id": 1, "number": "1234", "name": "Foo"},
            {"id": 2, "number": "5678", "name": "Bar"},
        ],
    )

    op.bulk_insert(
        Category.__table__,
        [
            {"id": 1, "name": "Dining"},
            {"id": 2, "name": "Entertainment"},
            {"id": 3, "name": "Utilities"},
            {"id": 4, "name": "Payment"},
        ],
    )

    op.bulk_insert(
        Merchant.__table__,
        [
            {"id": 1, "name": "Lindys", "category_id": 1},
            {"id": 2, "name": "AMC", "category_id": 2},
            {"id": 3, "name": "Eversource", "category_id": 3},
            {"id": 4, "name": "Bank", "category_id": 4},
        ],
    )

    op.bulk_insert(
        Description.__table__,
        [
            {"id": 1, "name": "TST LINDYS DINER   KEENE", "merchant_id": 1},
            {"id": 2, "name": "TST LINDYS DINER   GROTON", "merchant_id": 1},
            {"id": 3, "name": "**SQ AMC Cinemas", "merchant_id": 2},
            {"id": 4, "name": "Eversource Utilities", "merchant_id": 3},
            {"id": 5, "name": "Eversource Electric", "merchant_id": 3},
            {"id": 6, "name": "Online Payment for XXXXX", "merchant_id": 4},
        ],
    )

    op.bulk_insert(
        Transaction.__table__,
        [
            {
                "date": datetime.date(2020, 5, 18),
                "post_date": datetime.date(2020, 5, 18),
                "card_id": 1,
                "description_id": 1,
                "transactiontype_id": TransactionType.DEBIT,
                "amount": 58.92,
            },
            {
                "date": datetime.date(2021, 2, 12),
                "post_date": datetime.date(2021, 2, 13),
                "card_id": 2,
                "description_id": 3,
                "transactiontype_id": TransactionType.DEBIT,
                "amount": 101.47,
            },
            {
                "date": datetime.date(1997, 1, 1),
                "post_date": datetime.date(1997, 1, 2),
                "card_id": 2,
                "description_id": 6,
                "transactiontype_id": TransactionType.CREDIT,
                "amount": 1356.83,
            },
        ],
    )


def _upgrade_data() -> None:
    op.bulk_insert(
        TransactionType.__table__,
        [
            {"id": TransactionType.DEBIT, "name": "Debit"},
            {"id": TransactionType.CREDIT, "name": "Credit"},
        ],
    )


def _upgrade() -> None:
    _upgrade_schema()
    _upgrade_data()


def _downgrade() -> None:
    op.drop_table("transaction_", schema="capitalone")
    op.drop_table("transaction_type_", schema="capitalone")
    op.drop_table("description_", schema="capitalone")
    op.drop_table("merchant_", schema="capitalone")
    op.drop_table("category_", schema="capitalone")
    op.drop_table("card_", schema="capitalone")

    op.execute("drop schema capitalone")


def upgrade_dev() -> None:
    _upgrade()
    _upgrade_dev_prod_data()
    _sync_sequences()


def downgrade_dev() -> None:
    _downgrade()


def upgrade_test() -> None:
    _upgrade()
    _upgrade_test_data()
    _sync_sequences()


def downgrade_test() -> None:
    _downgrade()


def upgrade_prod() -> None:
    _upgrade()
    _upgrade_dev_prod_data()
    _sync_sequences()


def downgrade_prod() -> None:
    _downgrade()

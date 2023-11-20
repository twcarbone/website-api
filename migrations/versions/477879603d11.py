"""Grocery

Revision ID: 477879603d11
Revises: 01699e6d9ad6
Create Date: 2023-11-20 16:28:04.294687

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

from api.models.grocery import ShopriteRateType

# revision identifiers, used by Alembic.
revision: str = "477879603d11"
down_revision: Union[str, None] = "01699e6d9ad6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def _upgrade_schema() -> None:
    op.execute("create schema grocery")

    op.create_table(
        "shoprite_order_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_shoprite_order_")),
        sa.UniqueConstraint("date", name=op.f("uq_shoprite_order__date")),
        schema="grocery",
    )

    op.create_table(
        "shoprite_product_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_shoprite_product_")),
        sa.UniqueConstraint("code", name=op.f("uq_shoprite_product__code")),
        schema="grocery",
    )

    op.create_table(
        "shoprite_rate_type_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rate", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_shoprite_rate_type_")),
        sa.UniqueConstraint("rate", name=op.f("uq_shoprite_rate_type__rate")),
        schema="grocery",
    )

    op.create_table(
        "shoprite_product_detail_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("shopriteproduct_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=False),
        sa.Column("brand", sa.String(length=500), nullable=False),
        sa.Column("sku", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(
            ["shopriteproduct_id"],
            ["grocery.shoprite_product_.id"],
            name=op.f("fk_shoprite_product_detail__shopriteproduct_id_shoprite_product__id"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_shoprite_product_detail_")),
        sa.UniqueConstraint("shopriteproduct_id", name=op.f("uq_shoprite_product_detail__shopriteproduct_id")),
        sa.UniqueConstraint("sku", name=op.f("uq_shoprite_product_detail__sku")),
        schema="grocery",
    )

    op.create_table(
        "shoprite_transaction_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("shopriteorder_id", sa.Integer(), nullable=False),
        sa.Column("shopriteproduct_id", sa.Integer(), nullable=False),
        sa.Column("shopriteratetype_id", sa.Integer(), nullable=False),
        sa.Column("rate", sa.Numeric(precision=8, scale=2), nullable=False),
        sa.Column("qty", sa.Numeric(precision=8, scale=2), nullable=False),
        sa.Column("final", sa.Numeric(precision=8, scale=2), nullable=False),
        sa.ForeignKeyConstraint(
            ["shopriteorder_id"],
            ["grocery.shoprite_order_.id"],
            name=op.f("fk_shoprite_transaction__shopriteorder_id_shoprite_order__id"),
        ),
        sa.ForeignKeyConstraint(
            ["shopriteproduct_id"],
            ["grocery.shoprite_product_.id"],
            name=op.f("fk_shoprite_transaction__shopriteproduct_id_shoprite_product__id"),
        ),
        sa.ForeignKeyConstraint(
            ["shopriteratetype_id"],
            ["grocery.shoprite_rate_type_.id"],
            name=op.f("fk_shoprite_transaction__shopriteratetype_id_shoprite_rate_type__id"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_shoprite_transaction_")),
        schema="grocery",
    )

    op.create_table(
        "shoprite_discount_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("shopritetransaction_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=8, scale=2), nullable=False),
        sa.ForeignKeyConstraint(
            ["shopritetransaction_id"],
            ["grocery.shoprite_transaction_.id"],
            name=op.f("fk_shoprite_discount__shopritetransaction_id_shoprite_transaction__id"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_shoprite_discount_")),
        schema="grocery",
    )


def _upgrade_data() -> None:
    op.bulk_insert(
        ShopriteRateType.__table__,
        [
            {"id": ShopriteRateType.PER_LB, "rate": "PER_LB"},
            {"id": ShopriteRateType.PER_QTY, "rate": "PER_QTY"},
        ],
    )


def _upgrade() -> None:
    _upgrade_schema()
    _upgrade_data()


def _downgrade() -> None:
    op.drop_table("shoprite_discount_", schema="grocery")
    op.drop_table("shoprite_transaction_", schema="grocery")
    op.drop_table("shoprite_product_detail_", schema="grocery")
    op.drop_table("shoprite_rate_type_", schema="grocery")
    op.drop_table("shoprite_product_", schema="grocery")
    op.drop_table("shoprite_order_", schema="grocery")

    op.execute("drop schema grocery")


def upgrade_dev() -> None:
    _upgrade()


def downgrade_dev() -> None:
    _downgrade()


def upgrade_test() -> None:
    _upgrade()


def downgrade_test() -> None:
    _downgrade()


def upgrade_prod() -> None:
    _upgrade()


def downgrade_prod() -> None:
    _downgrade()

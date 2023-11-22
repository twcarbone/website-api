"""Grocery views

Revision ID: a90b354062ba
Revises: 477879603d11
Create Date: 2023-11-21 16:53:10.630953

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a90b354062ba"
down_revision: Union[str, None] = "477879603d11"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def _upgrade() -> None:
    op.execute(
        """
        create view grocery.product_view_ as
            select
                sp.id as id,
                spd.sku as sku,
                sp.name as short_name,
                spd.name as long_name,
                spd.brand as brand,
                spd.description as description
            from
                grocery.shoprite_product_ sp
                left outer join grocery.shoprite_product_detail_ spd on spd.shopriteproduct_id = sp.id
        """
    )

    op.execute(
        """
        create view grocery.order_view_ as
            select
                so.id as id,
                so.date as date,
                sum(st.final) as order_total
            from
                grocery.shoprite_order_ so
                join grocery.shoprite_transaction_ st on st.shopriteorder_id = so.id
            group by
                so.id
        """
    )

    op.execute(
        """
        create view grocery.transaction_view_ as
            select
                st.id as id,
                so.date as date,
                spd.sku as sku,
                sp.name as short_name,
                spd.name as long_name,
                st.rate as rate,
                srt.rate as rate_type,
                st.qty as qty,
                sd.amount as discount,
                st.final as final
            from
                grocery.shoprite_transaction_ st
                join grocery.shoprite_order_ so on st.shopriteorder_id = so.id
                join grocery.shoprite_product_ sp on st.shopriteproduct_id = sp.id
                join grocery.shoprite_rate_type_ srt on st.shopriteratetype_id = srt.id
                left outer join grocery.shoprite_discount_ sd on sd.shopritetransaction_id = st.id
                left outer join grocery.shoprite_product_detail_ spd on spd.shopriteproduct_id = sp.id
        """
    )


def _downgrade() -> None:
    op.execute("drop view grocery.product_view_")
    op.execute("drop view grocery.order_view_")
    op.execute("drop view grocery.transaction_view_")


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

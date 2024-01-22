"""CapitalOne views

Revision ID: 30dc36a9c3bb
Revises: f8288857573d
Create Date: 2024-01-21 23:20:10.453701

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "30dc36a9c3bb"
down_revision: Union[str, None] = "e8f575cde460"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def _upgrade_schema() -> None:
    op.execute(
        """
        create view capitalone.transaction_view_ as 
            select
                t.id as id,
                t.date as date,
                t.post_date post_date,
                cd.number as card_number,
                cd.name as card_name,
                m.name as merchant,
                cy.name as category,
                tt.name as transaction_type,
                t.amount as amount
            from
                capitalone.transaction_ t
                join capitalone.card_ cd on t.card_id = cd.id
                join capitalone.description_ d on t.description_id = d.id
                join capitalone.merchant_ m on d.merchant_id = m.id
                join capitalone.category_ cy on m.category_id = cy.id
                join capitalone.transaction_type_ tt on t.transactiontype_id = tt.id
        """
    )

    op.execute(
        """
        create view capitalone.merchant_view_ as
            select
                m.id,
                m.name as merchant,
                c.name as category
            from
                capitalone.merchant_ m
                join capitalone.category_ c on m.category_id = c.id
        """
    )


def _upgrade_data() -> None:
    pass


def _upgrade() -> None:
    _upgrade_schema()
    _upgrade_data()


def _downgrade() -> None:
    op.execute("drop view capitalone.transaction_view_")
    op.execute("drop view capitalone.merchant_view_")


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

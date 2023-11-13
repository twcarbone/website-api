"""Ready. Set. Go!

Revision ID: 4989fd6f0104
Revises: 
Create Date: 2023-11-13 13:15:07.141664

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4989fd6f0104"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def _upgrade() -> None:
    op.create_table(
        "user_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("pwhash", sa.LargeBinary(length=60), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_")),
        sa.UniqueConstraint("email", name=op.f("uq_user__email")),
    )


def _downgrade() -> None:
    op.drop_table("user_")


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

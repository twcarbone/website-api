"""Scientific units

Revision ID: 01699e6d9ad6
Revises: afd282324e02
Create Date: 2023-11-16 13:48:23.502676

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

from api.models.engdata import PipeSize
from api.models.engdata import PipeThkns
from api.models.engdata import Unit

# revision identifiers, used by Alembic.
revision: str = "01699e6d9ad6"
down_revision: Union[str, None] = "afd282324e02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def _upgrade_schema_pre_data() -> None:
    # Create table 'unit_'
    op.create_table(
        "unit_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("short_name", sa.String(length=20), nullable=False),
        sa.Column("long_name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_unit_")),
        sa.UniqueConstraint("long_name", name=op.f("uq_unit__long_name")),
        sa.UniqueConstraint("short_name", name=op.f("uq_unit__short_name")),
    )

    # Add column 'outer_dia_unit_id' to table 'pipe_size_'
    op.add_column("pipe_size_", sa.Column("outer_dia_unit_id", sa.Integer()))
    op.create_foreign_key(
        op.f("fk_pipe_size__outer_dia_unit_id_unit__id"),
        "pipe_size_",
        "unit_",
        ["outer_dia_unit_id"],
        ["id"],
    )

    # Add column 'thkns_unit_id' to table 'pipe_thkns_'
    op.add_column("pipe_thkns_", sa.Column("thkns_unit_id", sa.Integer()))
    op.create_foreign_key(
        op.f("fk_pipe_thkns__thkns_unit_id_unit__id"),
        "pipe_thkns_",
        "unit_",
        ["thkns_unit_id"],
        ["id"],
    )


def _upgrade_schema_post_data() -> None:
    # Make new table columns non-nullable
    op.alter_column("pipe_size_", "outer_dia_unit_id", nullable=False)
    op.alter_column("pipe_thkns_", "thkns_unit_id", nullable=False)


def _upgrade_data() -> None:
    op.bulk_insert(
        Unit.__table__,
        [
            {"id": 1, "short_name": "in", "long_name": "inch"},
            {"id": 2, "short_name": "g", "long_name": "gram"},
            {"id": 3, "short_name": "mol", "long_name": "mol"},
            {"id": 4, "short_name": "kg", "long_name": "kilogram"},
            {"id": 5, "short_name": "J", "long_name": "joule"},
            {"id": 6, "short_name": "kJ", "long_name": "kilojoules"},
            {"id": 7, "short_name": "degF", "long_name": "degrees fahrenheit"},
            {"id": 8, "short_name": "degC", "long_name": "degrees celcius"},
            {"id": 9, "short_name": "K", "long_name": "kelvin"},
            {"id": 10, "short_name": "degR", "long_name": "degrees rankine"},
        ],
    )

    op.execute(sa.update(PipeSize.__table__).values(outer_dia_unit_id=1))
    op.execute(sa.update(PipeThkns.__table__).values(thkns_unit_id=1))


def _upgrade() -> None:
    _upgrade_schema_pre_data()
    _upgrade_data()
    _upgrade_schema_post_data()


def _downgrade() -> None:
    op.drop_constraint(op.f("fk_pipe_size__outer_dia_unit_id_unit__id"), "pipe_size_", type_="foreignkey")
    op.drop_column("pipe_size_", "outer_dia_unit_id")

    op.drop_constraint(op.f("fk_pipe_thkns__thkns_unit_id_unit__id"), "pipe_thkns_", type_="foreignkey")
    op.drop_column("pipe_thkns_", "thkns_unit_id")

    op.drop_table("unit_")


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

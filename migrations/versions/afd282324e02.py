"""Pipe data

Revision ID: afd282324e02
Revises: 4989fd6f0104
Create Date: 2023-11-15 13:08:35.538259

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

from api.models.engdata import PipeSch
from api.models.engdata import PipeSize
from api.models.engdata import PipeThkns

# revision identifiers, used by Alembic.
revision: str = "afd282324e02"
down_revision: Union[str, None] = "4989fd6f0104"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


def _upgrade_schema() -> None:
    op.create_table(
        "pipe_sch_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sch", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_pipe_sch_")),
    )

    op.create_table(
        "pipe_size_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nps", sa.String(length=20), nullable=False),
        sa.Column("outer_dia", sa.Numeric(precision=6, scale=3), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_pipe_size_")),
        sa.UniqueConstraint("nps", name=op.f("uq_pipe_size__nps")),
    )

    op.create_table(
        "pipe_thkns_",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipesize_id", sa.Integer(), nullable=False),
        sa.Column("pipesch_id", sa.Integer(), nullable=False),
        sa.Column("thkns", sa.Numeric(precision=6, scale=3), nullable=False),
        sa.ForeignKeyConstraint(
            ["pipesch_id"],
            ["pipe_sch_.id"],
            name=op.f("fk_pipe_thkns__pipesch_id_pipe_sch__id"),
        ),
        sa.ForeignKeyConstraint(
            ["pipesize_id"],
            ["pipe_size_.id"],
            name=op.f("fk_pipe_thkns__pipesize_id_pipe_size__id"),
        ),
        sa.PrimaryKeyConstraint("pipesize_id", "pipesch_id", "id", name=op.f("pk_pipe_thkns_")),
    )


def _upgrade_data() -> None:
    op.bulk_insert(
        PipeSize.__table__,
        [
            {"id": 1, "nps": "0.125", "outer_dia": 0.405},
            {"id": 2, "nps": "0.250", "outer_dia": 0.54},
            {"id": 3, "nps": "0.375", "outer_dia": 0.675},
            {"id": 4, "nps": "0.500", "outer_dia": 0.84},
            {"id": 5, "nps": "0.750", "outer_dia": 1.05},
            {"id": 6, "nps": "1.000", "outer_dia": 1.315},
            {"id": 7, "nps": "1.250", "outer_dia": 1.66},
            {"id": 8, "nps": "1.500", "outer_dia": 1.9},
            {"id": 9, "nps": "2.000", "outer_dia": 2.375},
            {"id": 10, "nps": "2.500", "outer_dia": 2.875},
            {"id": 11, "nps": "3.000", "outer_dia": 3.5},
            {"id": 12, "nps": "3.500", "outer_dia": 4},
            {"id": 13, "nps": "4.000", "outer_dia": 4.5},
            {"id": 14, "nps": "5.000", "outer_dia": 5.563},
            {"id": 15, "nps": "6.000", "outer_dia": 6.625},
            {"id": 16, "nps": "8.000", "outer_dia": 8.625},
            {"id": 17, "nps": "10.000", "outer_dia": 10.75},
            {"id": 18, "nps": "12.000", "outer_dia": 12.75},
            {"id": 19, "nps": "14.000", "outer_dia": 14},
            {"id": 20, "nps": "16.000", "outer_dia": 16},
            {"id": 21, "nps": "18.000", "outer_dia": 18},
            {"id": 22, "nps": "20.000", "outer_dia": 20},
            {"id": 23, "nps": "22.000", "outer_dia": 22},
            {"id": 24, "nps": "24.000", "outer_dia": 24},
            {"id": 25, "nps": "30.000", "outer_dia": 30},
            {"id": 26, "nps": "32.000", "outer_dia": 32},
            {"id": 27, "nps": "34.000", "outer_dia": 34},
            {"id": 28, "nps": "36.000", "outer_dia": 36},
            {"id": 29, "nps": "42.000", "outer_dia": 42},
        ],
    )

    op.bulk_insert(
        PipeSch.__table__,
        [
            {"id": 1, "sch": "10"},
            {"id": 2, "sch": "20"},
            {"id": 3, "sch": "30"},
            {"id": 4, "sch": "STD"},
            {"id": 5, "sch": "40"},
            {"id": 6, "sch": "60"},
            {"id": 7, "sch": "XS"},
            {"id": 8, "sch": "80"},
            {"id": 9, "sch": "100"},
            {"id": 10, "sch": "120"},
            {"id": 11, "sch": "140"},
            {"id": 12, "sch": "160"},
            {"id": 13, "sch": "XXS"},
        ],
    )

    op.bulk_insert(
        PipeThkns.__table__,
        [
            {"id": 1, "pipesize_id": 19, "pipesch_id": 1, "thkns": 0.25},
            {"id": 2, "pipesize_id": 20, "pipesch_id": 1, "thkns": 0.25},
            {"id": 3, "pipesize_id": 21, "pipesch_id": 1, "thkns": 0.25},
            {"id": 4, "pipesize_id": 22, "pipesch_id": 1, "thkns": 0.25},
            {"id": 5, "pipesize_id": 23, "pipesch_id": 1, "thkns": 0.25},
            {"id": 6, "pipesize_id": 24, "pipesch_id": 1, "thkns": 0.25},
            {"id": 7, "pipesize_id": 25, "pipesch_id": 1, "thkns": 0.312},
            {"id": 8, "pipesize_id": 26, "pipesch_id": 1, "thkns": 0.312},
            {"id": 9, "pipesize_id": 27, "pipesch_id": 1, "thkns": 0.312},
            {"id": 10, "pipesize_id": 28, "pipesch_id": 1, "thkns": 0.312},
            {"id": 11, "pipesize_id": 16, "pipesch_id": 2, "thkns": 0.25},
            {"id": 12, "pipesize_id": 17, "pipesch_id": 2, "thkns": 0.25},
            {"id": 13, "pipesize_id": 18, "pipesch_id": 2, "thkns": 0.25},
            {"id": 14, "pipesize_id": 19, "pipesch_id": 2, "thkns": 0.312},
            {"id": 15, "pipesize_id": 20, "pipesch_id": 2, "thkns": 0.312},
            {"id": 16, "pipesize_id": 21, "pipesch_id": 2, "thkns": 0.312},
            {"id": 17, "pipesize_id": 22, "pipesch_id": 2, "thkns": 0.375},
            {"id": 18, "pipesize_id": 23, "pipesch_id": 2, "thkns": 0.375},
            {"id": 19, "pipesize_id": 24, "pipesch_id": 2, "thkns": 0.375},
            {"id": 20, "pipesize_id": 25, "pipesch_id": 2, "thkns": 0.5},
            {"id": 21, "pipesize_id": 26, "pipesch_id": 2, "thkns": 0.5},
            {"id": 22, "pipesize_id": 27, "pipesch_id": 2, "thkns": 0.5},
            {"id": 23, "pipesize_id": 28, "pipesch_id": 2, "thkns": 0.5},
            {"id": 24, "pipesize_id": 29, "pipesch_id": 2, "thkns": 0.5},
            {"id": 25, "pipesize_id": 16, "pipesch_id": 3, "thkns": 0.277},
            {"id": 26, "pipesize_id": 17, "pipesch_id": 3, "thkns": 0.307},
            {"id": 27, "pipesize_id": 18, "pipesch_id": 3, "thkns": 0.33},
            {"id": 28, "pipesize_id": 19, "pipesch_id": 3, "thkns": 0.375},
            {"id": 29, "pipesize_id": 20, "pipesch_id": 3, "thkns": 0.375},
            {"id": 30, "pipesize_id": 21, "pipesch_id": 3, "thkns": 0.438},
            {"id": 31, "pipesize_id": 22, "pipesch_id": 3, "thkns": 0.5},
            {"id": 32, "pipesize_id": 23, "pipesch_id": 3, "thkns": 0.5},
            {"id": 33, "pipesize_id": 24, "pipesch_id": 3, "thkns": 0.562},
            {"id": 34, "pipesize_id": 25, "pipesch_id": 3, "thkns": 0.625},
            {"id": 35, "pipesize_id": 26, "pipesch_id": 3, "thkns": 0.625},
            {"id": 36, "pipesize_id": 27, "pipesch_id": 3, "thkns": 0.625},
            {"id": 37, "pipesize_id": 28, "pipesch_id": 3, "thkns": 0.625},
            {"id": 38, "pipesize_id": 29, "pipesch_id": 3, "thkns": 0.625},
            {"id": 39, "pipesize_id": 1, "pipesch_id": 4, "thkns": 0.068},
            {"id": 40, "pipesize_id": 2, "pipesch_id": 4, "thkns": 0.088},
            {"id": 41, "pipesize_id": 3, "pipesch_id": 4, "thkns": 0.091},
            {"id": 42, "pipesize_id": 4, "pipesch_id": 4, "thkns": 0.109},
            {"id": 43, "pipesize_id": 5, "pipesch_id": 4, "thkns": 0.113},
            {"id": 44, "pipesize_id": 6, "pipesch_id": 4, "thkns": 0.133},
            {"id": 45, "pipesize_id": 7, "pipesch_id": 4, "thkns": 0.14},
            {"id": 46, "pipesize_id": 8, "pipesch_id": 4, "thkns": 0.145},
            {"id": 47, "pipesize_id": 9, "pipesch_id": 4, "thkns": 0.154},
            {"id": 48, "pipesize_id": 10, "pipesch_id": 4, "thkns": 0.203},
            {"id": 49, "pipesize_id": 11, "pipesch_id": 4, "thkns": 0.216},
            {"id": 50, "pipesize_id": 12, "pipesch_id": 4, "thkns": 0.226},
            {"id": 51, "pipesize_id": 13, "pipesch_id": 4, "thkns": 0.237},
            {"id": 52, "pipesize_id": 14, "pipesch_id": 4, "thkns": 0.258},
            {"id": 53, "pipesize_id": 15, "pipesch_id": 4, "thkns": 0.28},
            {"id": 54, "pipesize_id": 16, "pipesch_id": 4, "thkns": 0.322},
            {"id": 55, "pipesize_id": 17, "pipesch_id": 4, "thkns": 0.365},
            {"id": 56, "pipesize_id": 18, "pipesch_id": 4, "thkns": 0.375},
            {"id": 57, "pipesize_id": 19, "pipesch_id": 4, "thkns": 0.375},
            {"id": 58, "pipesize_id": 20, "pipesch_id": 4, "thkns": 0.375},
            {"id": 59, "pipesize_id": 21, "pipesch_id": 4, "thkns": 0.375},
            {"id": 60, "pipesize_id": 22, "pipesch_id": 4, "thkns": 0.375},
            {"id": 61, "pipesize_id": 23, "pipesch_id": 4, "thkns": 0.375},
            {"id": 62, "pipesize_id": 24, "pipesch_id": 4, "thkns": 0.375},
            {"id": 63, "pipesize_id": 25, "pipesch_id": 4, "thkns": 0.375},
            {"id": 64, "pipesize_id": 26, "pipesch_id": 4, "thkns": 0.375},
            {"id": 65, "pipesize_id": 27, "pipesch_id": 4, "thkns": 0.375},
            {"id": 66, "pipesize_id": 28, "pipesch_id": 4, "thkns": 0.375},
            {"id": 67, "pipesize_id": 29, "pipesch_id": 4, "thkns": 0.375},
            {"id": 68, "pipesize_id": 1, "pipesch_id": 5, "thkns": 0.068},
            {"id": 69, "pipesize_id": 2, "pipesch_id": 5, "thkns": 0.088},
            {"id": 70, "pipesize_id": 3, "pipesch_id": 5, "thkns": 0.091},
            {"id": 71, "pipesize_id": 4, "pipesch_id": 5, "thkns": 0.109},
            {"id": 72, "pipesize_id": 5, "pipesch_id": 5, "thkns": 0.113},
            {"id": 73, "pipesize_id": 6, "pipesch_id": 5, "thkns": 0.133},
            {"id": 74, "pipesize_id": 7, "pipesch_id": 5, "thkns": 0.14},
            {"id": 75, "pipesize_id": 8, "pipesch_id": 5, "thkns": 0.145},
            {"id": 76, "pipesize_id": 9, "pipesch_id": 5, "thkns": 0.154},
            {"id": 77, "pipesize_id": 10, "pipesch_id": 5, "thkns": 0.203},
            {"id": 78, "pipesize_id": 11, "pipesch_id": 5, "thkns": 0.216},
            {"id": 79, "pipesize_id": 12, "pipesch_id": 5, "thkns": 0.226},
            {"id": 80, "pipesize_id": 13, "pipesch_id": 5, "thkns": 0.237},
            {"id": 81, "pipesize_id": 14, "pipesch_id": 5, "thkns": 0.258},
            {"id": 82, "pipesize_id": 15, "pipesch_id": 5, "thkns": 0.28},
            {"id": 83, "pipesize_id": 16, "pipesch_id": 5, "thkns": 0.322},
            {"id": 84, "pipesize_id": 17, "pipesch_id": 5, "thkns": 0.365},
            {"id": 85, "pipesize_id": 18, "pipesch_id": 5, "thkns": 0.406},
            {"id": 86, "pipesize_id": 19, "pipesch_id": 5, "thkns": 0.438},
            {"id": 87, "pipesize_id": 20, "pipesch_id": 5, "thkns": 0.5},
            {"id": 88, "pipesize_id": 21, "pipesch_id": 5, "thkns": 0.562},
            {"id": 89, "pipesize_id": 22, "pipesch_id": 5, "thkns": 0.594},
            {"id": 90, "pipesize_id": 24, "pipesch_id": 5, "thkns": 0.688},
            {"id": 91, "pipesize_id": 26, "pipesch_id": 5, "thkns": 0.688},
            {"id": 92, "pipesize_id": 27, "pipesch_id": 5, "thkns": 0.688},
            {"id": 93, "pipesize_id": 28, "pipesch_id": 5, "thkns": 0.75},
            {"id": 94, "pipesize_id": 16, "pipesch_id": 6, "thkns": 0.406},
            {"id": 95, "pipesize_id": 17, "pipesch_id": 6, "thkns": 0.5},
            {"id": 96, "pipesize_id": 18, "pipesch_id": 6, "thkns": 0.562},
            {"id": 97, "pipesize_id": 19, "pipesch_id": 6, "thkns": 0.594},
            {"id": 98, "pipesize_id": 20, "pipesch_id": 6, "thkns": 0.656},
            {"id": 99, "pipesize_id": 21, "pipesch_id": 6, "thkns": 0.75},
            {"id": 100, "pipesize_id": 22, "pipesch_id": 6, "thkns": 0.812},
            {"id": 101, "pipesize_id": 23, "pipesch_id": 6, "thkns": 0.875},
            {"id": 102, "pipesize_id": 24, "pipesch_id": 6, "thkns": 0.969},
            {"id": 103, "pipesize_id": 1, "pipesch_id": 7, "thkns": 0.095},
            {"id": 104, "pipesize_id": 2, "pipesch_id": 7, "thkns": 0.119},
            {"id": 105, "pipesize_id": 3, "pipesch_id": 7, "thkns": 0.126},
            {"id": 106, "pipesize_id": 4, "pipesch_id": 7, "thkns": 0.147},
            {"id": 107, "pipesize_id": 5, "pipesch_id": 7, "thkns": 0.154},
            {"id": 108, "pipesize_id": 6, "pipesch_id": 7, "thkns": 0.179},
            {"id": 109, "pipesize_id": 7, "pipesch_id": 7, "thkns": 0.191},
            {"id": 110, "pipesize_id": 8, "pipesch_id": 7, "thkns": 0.2},
            {"id": 111, "pipesize_id": 9, "pipesch_id": 7, "thkns": 0.218},
            {"id": 112, "pipesize_id": 10, "pipesch_id": 7, "thkns": 0.276},
            {"id": 113, "pipesize_id": 11, "pipesch_id": 7, "thkns": 0.3},
            {"id": 114, "pipesize_id": 12, "pipesch_id": 7, "thkns": 0.318},
            {"id": 115, "pipesize_id": 13, "pipesch_id": 7, "thkns": 0.337},
            {"id": 116, "pipesize_id": 14, "pipesch_id": 7, "thkns": 0.375},
            {"id": 117, "pipesize_id": 15, "pipesch_id": 7, "thkns": 0.432},
            {"id": 118, "pipesize_id": 16, "pipesch_id": 7, "thkns": 0.5},
            {"id": 119, "pipesize_id": 17, "pipesch_id": 7, "thkns": 0.5},
            {"id": 120, "pipesize_id": 18, "pipesch_id": 7, "thkns": 0.5},
            {"id": 121, "pipesize_id": 19, "pipesch_id": 7, "thkns": 0.5},
            {"id": 122, "pipesize_id": 20, "pipesch_id": 7, "thkns": 0.5},
            {"id": 123, "pipesize_id": 21, "pipesch_id": 7, "thkns": 0.5},
            {"id": 124, "pipesize_id": 22, "pipesch_id": 7, "thkns": 0.5},
            {"id": 125, "pipesize_id": 23, "pipesch_id": 7, "thkns": 0.5},
            {"id": 126, "pipesize_id": 24, "pipesch_id": 7, "thkns": 0.5},
            {"id": 127, "pipesize_id": 25, "pipesch_id": 7, "thkns": 0.5},
            {"id": 128, "pipesize_id": 1, "pipesch_id": 8, "thkns": 0.095},
            {"id": 129, "pipesize_id": 2, "pipesch_id": 8, "thkns": 0.119},
            {"id": 130, "pipesize_id": 3, "pipesch_id": 8, "thkns": 0.126},
            {"id": 131, "pipesize_id": 4, "pipesch_id": 8, "thkns": 0.147},
            {"id": 132, "pipesize_id": 5, "pipesch_id": 8, "thkns": 0.154},
            {"id": 133, "pipesize_id": 6, "pipesch_id": 8, "thkns": 0.179},
            {"id": 134, "pipesize_id": 7, "pipesch_id": 8, "thkns": 0.191},
            {"id": 135, "pipesize_id": 8, "pipesch_id": 8, "thkns": 0.2},
            {"id": 136, "pipesize_id": 9, "pipesch_id": 8, "thkns": 0.218},
            {"id": 137, "pipesize_id": 10, "pipesch_id": 8, "thkns": 0.276},
            {"id": 138, "pipesize_id": 11, "pipesch_id": 8, "thkns": 0.3},
            {"id": 139, "pipesize_id": 12, "pipesch_id": 8, "thkns": 0.318},
            {"id": 140, "pipesize_id": 13, "pipesch_id": 8, "thkns": 0.337},
            {"id": 141, "pipesize_id": 14, "pipesch_id": 8, "thkns": 0.375},
            {"id": 142, "pipesize_id": 15, "pipesch_id": 8, "thkns": 0.432},
            {"id": 143, "pipesize_id": 16, "pipesch_id": 8, "thkns": 0.5},
            {"id": 144, "pipesize_id": 17, "pipesch_id": 8, "thkns": 0.594},
            {"id": 145, "pipesize_id": 18, "pipesch_id": 8, "thkns": 0.688},
            {"id": 146, "pipesize_id": 19, "pipesch_id": 8, "thkns": 0.75},
            {"id": 147, "pipesize_id": 20, "pipesch_id": 8, "thkns": 0.844},
            {"id": 148, "pipesize_id": 21, "pipesch_id": 8, "thkns": 0.938},
            {"id": 149, "pipesize_id": 22, "pipesch_id": 8, "thkns": 1.031},
            {"id": 150, "pipesize_id": 23, "pipesch_id": 8, "thkns": 1.125},
            {"id": 151, "pipesize_id": 24, "pipesch_id": 8, "thkns": 1.219},
            {"id": 152, "pipesize_id": 16, "pipesch_id": 9, "thkns": 0.594},
            {"id": 153, "pipesize_id": 17, "pipesch_id": 9, "thkns": 0.719},
            {"id": 154, "pipesize_id": 18, "pipesch_id": 9, "thkns": 0.844},
            {"id": 155, "pipesize_id": 19, "pipesch_id": 9, "thkns": 0.938},
            {"id": 156, "pipesize_id": 20, "pipesch_id": 9, "thkns": 1.031},
            {"id": 157, "pipesize_id": 21, "pipesch_id": 9, "thkns": 1.156},
            {"id": 158, "pipesize_id": 22, "pipesch_id": 9, "thkns": 1.281},
            {"id": 159, "pipesize_id": 23, "pipesch_id": 9, "thkns": 1.375},
            {"id": 160, "pipesize_id": 24, "pipesch_id": 9, "thkns": 1.531},
            {"id": 161, "pipesize_id": 13, "pipesch_id": 10, "thkns": 0.438},
            {"id": 162, "pipesize_id": 14, "pipesch_id": 10, "thkns": 0.5},
            {"id": 163, "pipesize_id": 15, "pipesch_id": 10, "thkns": 0.562},
            {"id": 164, "pipesize_id": 16, "pipesch_id": 10, "thkns": 0.719},
            {"id": 165, "pipesize_id": 17, "pipesch_id": 10, "thkns": 0.844},
            {"id": 166, "pipesize_id": 18, "pipesch_id": 10, "thkns": 1},
            {"id": 167, "pipesize_id": 19, "pipesch_id": 10, "thkns": 1.094},
            {"id": 168, "pipesize_id": 20, "pipesch_id": 10, "thkns": 1.219},
            {"id": 169, "pipesize_id": 21, "pipesch_id": 10, "thkns": 1.375},
            {"id": 170, "pipesize_id": 22, "pipesch_id": 10, "thkns": 1.5},
            {"id": 171, "pipesize_id": 23, "pipesch_id": 10, "thkns": 1.625},
            {"id": 172, "pipesize_id": 24, "pipesch_id": 10, "thkns": 1.812},
            {"id": 173, "pipesize_id": 16, "pipesch_id": 11, "thkns": 0.812},
            {"id": 174, "pipesize_id": 17, "pipesch_id": 11, "thkns": 1},
            {"id": 175, "pipesize_id": 18, "pipesch_id": 11, "thkns": 1.125},
            {"id": 176, "pipesize_id": 19, "pipesch_id": 11, "thkns": 1.25},
            {"id": 177, "pipesize_id": 20, "pipesch_id": 11, "thkns": 1.438},
            {"id": 178, "pipesize_id": 21, "pipesch_id": 11, "thkns": 1.562},
            {"id": 179, "pipesize_id": 22, "pipesch_id": 11, "thkns": 1.75},
            {"id": 180, "pipesize_id": 23, "pipesch_id": 11, "thkns": 1.875},
            {"id": 181, "pipesize_id": 24, "pipesch_id": 11, "thkns": 2.062},
            {"id": 182, "pipesize_id": 4, "pipesch_id": 12, "thkns": 0.187},
            {"id": 183, "pipesize_id": 5, "pipesch_id": 12, "thkns": 0.219},
            {"id": 184, "pipesize_id": 6, "pipesch_id": 12, "thkns": 0.25},
            {"id": 185, "pipesize_id": 7, "pipesch_id": 12, "thkns": 0.25},
            {"id": 186, "pipesize_id": 8, "pipesch_id": 12, "thkns": 0.281},
            {"id": 187, "pipesize_id": 9, "pipesch_id": 12, "thkns": 0.344},
            {"id": 188, "pipesize_id": 10, "pipesch_id": 12, "thkns": 0.375},
            {"id": 189, "pipesize_id": 11, "pipesch_id": 12, "thkns": 0.438},
            {"id": 190, "pipesize_id": 13, "pipesch_id": 12, "thkns": 0.531},
            {"id": 191, "pipesize_id": 14, "pipesch_id": 12, "thkns": 0.625},
            {"id": 192, "pipesize_id": 15, "pipesch_id": 12, "thkns": 0.719},
            {"id": 193, "pipesize_id": 16, "pipesch_id": 12, "thkns": 0.906},
            {"id": 194, "pipesize_id": 17, "pipesch_id": 12, "thkns": 1.125},
            {"id": 195, "pipesize_id": 18, "pipesch_id": 12, "thkns": 1.312},
            {"id": 196, "pipesize_id": 19, "pipesch_id": 12, "thkns": 1.406},
            {"id": 197, "pipesize_id": 20, "pipesch_id": 12, "thkns": 1.594},
            {"id": 198, "pipesize_id": 21, "pipesch_id": 12, "thkns": 1.781},
            {"id": 199, "pipesize_id": 22, "pipesch_id": 12, "thkns": 1.969},
            {"id": 200, "pipesize_id": 23, "pipesch_id": 12, "thkns": 2.125},
            {"id": 201, "pipesize_id": 24, "pipesch_id": 12, "thkns": 2.344},
            {"id": 202, "pipesize_id": 4, "pipesch_id": 13, "thkns": 0.294},
            {"id": 203, "pipesize_id": 5, "pipesch_id": 13, "thkns": 0.308},
            {"id": 204, "pipesize_id": 6, "pipesch_id": 13, "thkns": 0.358},
            {"id": 205, "pipesize_id": 7, "pipesch_id": 13, "thkns": 0.382},
            {"id": 206, "pipesize_id": 8, "pipesch_id": 13, "thkns": 0.4},
            {"id": 207, "pipesize_id": 9, "pipesch_id": 13, "thkns": 0.436},
            {"id": 208, "pipesize_id": 10, "pipesch_id": 13, "thkns": 0.552},
            {"id": 209, "pipesize_id": 11, "pipesch_id": 13, "thkns": 0.6},
            {"id": 210, "pipesize_id": 13, "pipesch_id": 13, "thkns": 0.674},
            {"id": 211, "pipesize_id": 14, "pipesch_id": 13, "thkns": 0.75},
            {"id": 212, "pipesize_id": 15, "pipesch_id": 13, "thkns": 0.864},
            {"id": 213, "pipesize_id": 16, "pipesch_id": 13, "thkns": 0.875},
            {"id": 214, "pipesize_id": 17, "pipesch_id": 13, "thkns": 1},
            {"id": 215, "pipesize_id": 18, "pipesch_id": 13, "thkns": 1},
        ],
    )


def _upgrade() -> None:
    _upgrade_schema()
    _upgrade_data()


def _downgrade() -> None:
    op.drop_table("pipe_thkns_")
    op.drop_table("pipe_size_")
    op.drop_table("pipe_sch_")


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

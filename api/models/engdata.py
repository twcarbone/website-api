from __future__ import annotations

import decimal

from api import db
from api.models import Base
from api.models import exc
from api.models import hybrid
from api.models import num_6_3
from api.models import orm
from api.models import sa
from api.models import str_20
from api.models import str_100
from api.models.quantity import HasQuantityColumn
from api.models.quantity import QuantityColumn


class Unit(Base):
    """
    Scientific Units.
    """

    short_name: orm.Mapped[str_20] = orm.mapped_column(unique=True)
    long_name: orm.Mapped[str_100] = orm.mapped_column(unique=True)


class PipeSize(HasQuantityColumn, Base):
    """
    Nominal pipe size and OD in accordance with ANSI B36.10.
    """

    nps: orm.Mapped[str_20] = orm.mapped_column(unique=True)
    outer_dia = QuantityColumn("in", sa.Column(sa.Numeric(6, 3), nullable=False))
    outer_dia_unit_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(Unit.id))

    _outer_dia_unit: orm.Mapped["Unit"] = orm.relationship()
    _pipethnkss: orm.Mapped[list["PipeThkns"]] = orm.relationship(back_populates="_pipesize")

    @staticmethod
    def inner_dia(nps: str, sch: str) -> decimal.Decimal:
        """
        Return calculated inner diameter for the given *nps* and *sch*.

        Raises `ValueError` for invalid *nps* or *sch*.
        """
        try:
            outer_dia, thkns = db.session.execute(
                db.select(PipeSize.outer_dia, PipeThkns.thkns)
                .join(PipeSize)
                .join(PipeSch)
                .where(PipeSize.nps.like(nps))
                .where(PipeSch.sch.like(sch))
            ).one()
        except exc.NoResultFound:
            raise ValueError("Invalid NPS or schedule")
        else:
            # TODO: (#9) Return as different units in PipeSize.inner_dia
            return outer_dia - 2 * thkns


class PipeSch(Base):
    """
    Pipe schedules in accordance with ANSI B36.10.
    """

    sch: orm.Mapped[str_100]

    _pipethnkss: orm.Mapped[list["PipeThkns"]] = orm.relationship(back_populates="_pipesch")


class PipeThkns(HasQuantityColumn, Base):
    """
    Pipe wall thickness for pipe NPS and schedule in accordance with ANSI B36.10.
    """

    pipesize_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(PipeSize.id), primary_key=True)
    pipesch_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(PipeSch.id), primary_key=True)
    thkns = QuantityColumn("in", sa.Column(sa.Numeric(6, 3), nullable=False))
    thkns_unit_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(Unit.id))

    _thkns_unit: orm.Mapped["Unit"] = orm.relationship()
    _pipesize: orm.Mapped["PipeSize"] = orm.relationship(back_populates="_pipethnkss")
    _pipesch: orm.Mapped["PipeSch"] = orm.relationship(back_populates="_pipethnkss")

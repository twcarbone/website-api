from __future__ import annotations

import decimal

from api import db
from api import ureg
from api.models import Base
from api.models import hybrid
from api.models import num_6_3
from api.models import orm
from api.models import sa
from api.models import str_20
from api.models import str_100


class Unit(Base):
    """
    Scientific Units.
    """

    short_name: orm.Mapped[str_20] = orm.mapped_column(unique=True)
    long_name: orm.Mapped[str_100] = orm.mapped_column(unique=True)


class PipeSize(Base):
    """
    Nominal pipe size and OD in accordance with ANSI B36.10.
    """

    nps: orm.Mapped[str_20] = orm.mapped_column(unique=True)
    _outer_dia: orm.Mapped[num_6_3] = orm.mapped_column("outer_dia")
    outer_dia_unit_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(Unit.id))

    _outer_dia_unit: orm.Mapped["Unit"] = orm.relationship()
    _pipethnkss: orm.Mapped[list["PipeThkns"]] = orm.relationship(back_populates="_pipesize")

    @hybrid.hybrid_property
    def outer_dia(self):
        return self._outer_dia * getattr(ureg, self._outer_dia_unit.short_name)

    @outer_dia.inplace.expression
    def outer_dia_expression(self):
        return self._outer_dia

    @outer_dia.inplace.setter
    def outer_dia_setter(self, outer_dia):
        try:
            if not outer_dia.check("[length]"):
                raise ValueError("Outer diameter must be a Quantity with dimensionality of [length]")
        except AttributeError:
            raise TypeError("Outer diameter must be a Quantity")

        self._outer_dia = outer_dia.to(getattr(ureg, self._outer_dia_unit.short_name))

    @staticmethod
    def inner_dia(nps: str, sch: str) -> decimal.Decimal:
        """
        Return calculated inner diameter for the given *nps* and *sch*.
        """
        outer_dia, thkns = db.session.execute(
            db.select(PipeSize.outer_dia, PipeThkns.thkns)
            .join(PipeSize)
            .join(PipeSch)
            .where(PipeSize.nps.like(nps))
            .where(PipeSch.sch.like(sch))
        ).one()
        return outer_dia - 2 * thkns


class PipeSch(Base):
    """
    Pipe schedules in accordance with ANSI B36.10.
    """

    sch: orm.Mapped[str_100]

    _pipethnkss: orm.Mapped[list["PipeThkns"]] = orm.relationship(back_populates="_pipesch")


class PipeThkns(Base):
    """
    Pipe wall thickness for pipe NPS and schedule in accordance with ANSI B36.10.
    """

    pipesize_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(PipeSize.id), primary_key=True)
    pipesch_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(PipeSch.id), primary_key=True)
    thkns: orm.Mapped[num_6_3]
    thkns_unit_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(Unit.id))

    _thkns_unit: orm.Mapped["Unit"] = orm.relationship()
    _pipesize: orm.Mapped["PipeSize"] = orm.relationship(back_populates="_pipethnkss")
    _pipesch: orm.Mapped["PipeSch"] = orm.relationship(back_populates="_pipethnkss")

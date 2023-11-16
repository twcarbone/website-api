from __future__ import annotations

import decimal

from api import db
from api.models import Base
from api.models import num_6_3
from api.models import orm
from api.models import sa
from api.models import str_20
from api.models import str_100


class PipeSize(Base):
    """
    Nominal pipe size and OD in accordance with ANSI B36.10.
    """

    nps: orm.Mapped[str_20] = orm.mapped_column(unique=True)
    outer_dia: orm.Mapped[num_6_3]

    _pipeschs: orm.Mapped[list["PipeThkns"]] = orm.relationship(back_populates="_pipesize")

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

    _pipesizes: orm.Mapped[list["PipeThkns"]] = orm.relationship(back_populates="_pipesch")


class PipeThkns(Base):
    """
    Pipe wall thickness for pipe NPS and schedule in accordance with ANSI B36.10.
    """

    pipesize_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(PipeSize.id), primary_key=True)
    pipesch_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(PipeSch.id), primary_key=True)
    thkns: orm.Mapped[num_6_3]

    _pipesize: orm.Mapped["PipeSize"] = orm.relationship(back_populates="_pipeschs")
    _pipesch: orm.Mapped["PipeSch"] = orm.relationship(back_populates="_pipesizes")

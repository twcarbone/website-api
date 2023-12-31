"""
Tests for models.
"""
import decimal
import re

import pytest

from api import db
from api import ureg
from api.models.engdata import PipeSize


class TestBase:
    def test_repr(self, _new_user, _pipesize):
        """
        GIVEN a model derived from Base
        WHEN __repr__ is called
        THEN check for correct representation
        """
        # fmt: off
        assert _new_user.__repr__() == "<User id=None, email='cheese@gmail.com'>"
        assert _pipesize.__repr__() == "<PipeSize id=10, nps='2.500', outer_dia_unit_id=1, outer_dia=<Quantity(2.875, 'inch')>>"
        # fmt: on

    def test_eq(self):
        """
        GIVEN a model derived from Base
        WHEN __eq__ is called
        THEN check for correct equality evaluation
        """
        # PipeSize
        pipesize1 = PipeSize(id=50, nps="100.000", outer_dia=120 * ureg.inch, outer_dia_unit_id=1)
        pipesize2 = PipeSize(id=50, nps="100.000", outer_dia=120 * ureg.inch, outer_dia_unit_id=1)
        pipesize3 = PipeSize(id=50, nps="100.000", outer_dia=121 * ureg.inch, outer_dia_unit_id=1)
        pipesize4 = PipeSize(id=50, nps="100.000", outer_dia=120 * ureg.mm, outer_dia_unit_id=1)
        pipesize5 = PipeSize(id=50, nps="100.000", outer_dia=120 * ureg.inch, outer_dia_unit_id=2)
        assert pipesize1 == pipesize2
        assert pipesize1 != pipesize3
        assert pipesize1 != pipesize4
        assert pipesize1 != pipesize5

    def test_serialize(self, _new_user, _pipesize):
        assert _pipesize.serialize() == {"id": 10, "nps": "2.500", "outer_dia": 2.875, "outer_dia_unit_id": 1}

    def test_serialize_sequence(self, _client):
        pipesize1 = db.session.get(PipeSize, 1)
        pipesize2 = db.session.get(PipeSize, 2)
        assert PipeSize.serialize_sequence([pipesize1, pipesize2]) == [
            {"id": 1, "nps": "0.125", "outer_dia": 0.405, "outer_dia_unit_id": 1},
            {"id": 2, "nps": "0.250", "outer_dia": 0.540, "outer_dia_unit_id": 1},
        ]


class TestUser:
    def test_init(self, _new_user):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check the email and pwhash fields are defined correctly
        """
        assert _new_user.email == "cheese@gmail.com"
        assert _new_user.pwhash != "my-favorite-bone"

    def test_chekpw(self, _new_user):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check that the configured password hashes to the stored database value
        """
        assert _new_user.checkpw("my-favorite-bone") == True


class TestPipeSize:
    def test_inner_dia(self, _client):
        assert PipeSize.inner_dia(nps="0.250", sch="XS") == decimal.Decimal("0.302")
        assert PipeSize.inner_dia(nps="2.500", sch="40") == decimal.Decimal("2.469")
        assert PipeSize.inner_dia(nps="10.000", sch="XXS") == decimal.Decimal("8.750")
        assert PipeSize.inner_dia(nps="24.000", sch="STD") == decimal.Decimal("23.25")

        with pytest.raises(ValueError, match="Invalid NPS or schedule"):
            assert PipeSize.inner_dia(nps="not-a-pipe-nps", sch="STD")
            assert PipeSize.inner_dia(nps="2.000", sch="not-a-schedule")
            assert PipeSize.inner_dia(nps="not-a-pipe-nps", sch="not-a-schedule")

    def test_quantity_column(self, _client):
        """
        GIVEN a SQLAlchemy mapper with a QuantityColumn
        WHEN the QuantityColumn is get, set, and queried
        THEN check to see that it works
        """
        pipesize = db.session.get(PipeSize, 1)

        assert pipesize._outer_dia == decimal.Decimal("0.405")
        assert pipesize.outer_dia == pipesize._outer_dia * ureg.inch

        with pytest.raises(TypeError, match="Must be a Quantity"):
            pipesize.outer_dia = 5

        with pytest.raises(ValueError, match=re.escape("Quantity must have dimensionality of [length]")):
            pipesize.outer_dia = 5 * ureg.gram

        pipesize.outer_dia = 1 * ureg.foot
        assert pipesize.outer_dia == pipesize._outer_dia * ureg.inch

"""
Tests for models.
"""
import decimal
import re

import pytest

from api import db
from api import ureg
from api.models.engdata import PipeSize


class TestUser:
    def test_init(self, _new_user):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check the email and pwhash fields are defined correctly
        """
        assert _new_user.email == "cheese@gmail.com"
        assert _new_user.pwhash != "my-favorite-bone"

    def test_repr(self, _new_user):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check __repr__ returns the correct representation
        """
        assert _new_user.__repr__() == "<User id=None, email='cheese@gmail.com'>"

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

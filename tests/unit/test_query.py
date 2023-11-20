"""
Tests for queries.
"""

import decimal

import pytest
from pint import Quantity

from api import db
from api.models import exc
from api.models.engdata import PipeSize


class TestQueryMixin:
    def test_pipesize_all(self, _client):
        # fmt: off
        assert PipeSize.all(column="nps") == [
            ("0.125",), ("0.250",), ("0.375",), ("0.500",), ("0.750",), ("1.000",),
            ("1.250",), ("1.500",), ("2.000",), ("2.500",), ("3.000",), ("3.500",),
            ("4.000",), ("5.000",), ("6.000",), ("8.000",), ("10.000",), ("12.000",),
            ("14.000",), ("16.000",), ("18.000",), ("20.000",), ("22.000",), ("24.000",),
            ("30.000",), ("32.000",), ("34.000",), ("36.000",), ("42.000",),
        ]
        # fmt: on

    def test_pipesize_scalars(self, _client):
        assert PipeSize.scalars() == [
            PipeSize(id=1, nps="0.125", outer_dia_unit_id=1, outer_dia=Quantity("0.405", "inch")),
            PipeSize(id=2, nps="0.250", outer_dia_unit_id=1, outer_dia=Quantity("0.540", "inch")),
            PipeSize(id=3, nps="0.375", outer_dia_unit_id=1, outer_dia=Quantity("0.675", "inch")),
            PipeSize(id=4, nps="0.500", outer_dia_unit_id=1, outer_dia=Quantity("0.840", "inch")),
            PipeSize(id=5, nps="0.750", outer_dia_unit_id=1, outer_dia=Quantity("1.050", "inch")),
            PipeSize(id=6, nps="1.000", outer_dia_unit_id=1, outer_dia=Quantity("1.315", "inch")),
            PipeSize(id=7, nps="1.250", outer_dia_unit_id=1, outer_dia=Quantity("1.660", "inch")),
            PipeSize(id=8, nps="1.500", outer_dia_unit_id=1, outer_dia=Quantity("1.900", "inch")),
            PipeSize(id=9, nps="2.000", outer_dia_unit_id=1, outer_dia=Quantity("2.375", "inch")),
            PipeSize(id=10, nps="2.500", outer_dia_unit_id=1, outer_dia=Quantity("2.875", "inch")),
            PipeSize(id=11, nps="3.000", outer_dia_unit_id=1, outer_dia=Quantity("3.500", "inch")),
            PipeSize(id=12, nps="3.500", outer_dia_unit_id=1, outer_dia=Quantity("4.000", "inch")),
            PipeSize(id=13, nps="4.000", outer_dia_unit_id=1, outer_dia=Quantity("4.500", "inch")),
            PipeSize(id=14, nps="5.000", outer_dia_unit_id=1, outer_dia=Quantity("5.563", "inch")),
            PipeSize(id=15, nps="6.000", outer_dia_unit_id=1, outer_dia=Quantity("6.625", "inch")),
            PipeSize(id=16, nps="8.000", outer_dia_unit_id=1, outer_dia=Quantity("8.625", "inch")),
            PipeSize(id=17, nps="10.000", outer_dia_unit_id=1, outer_dia=Quantity("10.750", "inch")),
            PipeSize(id=18, nps="12.000", outer_dia_unit_id=1, outer_dia=Quantity("12.750", "inch")),
            PipeSize(id=19, nps="14.000", outer_dia_unit_id=1, outer_dia=Quantity("14.000", "inch")),
            PipeSize(id=20, nps="16.000", outer_dia_unit_id=1, outer_dia=Quantity("16.000", "inch")),
            PipeSize(id=21, nps="18.000", outer_dia_unit_id=1, outer_dia=Quantity("18.000", "inch")),
            PipeSize(id=22, nps="20.000", outer_dia_unit_id=1, outer_dia=Quantity("20.000", "inch")),
            PipeSize(id=23, nps="22.000", outer_dia_unit_id=1, outer_dia=Quantity("22.000", "inch")),
            PipeSize(id=24, nps="24.000", outer_dia_unit_id=1, outer_dia=Quantity("24.000", "inch")),
            PipeSize(id=25, nps="30.000", outer_dia_unit_id=1, outer_dia=Quantity("30.000", "inch")),
            PipeSize(id=26, nps="32.000", outer_dia_unit_id=1, outer_dia=Quantity("32.000", "inch")),
            PipeSize(id=27, nps="34.000", outer_dia_unit_id=1, outer_dia=Quantity("34.000", "inch")),
            PipeSize(id=28, nps="36.000", outer_dia_unit_id=1, outer_dia=Quantity("36.000", "inch")),
            PipeSize(id=29, nps="42.000", outer_dia_unit_id=1, outer_dia=Quantity("42.000", "inch")),
        ]

        # fmt: off
        assert PipeSize.scalars(column="nps") == [
            "0.125", "0.250", "0.375", "0.500", "0.750", "1.000", "1.250", "1.500",
            "2.000", "2.500", "3.000", "3.500", "4.000", "5.000", "6.000", "8.000",
            "10.000", "12.000", "14.000", "16.000", "18.000", "20.000", "22.000",
            "24.000", "30.000", "32.000", "34.000", "36.000", "42.000",
        ]
        # fmt: on

        assert PipeSize.scalars(column="nps", id=21) == ["18.000"]
        assert PipeSize.scalars(column="outer_dia", id=21) == [decimal.Decimal("18.000")]

        # TODO: (#13) Add tests for 'QueryMixin' methods using 'order_by'

    def test_pipesize_scalar_one(self, _client):
        assert PipeSize.scalar_one(column="nps", id=1) == "0.125"

        with pytest.raises(exc.NoResultFound):
            assert PipeSize.scalar_one(id=999)

        with pytest.raises(exc.MultipleResultsFound):
            assert PipeSize.scalar_one()

    def test_pipesize_scalar_one_or_none(self, _client):
        assert PipeSize.scalar_one_or_none(column="nps", id=1) == "0.125"

        assert PipeSize.scalar_one_or_none(id=999) == None

        with pytest.raises(exc.MultipleResultsFound):
            assert PipeSize.scalar_one_or_none()

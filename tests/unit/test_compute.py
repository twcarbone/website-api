from decimal import Decimal

import api.engdata.compute as compute
from api import ureg


def test_specific_volume():
    rho = ureg.Quantity(Decimal("0.2"), "kg/m^3")

    sv = compute.specific_volume(ureg.Quantity(Decimal("0.2"), "kg/m^3"))
    assert sv.magnitude == Decimal("5")
    assert sv.units == ureg.meter**3 / ureg.kg

    sv = compute.specific_volume(ureg.Quantity(Decimal("0.2"), "kg/m^3"), to="ft^3/lb")
    assert sv.magnitude == Decimal("80.092316869800725")
    assert sv.units == ureg.foot**3 / ureg.pound

import functools
from decimal import Decimal

from pint import Quantity

from api import ureg


def requires_dimensionality(*dimensionalities):
    def decorator_requires_dimensionality(func):
        @functools.wraps(func)
        def wrapper_requires_dimensionality(*args, **kwargs):
            for arg in args:
                if not isinstance(arg, Quantity) or not isinstance(arg.magnitude, Decimal):
                    raise ValueError("All arguments must be Quantity with magnitude of Decimal")

            for arg, dimensionality in zip(args, dimensionalities, strict=True):
                if not arg.check(dimensionality):
                    raise ValueError

            return func(*args, **kwargs)

        return wrapper_requires_dimensionality

    return decorator_requires_dimensionality


@requires_dimensionality("[density]")
def specific_volume(rho, /, *, to: str = "m^3/kg"):
    """
    Compute the Specific Volume.

    V = 1 / rho

    Where
        V   = specific volume, m^3/kg
        rho = fluid density, kg/m^3
    """
    return (1 / rho).to(to)


@requires_dimensionality("[velocity]", "[length]", "kinematic_viscosity")
def reynolds_number1(u, dh, v, /):
    """
    Compute the Reynolds Number.

    Re = u * dh / v

    Where
        Re  = Reynolds number, dimensionless
        u   = mean fluid velocity, m/s
        dh  = hydraulic diameter, m
        v   = kinematic viscosity, m^2/s
    """
    return u.to("m/s") * dh.to("m") / v.to("m^2/s")


@requires_dimensionality("[velocity]", "[length]", "[viscosity]", "[density]")
def reynolds_number2(u, dh, mu, rho, /):
    """
    Compute the Reynolds Number.

    Re = rho * u * dh / mu

    Where:
        Re  = Reynolds number, dimensionless
        rho = fluid density, kg/m^3
        u   = mean fluid velocity, m/s
        dh  = hydraulic diameter, m
        mu  = dynamic viscosity, N*s/m^s
    """
    return rho.to("m") * u.to("m/s") * dh.to("m") / mu.to("N*s/m^2")

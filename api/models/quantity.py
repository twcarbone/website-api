import decimal

import pint

from api import ureg
from api.models import Base
from api.models import hybrid
from api.models import sa


class HasQuantityColumn:
    """
    Mixed-in classes have an event listener configured for 'mapper_configured'.
    """

    pass


class QuantityColumn(object):
    def __init__(self, unit: str, column: sa.Column):
        """
        Create a new QuantityColumn instance with units of *unit* and SQLAlchemy column
        *column*, where *unit* is a attribute name from pint.UnitRegistry.
        """
        self.unit = unit
        self.column = column


@sa.event.listens_for(HasQuantityColumn, "mapper_configured", propagate=True)
def get_quantity_columns(mapper, cls):
    """
    Scans each attribute of models inheriting from 'HasQuantityColumn'. For any
    attribute of type 'QuantityColumn', create a mapped column and hybrid
    getter/setter/expression methods.

    Inspired by:
     - https://github.com/robintw/sqlalchemy-units-example
     - https://stackoverflow.com/a/14096082
    """
    for attr in dir(cls):
        if isinstance((quantity_column := getattr(cls, attr)), QuantityColumn):
            name = f"_{attr}"
            unit = getattr(ureg, quantity_column.unit)

            # Create SQLAlchemy Column. The column is mapped to the database column
            # matching the name of the attribute. The python class attribute name is the
            # column name with a leading underscore.
            #
            # Example:
            # ```
            # # The following QuantityColumn
            # value = QuantityColumn("in", Column(Float()))
            #
            # # Creates the following Column
            # _value = Column("value", Float())
            # ```
            quantity_column.column.name = attr
            setattr(cls, name, quantity_column.column)

            @hybrid.hybrid_property
            def columnhybrid(self) -> pint.Quantity:
                return getattr(self, name) * unit

            @columnhybrid.inplace.setter
            def columnhybrid_setter(self, quantity):
                try:
                    if not quantity.check(unit.dimensionality):
                        raise ValueError(f"Quantity must have dimensionality of {unit.dimensionality}")
                except AttributeError:
                    raise TypeError("Must be a Quantity")

                setattr(self, name, decimal.Decimal(quantity.to(unit).magnitude))

            @columnhybrid.inplace.expression
            def columnhybrid_expression(self):
                return getattr(self, name)

            # Create getter, setter, and expression
            setattr(cls, attr, columnhybrid)
            setattr(cls, attr, columnhybrid_expression)
            setattr(cls, attr, columnhybrid_setter)

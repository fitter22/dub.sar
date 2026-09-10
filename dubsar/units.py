"""DUB.SAR 1.0 — Units and Quantities System.

Implements Sections 7, 9, 15, and 16:
- First-class unit and dimension expressions
- Reference units: second, minute, hour, day (𒌓), month (𒌗), year (𒈬)
- Dimension algebra: multiply, divide, power
- Strict dimensional compatibility checks for addition, subtraction, comparison
- Explicit unit conversions via convert(value, target_unit)
- Quantity representation: (value: Rational, unit: Unit)
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple, Union

from dubsar.errors import DubSarDivisionByZero, DubSarUnitError
from dubsar.numbers import Rational, to_rational


class Unit:
    """Represents a physical/abstract unit with dimensional exponents and scale factor.

    Dimensions are stored as a mapping from base dimension name to integer/rational exponent.
    The scale factor relates this unit to its base dimensional unit.
    For example:
      second: dims={'time': 1}, scale=1
      minute: dims={'time': 1}, scale=60
      hour:   dims={'time': 1}, scale=3600
      day:    dims={'time': 1}, scale=86400
      month:  dims={'month': 1}, scale=1 (abstract calendar unit)
      year:   dims={'year': 1}, scale=1  (abstract astronomical unit)
      dimensionless: dims={}, scale=1
    """

    __slots__ = ("_dims", "_scale", "_name")

    def __init__(
        self,
        dims: Optional[Dict[str, int]] = None,
        scale: Union[Rational, int] = 1,
        name: Optional[str] = None,
    ) -> None:
        self._scale = to_rational(scale)
        # Normalize dimensions: remove zero exponents, sort keys
        filtered_dims = {}
        if dims:
            for k, exp in dims.items():
                if exp != 0:
                    filtered_dims[k] = exp
        self._dims: Dict[str, int] = dict(sorted(filtered_dims.items()))
        self._name = name

    @property
    def dimensions(self) -> Dict[str, int]:
        return dict(self._dims)

    @property
    def scale(self) -> Rational:
        return self._scale

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def is_dimensionless(self) -> bool:
        return len(self._dims) == 0

    def is_compatible_with(self, other: Unit) -> bool:
        """Checks if two units have identical dimensional exponents."""
        return self._dims == other._dims

    def __hash__(self) -> int:
        return hash((tuple(sorted(self._dims.items())), self._scale))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Unit):
            return False
        return self._dims == other._dims and self._scale == other._scale

    def __repr__(self) -> str:
        return f"Unit({self.format()})"

    def __str__(self) -> str:
        return self.format()

    def format(self, use_cuneiform: bool = False) -> str:
        """Formats the unit for display."""
        if self._name:
            if use_cuneiform:
                c_name = UNIT_TO_CUNEIFORM.get(self._name, self._name)
                return c_name
            return self._name

        if self.is_dimensionless:
            return ""

        pos_parts = []
        neg_parts = []
        for d, exp in self._dims.items():
            disp_d = d
            if use_cuneiform and disp_d in UNIT_TO_CUNEIFORM:
                disp_d = UNIT_TO_CUNEIFORM[disp_d]

            if exp > 0:
                pos_parts.append(f"{disp_d}^{exp}" if exp != 1 else disp_d)
            else:
                pos_parts_neg = f"{disp_d}^{-exp}" if exp != -1 else disp_d
                neg_parts.append(pos_parts_neg)

        if not pos_parts and not neg_parts:
            return ""
        if not neg_parts:
            return " * ".join(pos_parts)
        if not pos_parts:
            return "1 / (" + " * ".join(neg_parts) + ")"
        return " * ".join(pos_parts) + " / (" + " * ".join(neg_parts) + ")"

    def __mul__(self, other: Unit) -> Unit:
        new_dims = dict(self._dims)
        for d, exp in other._dims.items():
            new_dims[d] = new_dims.get(d, 0) + exp
        new_scale = self._scale * other._scale
        new_name = None
        if other.is_dimensionless:
            new_name = self._name
        elif self.is_dimensionless:
            new_name = other._name
        return Unit(new_dims, new_scale, name=new_name)

    def __truediv__(self, other: Unit) -> Unit:
        new_dims = dict(self._dims)
        for d, exp in other._dims.items():
            new_dims[d] = new_dims.get(d, 0) - exp
        new_scale = self._scale / other._scale
        new_name = self._name if other.is_dimensionless else None
        return Unit(new_dims, new_scale, name=new_name)

    def __pow__(self, exp: int) -> Unit:
        if not isinstance(exp, int):
            raise TypeError("Unit power must be an integer")
        new_dims = {d: v * exp for d, v in self._dims.items()}
        new_scale = self._scale**exp
        return Unit(new_dims, new_scale)


# Dimensionless singleton
DIMENSIONLESS = Unit(dims={}, scale=1, name="")

# Base standard unit definitions per Section 15
UNIT_TABLE: Dict[str, Unit] = {
    # Time units (base dimension: time, base unit: second)
    "second": Unit({"time": 1}, scale=1, name="second"),
    "sec": Unit({"time": 1}, scale=1, name="second"),
    "minute": Unit({"time": 1}, scale=60, name="minute"),
    "min": Unit({"time": 1}, scale=60, name="minute"),
    "hour": Unit({"time": 1}, scale=3600, name="hour"),
    "hr": Unit({"time": 1}, scale=3600, name="hour"),
    "day": Unit({"time": 1}, scale=86400, name="day"),
    "ud": Unit({"time": 1}, scale=86400, name="day"),
    "𒌓": Unit({"time": 1}, scale=86400, name="𒌓"),

    # Calendar units (abstract separate dimensions per Section 15 & 16)
    "month": Unit({"month": 1}, scale=1, name="month"),
    "iti": Unit({"month": 1}, scale=1, name="month"),
    "𒌗": Unit({"month": 1}, scale=1, name="𒌗"),

    "year": Unit({"year": 1}, scale=1, name="year"),
    "mu": Unit({"year": 1}, scale=1, name="year"),
    "𒈬": Unit({"year": 1}, scale=1, name="𒈬"),

    # Weight / metrology units (base dimension: mass, base: shekel)
    "talent": Unit({"mass": 1}, scale=3600, name="talent"),
    "gun": Unit({"mass": 1}, scale=3600, name="talent"),
    "𒄘": Unit({"mass": 1}, scale=3600, name="𒄘"),
    "mina": Unit({"mass": 1}, scale=60, name="mina"),
    "ma-na": Unit({"mass": 1}, scale=60, name="mina"),
    "𒈠𒈾": Unit({"mass": 1}, scale=60, name="𒈠𒈾"),
}

UNIT_TO_CUNEIFORM: Dict[str, str] = {
    "day": "𒌓",
    "ud": "𒌓",
    "month": "𒌗",
    "iti": "𒌗",
    "year": "𒈬",
    "mu": "𒈬",
    "talent": "𒄘",
    "gun": "𒄘",
    "mina": "𒈠𒈾",
    "ma-na": "𒈠𒈾",
}

CUNEIFORM_TO_UNIT_NAME: Dict[str, str] = {
    "𒌓": "day",
    "𒌗": "month",
    "𒈬": "year",
    "𒄘": "talent",
    "𒈠𒈾": "mina",
}


def lookup_unit(name: str) -> Unit:
    """Looks up or dynamically creates a named unit."""
    name_clean = name.strip()
    if not name_clean:
        return DIMENSIONLESS
    if name_clean in UNIT_TABLE:
        return UNIT_TABLE[name_clean]
    # For custom/unknown units, treat as a distinct base dimension
    return Unit({name_clean: 1}, scale=1, name=name_clean)


class Quantity:
    """A pair: (value: Rational, unit: Unit) as defined in Section 7."""

    __slots__ = ("_value", "_unit")

    def __init__(self, value: Union[Rational, int, str, float], unit: Optional[Unit] = None) -> None:
        self._value = to_rational(value)
        self._unit = unit if unit is not None else DIMENSIONLESS

    @property
    def value(self) -> Rational:
        return self._value

    @property
    def unit(self) -> Unit:
        return self._unit

    @property
    def is_dimensionless(self) -> bool:
        return self._unit.is_dimensionless

    def base_value(self) -> Rational:
        """Magnitude in base dimensional units."""
        return self._value * self._unit.scale

    def __hash__(self) -> int:
        return hash((self.base_value(), tuple(sorted(self._unit.dimensions.items()))))

    def __repr__(self) -> str:
        u_str = f" {self._unit}" if not self.is_dimensionless else ""
        return f"Quantity({self._value}{u_str})"

    def __str__(self) -> str:
        return self.format()

    def format(self, use_cuneiform: bool = False, format_mode: str = "canonical") -> str:
        """Formats the quantity with its unit."""
        if format_mode == "sexagesimal":
            val_str = self._value.format_sexagesimal()
        else:
            val_str = self._value.format_canonical()

        if self.is_dimensionless:
            return val_str

        u_str = self._unit.format(use_cuneiform=use_cuneiform)
        if not u_str:
            return val_str
        return f"{val_str} {u_str}"

    def convert_to(self, target_unit: Unit) -> Quantity:
        """Explicitly converts this quantity to target_unit per Section 16."""
        if not self._unit.is_compatible_with(target_unit):
            raise DubSarUnitError(
                f"Cannot convert incompatible units: {self._unit} to {target_unit}"
            )
        # val_target * target.scale = val_source * source.scale
        new_val = (self._value * self._unit.scale) / target_unit.scale
        return Quantity(new_val, target_unit)

    # Arithmetic operations
    def __add__(self, other: Union[Quantity, Rational, int]) -> Quantity:
        other_q = to_quantity(other)
        if not self._unit.is_compatible_with(other_q._unit):
            raise DubSarUnitError(
                f"Cannot add incompatible quantities: {self} + {other_q}"
            )
        # Convert other to self's unit if scale differs
        if self._unit._scale == other_q._unit._scale:
            return Quantity(self._value + other_q._value, self._unit)
        other_conv = other_q.convert_to(self._unit)
        return Quantity(self._value + other_conv._value, self._unit)

    def __radd__(self, other: Union[Quantity, Rational, int]) -> Quantity:
        return to_quantity(other).__add__(self)

    def __sub__(self, other: Union[Quantity, Rational, int]) -> Quantity:
        other_q = to_quantity(other)
        if not self._unit.is_compatible_with(other_q._unit):
            raise DubSarUnitError(
                f"Cannot subtract incompatible quantities: {self} - {other_q}"
            )
        if self._unit._scale == other_q._unit._scale:
            return Quantity(self._value - other_q._value, self._unit)
        other_conv = other_q.convert_to(self._unit)
        return Quantity(self._value - other_conv._value, self._unit)

    def __rsub__(self, other: Union[Quantity, Rational, int]) -> Quantity:
        return to_quantity(other).__sub__(self)

    def __mul__(self, other: Union[Quantity, Rational, int]) -> Quantity:
        other_q = to_quantity(other)
        new_val = self._value * other_q._value
        new_unit = self._unit * other_q._unit
        return Quantity(new_val, new_unit)

    def __rmul__(self, other: Union[Quantity, Rational, int]) -> Quantity:
        return self.__mul__(other)

    def __truediv__(self, other: Union[Quantity, Rational, int]) -> Quantity:
        other_q = to_quantity(other)
        if other_q._value == 0:
            raise DubSarDivisionByZero("Division by zero")
        new_val = self._value / other_q._value
        new_unit = self._unit / other_q._unit
        return Quantity(new_val, new_unit)

    def __rtruediv__(self, other: Union[Quantity, Rational, int]) -> Quantity:
        return to_quantity(other).__truediv__(self)

    def __mod__(self, other: Union[Quantity, Rational, int]) -> Quantity:
        other_q = to_quantity(other)
        if not self._unit.is_compatible_with(other_q._unit):
            raise DubSarUnitError(
                f"Cannot modulo incompatible quantities: {self} % {other_q}"
            )
        other_conv = other_q.convert_to(self._unit)
        return Quantity(self._value % other_conv._value, self._unit)

    def __pow__(self, exp: int) -> Quantity:
        if not isinstance(exp, int):
            raise TypeError("Exponent must be an integer")
        return Quantity(self._value**exp, self._unit**exp)

    def __neg__(self) -> Quantity:
        return Quantity(-self._value, self._unit)

    def __pos__(self) -> Quantity:
        return self

    def __abs__(self) -> Quantity:
        return Quantity(abs(self._value), self._unit)

    def abs(self) -> Quantity:
        return abs(self)

    # Comparisons
    def _check_cmp_compat(self, other: Quantity) -> None:
        if not self._unit.is_compatible_with(other._unit):
            raise DubSarUnitError(
                f"Cannot compare incompatible quantities: {self} and {other}"
            )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (Quantity, Rational, int)):
            return False
        other_q = to_quantity(other)
        if not self._unit.is_compatible_with(other_q._unit):
            return False
        return self.base_value() == other_q.base_value()

    def __lt__(self, other: Union[Quantity, Rational, int]) -> bool:
        other_q = to_quantity(other)
        self._check_cmp_compat(other_q)
        return self.base_value() < other_q.base_value()

    def __le__(self, other: Union[Quantity, Rational, int]) -> bool:
        other_q = to_quantity(other)
        self._check_cmp_compat(other_q)
        return self.base_value() <= other_q.base_value()

    def __gt__(self, other: Union[Quantity, Rational, int]) -> bool:
        other_q = to_quantity(other)
        self._check_cmp_compat(other_q)
        return self.base_value() > other_q.base_value()

    def __ge__(self, other: Union[Quantity, Rational, int]) -> bool:
        other_q = to_quantity(other)
        self._check_cmp_compat(other_q)
        return self.base_value() >= other_q.base_value()

    # Built-in math operations (§14)
    def floor(self) -> Quantity:
        """Mathematical floor: retains unit, magnitude floor."""
        return Quantity(Rational(self._value.floor(), 1), self._unit)

    def ceil(self) -> Quantity:
        """Mathematical ceiling: retains unit, magnitude ceil."""
        return Quantity(Rational(self._value.ceil(), 1), self._unit)

    def nearest(self) -> Quantity:
        """Returns the nearest integer, retaining the quantity's unit."""
        return Quantity(Rational(self._value.nearest(), 1), self._unit)


def to_quantity(val: Union[Quantity, Rational, int, str, float]) -> Quantity:
    """Converts a value to a Quantity."""
    if isinstance(val, Quantity):
        return val
    return Quantity(to_rational(val), DIMENSIONLESS)

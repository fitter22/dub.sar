"""DUB.SAR 1.0 — Built-in Mathematical Procedures.

Implements Section 14 and Section 16:
- abs(x)
- floor(x)
- ceil(x)
- nearest(x) (exact half-way cases round away from zero; yields dimensionless integer)
- min(a, b)
- max(a, b)
- gcd(a, b)
- lcm(a, b)
- convert(value, target_unit)
"""

from __future__ import annotations

import math
from typing import Any, Callable, Dict, List, Union

from dubsar.errors import DubSarNameError, DubSarUnitError
from dubsar.numbers import Rational
from dubsar.units import (
    DIMENSIONLESS,
    Quantity,
    Unit,
    lookup_unit,
    to_quantity,
)


def builtin_abs(x: Union[Quantity, Rational, int]) -> Quantity:
    """Returns absolute value, preserving unit."""
    q = to_quantity(x)
    return abs(q)


def builtin_floor(x: Union[Quantity, Rational, int]) -> Quantity:
    """Mathematical floor: retains unit, magnitude floor."""
    q = to_quantity(x)
    return q.floor()


def builtin_ceil(x: Union[Quantity, Rational, int]) -> Quantity:
    """Mathematical ceiling: retains unit, magnitude ceil."""
    q = to_quantity(x)
    return q.ceil()


def builtin_nearest(x: Union[Quantity, Rational, int]) -> Quantity:
    """Returns the nearest integer.

    Per Section 14.1:
    - If argument is dimensionless, result is dimensionless integer.
    - If argument is a quantity, result is the corresponding integer count and is dimensionless.
    - Exact half-way cases round away from zero.
    """
    q = to_quantity(x)
    return q.nearest()


def builtin_min(a: Union[Quantity, Rational, int], b: Union[Quantity, Rational, int]) -> Quantity:
    """Returns the minimum of two dimensionally compatible quantities."""
    qa = to_quantity(a)
    qb = to_quantity(b)
    if not qa.unit.is_compatible_with(qb.unit):
        raise DubSarUnitError(f"Cannot compute min of incompatible quantities: {qa} and {qb}")
    return qa if qa <= qb else qb


def builtin_max(a: Union[Quantity, Rational, int], b: Union[Quantity, Rational, int]) -> Quantity:
    """Returns the maximum of two dimensionally compatible quantities."""
    qa = to_quantity(a)
    qb = to_quantity(b)
    if not qa.unit.is_compatible_with(qb.unit):
        raise DubSarUnitError(f"Cannot compute max of incompatible quantities: {qa} and {qb}")
    return qa if qa >= qb else qb


def builtin_gcd(a: Union[Quantity, Rational, int], b: Union[Quantity, Rational, int]) -> Quantity:
    """Greatest common divisor of two integers."""
    qa = to_quantity(a)
    qb = to_quantity(b)
    if not qa.value.is_integer or not qb.value.is_integer:
        raise DubSarUnitError("gcd requires integer arguments")
    val = math.gcd(int(qa.value.numerator), int(qb.value.numerator))
    return Quantity(val, DIMENSIONLESS)


def builtin_lcm(a: Union[Quantity, Rational, int], b: Union[Quantity, Rational, int]) -> Quantity:
    """Least common multiple of two integers."""
    qa = to_quantity(a)
    qb = to_quantity(b)
    if not qa.value.is_integer or not qb.value.is_integer:
        raise DubSarUnitError("lcm requires integer arguments")
    na = abs(int(qa.value.numerator))
    nb = abs(int(qb.value.numerator))
    if na == 0 or nb == 0:
        return Quantity(0, DIMENSIONLESS)
    val = (na * nb) // math.gcd(na, nb)
    return Quantity(val, DIMENSIONLESS)


def builtin_convert(value: Union[Quantity, Rational, int], target: Union[Unit, str, Quantity]) -> Quantity:
    """Explicit conversion: convert(value, target_unit) per Section 16."""
    q = to_quantity(value)
    if isinstance(target, str):
        target_unit = lookup_unit(target)
    elif isinstance(target, Unit):
        target_unit = target
    elif isinstance(target, Quantity):
        target_unit = target.unit
    else:
        raise DubSarUnitError(f"Invalid target unit specification: {target}")

    return q.convert_to(target_unit)


BUILTINS: Dict[str, Callable[..., Any]] = {
    "abs": builtin_abs,
    "floor": builtin_floor,
    "ceil": builtin_ceil,
    "nearest": builtin_nearest,
    "min": builtin_min,
    "max": builtin_max,
    "gcd": builtin_gcd,
    "lcm": builtin_lcm,
    "convert": builtin_convert,
}

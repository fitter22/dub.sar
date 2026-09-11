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


def builtin_square(x: Union[Quantity, Rational, int]) -> Quantity:
    """Returns square of quantity: x * x."""
    q = to_quantity(x)
    return q.square()


def builtin_square_root(x: Union[Quantity, Rational, int], allow_approx: bool = False) -> Quantity:
    """Returns exact square root if rational, or Babylonian approximation if allow_approx is True."""
    q = to_quantity(x)
    return q.square_root(allow_approx=allow_approx)


def builtin_right_triangle(
    short: Union[Quantity, Rational, int],
    long: Union[Quantity, Rational, int],
    diag: Optional[Union[Quantity, Rational, int]] = None,
) -> Any:
    """Creates/solves a right-triangle mathematical determination."""
    from dubsar.geometry import RightTriangleValue
    return RightTriangleValue.determine(short_side=short, long_side=long, diagonal=diag)


def builtin_validate_triangle(tri: Any) -> bool:
    """Validates the Pythagorean relation of a right triangle determination."""
    if hasattr(tri, "is_valid"):
        return tri.is_valid()
    from dubsar.geometry import RightTriangleValue
    if isinstance(tri, dict):
        rt = RightTriangleValue(tri.get("short-side", 0), tri.get("long-side", 0), tri.get("diagonal", 0))
        return rt.is_valid()
    return False


def builtin_scale_triangle(tri: Any, factor: Union[Quantity, Rational, int]) -> Any:
    """Scales a right-triangle determination by a rational factor."""
    if hasattr(tri, "scale"):
        return tri.scale(factor)
    raise DubSarUnitError(f"Cannot scale non-triangle object: {tri}")


def builtin_inclination(
    rise: Union[Quantity, Rational, int],
    run: Union[Quantity, Rational, int],
) -> Quantity:
    """Returns the dimensionless slope ratio: rise / run."""
    qr = to_quantity(rise)
    qu = to_quantity(run)
    return qr / qu


def builtin_feed(
    rise: Union[Quantity, Rational, int],
    run: Union[Quantity, Rational, int],
) -> Quantity:
    """Returns the dimensionless feed ratio (run per rise, Old Babylonian mūṣû)."""
    qr = to_quantity(rise)
    qu = to_quantity(run)
    return qu / qr


def builtin_direction(
    rise_or_turn: Any,
    run: Optional[Any] = None,
) -> Any:
    """Constructs a Direction orientation."""
    from dubsar.geometry import Direction, Turn
    if run is not None:
        return Direction.from_inclination(rise=rise_or_turn, run=run)
    if isinstance(rise_or_turn, Turn):
        return Direction(rise_or_turn)
    return Direction(Turn(rise_or_turn))


def builtin_turn(fraction: Any) -> Any:
    """Constructs a Turn fraction."""
    from dubsar.geometry import Turn
    return Turn(fraction)


def builtin_rotate(target: Any, turn_val: Any) -> Any:
    """Rotates a Direction or DirectedQuantity by a Turn fraction."""
    if hasattr(target, "rotate"):
        return target.rotate(turn_val)
    raise DubSarUnitError(f"Cannot rotate target of type {type(target)}")


def builtin_directed_quantity(magnitude: Any, dir_val: Optional[Any] = None) -> Any:
    """Constructs a DirectedQuantity: magnitude + direction."""
    from dubsar.geometry import DirectedQuantity
    return DirectedQuantity(magnitude, dir_val)


def builtin_approximate(val: Any, precision: int = 6) -> Any:
    """Explicitly converts a quantity to an ApproximateQuantity with requested precision."""
    from dubsar.geometry import ApproximateQuantity
    return ApproximateQuantity(val, precision=precision)


def builtin_within_tolerance(a: Any, b: Any, tol: Any) -> bool:
    """Compares two values within declared error tolerance."""
    if hasattr(a, "is_within_tolerance"):
        return a.is_within_tolerance(b, tol)
    if hasattr(b, "is_within_tolerance"):
        return b.is_within_tolerance(a, tol)
    qa = to_quantity(a)
    qb = to_quantity(b)
    diff = abs(qa - qb)
    tq = to_quantity(tol)
    return diff.base_value() <= tq.base_value()


def builtin_is_power_of_two(n: Any) -> bool:
    """Determines whether integer n is a power of 2."""
    val = int(to_quantity(n).value.numerator)
    return val > 0 and (val & (val - 1)) == 0


def builtin_dft(sequence_data: Any, inverse: bool = False) -> Any:
    """Computes Discrete Fourier Transform of sequence tablet."""
    from dubsar.geometry import reference_dft
    return reference_dft(sequence_data, inverse=inverse)


def builtin_fft(sequence_data: Any, inverse: bool = False) -> Any:
    """Computes Fast Fourier Transform of sequence tablet."""
    from dubsar.geometry import recursive_fft
    return recursive_fft(sequence_data, inverse=inverse)


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
    "square": builtin_square,
    "square_root": builtin_square_root,
    "sqrt": builtin_square_root,
    "right_triangle": builtin_right_triangle,
    "validate_triangle": builtin_validate_triangle,
    "scale_triangle": builtin_scale_triangle,
    "inclination": builtin_inclination,
    "feed": builtin_feed,
    "direction": builtin_direction,
    "turn": builtin_turn,
    "rotate": builtin_rotate,
    "directed_quantity": builtin_directed_quantity,
    "approximate": builtin_approximate,
    "within_tolerance": builtin_within_tolerance,
    "is_power_of_two": builtin_is_power_of_two,
    "dft": builtin_dft,
    "fft": builtin_fft,
}

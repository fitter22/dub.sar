"""DUB.SAR 1.0 — Geometric Mathematics Foundation.

Implements the Geometric Mathematics Foundation and Coherent Path to Fourier Mathematics:
- Layer A: Exact scalar quantities
- Layer B: Ratios and reciprocals
- Layer C: Geometric relations (square, square-root, right-triangle, inclination/feed, validation)
- Layer D: Direction (orientation without premature angles/degrees)
- Layer E: Turn system (whole-turn, fractional turns, rotation)
- Layer F: Explicit approximation (requested precision / tolerance, no silent float conversion)
- Layer G: Directed quantities (magnitude + direction, component extraction, vector addition)
- Layer H: Fourier mathematics (equal turn divisions, reference DFT, recursive FFT)
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple, Union

from dubsar.archive.working import WorkingTablet
from dubsar.errors import (
    DubSarGeometricError,
    DubSarMathError,
    DubSarTypeError,
    DubSarUnitError,
)
from dubsar.numbers import Rational, to_rational
from dubsar.units import DIMENSIONLESS, Quantity, Unit, to_quantity
from dubsar.values import DeterminationValue


# ==============================================================================
# Layer E: Turn System
# ==============================================================================

class Turn:
    """Represents a fraction of a complete cycle/turn: tau in [0, 1).

    Per Section 9.2: Turn is the parent mathematical concept for rotation,
    divisions of a cycle, and harmonic roots, rather than premature modern degree/radian units.
    """

    __slots__ = ("_fraction",)

    def __init__(self, fraction: Union[Rational, int, str, float]) -> None:
        r = to_rational(fraction)
        # Normalize to [0, 1)
        mod_val = r % Rational(1, 1)
        if mod_val < Rational(0, 1):
            mod_val = mod_val + Rational(1, 1)
        self._fraction: Rational = mod_val

    @property
    def fraction(self) -> Rational:
        return self._fraction

    @property
    def is_whole(self) -> bool:
        return self._fraction == 0

    @property
    def is_half(self) -> bool:
        return self._fraction == Rational(1, 2)

    @property
    def is_quarter(self) -> bool:
        return self._fraction == Rational(1, 4) or self._fraction == Rational(3, 4)

    @classmethod
    def whole(cls) -> Turn:
        return cls(0)

    @classmethod
    def half(cls) -> Turn:
        return cls(Rational(1, 2))

    @classmethod
    def quarter(cls) -> Turn:
        return cls(Rational(1, 4))

    @classmethod
    def eighth(cls) -> Turn:
        return cls(Rational(1, 8))

    @classmethod
    def division(cls, k: int, n: int) -> Turn:
        """Returns the k-th equal division of a full turn into n parts."""
        if n <= 0:
            raise DubSarMathError("Turn division requires positive integer n")
        return cls(Rational(k, n))

    def rotate(self, other: Turn) -> Turn:
        return Turn(self._fraction + other._fraction)

    def __add__(self, other: Union[Turn, Rational, int]) -> Turn:
        if isinstance(other, Turn):
            return Turn(self._fraction + other._fraction)
        return Turn(self._fraction + to_rational(other))

    def __sub__(self, other: Union[Turn, Rational, int]) -> Turn:
        if isinstance(other, Turn):
            return Turn(self._fraction - other._fraction)
        return Turn(self._fraction - to_rational(other))

    def __mul__(self, other: Union[int, Rational]) -> Turn:
        r = to_rational(other)
        return Turn(self._fraction * r)

    def __rmul__(self, other: Union[int, Rational]) -> Turn:
        return self.__mul__(other)

    def __truediv__(self, other: Union[int, Rational]) -> Turn:
        r = to_rational(other)
        if r == 0:
            raise DubSarMathError("Division by zero in turn calculation")
        return Turn(self._fraction / r)

    def __neg__(self) -> Turn:
        return Turn(-self._fraction)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Turn):
            return self._fraction == other._fraction
        return False

    def __hash__(self) -> int:
        return hash(self._fraction)

    def __repr__(self) -> str:
        return f"Turn({self.format()})"

    def __str__(self) -> str:
        return self.format()

    def format(self) -> str:
        if self._fraction == 0:
            return "whole-turn"
        elif self._fraction == Rational(1, 2):
            return "half-turn"
        elif self._fraction == Rational(1, 4):
            return "quarter-turn"
        elif self._fraction == Rational(3, 4):
            return "three-quarter-turn"
        elif self._fraction == Rational(1, 8):
            return "eighth-turn"
        return f"{self._fraction.format_canonical()}-turn"


# ==============================================================================
# Layer D: Direction
# ==============================================================================

class Direction:
    """Represents a geometric orientation in the plane.

    Defined conceptually by orientation relative to a reference direction,
    without requiring premature modern degrees or radians.
    """

    __slots__ = ("_turn", "_name")

    def __init__(self, turn: Union[Turn, Rational, int] = 0, name: Optional[str] = None) -> None:
        self._turn = turn if isinstance(turn, Turn) else Turn(turn)
        self._name = name

    @property
    def turn(self) -> Turn:
        return self._turn

    @property
    def fraction(self) -> Rational:
        return self._turn.fraction

    @classmethod
    def reference(cls) -> Direction:
        """Reference direction along the horizontal positive axis."""
        return cls(Turn.whole(), name="reference")

    @classmethod
    def perpendicular(cls) -> Direction:
        """Quarter-turn perpendicular direction."""
        return cls(Turn.quarter(), name="perpendicular")

    @classmethod
    def opposite_reference(cls) -> Direction:
        """Half-turn opposite direction."""
        return cls(Turn.half(), name="opposite")

    @classmethod
    def from_inclination(
        cls,
        rise: Union[Quantity, Rational, int],
        run: Union[Quantity, Rational, int],
    ) -> Direction:
        """Derives a direction from geometric rise and run (inclination)."""
        r_rise = to_quantity(rise).base_value()
        r_run = to_quantity(run).base_value()

        if r_run == 0 and r_rise == 0:
            raise DubSarGeometricError("Cannot determine direction from zero rise and zero run")

        # Exact axis cases
        if r_run > 0 and r_rise == 0:
            return cls(Turn.whole())
        elif r_run == 0 and r_rise > 0:
            return cls(Turn.quarter())
        elif r_run < 0 and r_rise == 0:
            return cls(Turn.half())
        elif r_run == 0 and r_rise < 0:
            return cls(Turn(Rational(3, 4)))
        # Exact diagonal cases (1/8 turn)
        elif r_run > 0 and r_rise == r_run:
            return cls(Turn.eighth())
        elif r_run < 0 and r_rise == -r_run:
            return cls(Turn(Rational(3, 8)))
        elif r_run < 0 and r_rise == r_run:
            return cls(Turn(Rational(5, 8)))
        elif r_run > 0 and r_rise == -r_run:
            return cls(Turn(Rational(7, 8)))

        # General case: compute approximate turn fraction from atan2
        num_y, den_y = r_rise.numerator, r_rise.denominator
        num_x, den_x = r_run.numerator, r_run.denominator
        mb = max(num_y.bit_length(), den_y.bit_length(), num_x.bit_length(), den_x.bit_length())
        if mb > 80:
            sh = mb - 80
            num_y >>= sh
            den_y >>= sh
            num_x >>= sh
            den_x >>= sh
            if den_y == 0:
                den_y = 1
            if den_x == 0:
                den_x = 1

        ang = math.atan2(float(num_y) / float(den_y), float(num_x) / float(den_x))
        frac = (ang / (2.0 * math.pi)) % 1.0
        # Convert to high-precision rational fraction
        rat_frac = Rational(int(round(frac * 360000)), 360000)
        return cls(Turn(rat_frac))

    @classmethod
    def from_components(cls, x: Union[Rational, int], y: Union[Rational, int]) -> Direction:
        return cls.from_inclination(rise=y, run=x)

    def rotate(self, turn: Union[Turn, Rational, int]) -> Direction:
        t = turn if isinstance(turn, Turn) else Turn(turn)
        return Direction(self._turn.rotate(t))

    def perpendicular_dir(self) -> Direction:
        """Returns direction rotated by quarter-turn."""
        return self.rotate(Turn.quarter())

    def opposite(self) -> Direction:
        """Returns direction rotated by half-turn."""
        return self.rotate(Turn.half())

    def components(self, allow_approx: bool = True) -> Tuple[Rational, Rational]:
        """Returns (x, y) unit components of the direction.

        Exact rationals are returned for cardinal quarter-turns and attested multiples.
        """
        frac = self._turn.fraction
        if frac == 0:
            return (Rational(1), Rational(0))
        elif frac == Rational(1, 4):
            return (Rational(0), Rational(1))
        elif frac == Rational(1, 2):
            return (Rational(-1), Rational(0))
        elif frac == Rational(3, 4):
            return (Rational(0), Rational(-1))
        elif frac == Rational(1, 8):
            val = Rational(17, 24)
            return (val, val)
        elif frac == Rational(3, 8):
            val = Rational(17, 24)
            return (-val, val)
        elif frac == Rational(5, 8):
            val = Rational(17, 24)
            return (-val, -val)
        elif frac == Rational(7, 8):
            val = Rational(17, 24)
            return (val, -val)

        if not allow_approx:
            raise DubSarGeometricError(
                f"Direction with turn {self._turn} cannot be converted to exact rational Cartesian components without approximation"
            )

        rad = float(frac.numerator) / float(frac.denominator) * 2.0 * math.pi
        cos_val = math.cos(rad)
        sin_val = math.sin(rad)
        rx = Rational(int(round(cos_val * 1000000)), 1000000)
        ry = Rational(int(round(sin_val * 1000000)), 1000000)
        return (rx, ry)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Direction):
            return self._turn == other._turn
        return False

    def __hash__(self) -> int:
        return hash(self._turn)

    def __repr__(self) -> str:
        return f"Direction({self._turn.format()})"

    def __str__(self) -> str:
        if self._name:
            return self._name
        return f"direction({self._turn.format()})"


# ==============================================================================
# Layer F: Explicit Approximation
# ==============================================================================

class ApproximateQuantity:
    """Explicitly approximate quantity with specified precision or error tolerance.

    Per Section 12: Approximate values CANNOT silently participate in exact equality checks.
    Exact rational arithmetic remains the default, and approximation is an explicit determination.
    """

    __slots__ = ("_quantity", "_precision", "_tolerance")

    def __init__(
        self,
        quantity: Union[Quantity, Rational, int],
        precision: int = 6,
        tolerance: Optional[Union[Rational, int]] = None,
    ) -> None:
        self._quantity = to_quantity(quantity)
        self._precision = precision
        self._tolerance = to_rational(tolerance) if tolerance is not None else None

    @property
    def quantity(self) -> Quantity:
        return self._quantity

    @property
    def value(self) -> Rational:
        return self._quantity.value

    @property
    def unit(self) -> Unit:
        return self._quantity.unit

    @property
    def precision(self) -> int:
        return self._precision

    @property
    def tolerance(self) -> Optional[Rational]:
        return self._tolerance

    def is_within_tolerance(
        self,
        other: Union[ApproximateQuantity, Quantity, Rational, int],
        tolerance: Optional[Union[Quantity, Rational, int]] = None,
    ) -> bool:
        """Determines whether two quantities agree within declared tolerance."""
        other_q = other.quantity if isinstance(other, ApproximateQuantity) else to_quantity(other)
        diff = abs(self._quantity - other_q)
        tol_val = to_rational(tolerance) if tolerance is not None else (self._tolerance or Rational(1, 100000))
        return diff.base_value() <= tol_val

    def __eq__(self, other: object) -> bool:
        raise DubSarTypeError(
            "Approximate values cannot silently participate in exact equality checks (§12). "
            "Use an explicit 'within tolerance' determination."
        )

    def __repr__(self) -> str:
        return f"ApproximateQuantity(~{self._quantity})"

    def __str__(self) -> str:
        return f"~{self._quantity.format()}"


# ==============================================================================
# Layer G: Directed Quantity
# ==============================================================================

class DirectedQuantity:
    """A magnitude associated with a direction: magnitude + direction.

    Per Section 10: Represents vectors, rotations, and harmonic roots
    without exposing premature complex types or Euler's formula in the user language.
    """

    __slots__ = ("_magnitude", "_direction")

    def __init__(
        self,
        magnitude: Union[Quantity, Rational, int],
        direction: Optional[Direction] = None,
    ) -> None:
        q = to_quantity(magnitude)
        if q.value < 0:
            mag = abs(q)
            d = (direction or Direction.reference()).opposite()
        else:
            mag = q
            d = direction or Direction.reference()
        self._magnitude = mag
        self._direction = d

    @property
    def magnitude(self) -> Quantity:
        return self._magnitude

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def turn(self) -> Turn:
        return self._direction.turn

    def rotate(self, turn: Union[Turn, Rational, int]) -> DirectedQuantity:
        """Rotates the direction of the quantity by turn, preserving magnitude."""
        return DirectedQuantity(self._magnitude, self._direction.rotate(turn))

    def scale(self, factor: Union[Quantity, Rational, int]) -> DirectedQuantity:
        """Scales the magnitude of the quantity."""
        r = to_rational(factor.value if isinstance(factor, Quantity) else factor)
        if r < 0:
            return DirectedQuantity(self._magnitude * abs(r), self._direction.opposite())
        return DirectedQuantity(self._magnitude * r, self._direction)

    def opposite(self) -> DirectedQuantity:
        return DirectedQuantity(self._magnitude, self._direction.opposite())

    def __neg__(self) -> DirectedQuantity:
        return self.opposite()

    def horizontal_component(self, allow_approx: bool = True) -> Quantity:
        cx, _ = self._direction.components(allow_approx=allow_approx)
        return self._magnitude * cx

    def vertical_component(self, allow_approx: bool = True) -> Quantity:
        _, cy = self._direction.components(allow_approx=allow_approx)
        return self._magnitude * cy

    def add(
        self,
        other: DirectedQuantity,
        allow_approx: bool = True,
    ) -> DirectedQuantity:
        """Vector addition of two directed quantities via component combination."""
        if not self._magnitude.unit.is_compatible_with(other._magnitude.unit):
            raise DubSarUnitError(
                f"Cannot add directed quantities with incompatible units: {self._magnitude.unit} and {other._magnitude.unit}"
            )

        x1, y1 = self._direction.components(allow_approx=allow_approx)
        x2, y2 = other._direction.components(allow_approx=allow_approx)

        m1 = self._magnitude.base_value()
        m2 = other._magnitude.base_value()

        net_x = m1 * x1 + m2 * x2
        net_y = m1 * y1 + m2 * y2

        if abs(net_x) < Rational(1, 1000000) and abs(net_y) < Rational(1, 1000000):
            return DirectedQuantity(Quantity(0, self._magnitude.unit), Direction.reference())

        sq_sum = net_x * net_x + net_y * net_y
        if sq_sum.is_perfect_square():
            mag_val = sq_sum.exact_sqrt()
            assert mag_val is not None
        else:
            mag_val = sq_sum.sqrt_babylonian(iterations=4)

        net_mag = Quantity(mag_val / self._magnitude.unit.scale, self._magnitude.unit)
        if net_mag.value == 0:
            return DirectedQuantity(net_mag, Direction.reference())

        net_dir = Direction.from_components(x=net_x, y=net_y)
        return DirectedQuantity(net_mag, net_dir)

    def __add__(self, other: DirectedQuantity) -> DirectedQuantity:
        if not isinstance(other, DirectedQuantity):
            raise DubSarTypeError(f"Cannot add {type(other)} to DirectedQuantity")
        return self.add(other)

    def __sub__(self, other: DirectedQuantity) -> DirectedQuantity:
        if not isinstance(other, DirectedQuantity):
            raise DubSarTypeError(f"Cannot subtract {type(other)} from DirectedQuantity")
        return self.add(other.opposite())

    def __repr__(self) -> str:
        return f"DirectedQuantity({self._magnitude} along {self._direction})"

    def __str__(self) -> str:
        return f"{self._magnitude} along {self._direction}"


# ==============================================================================
# Layer C: Geometric Determinations (Right Triangle, Inclination)
# ==============================================================================

class RightTriangleValue(DeterminationValue):
    """A structured right-triangle mathematical determination.

    Per Section 5.3: Contains short-side, long-side, diagonal, inclination, feed, and area.
    """

    def __init__(
        self,
        short_side: Union[Quantity, Rational, int],
        long_side: Union[Quantity, Rational, int],
        diagonal: Union[Quantity, Rational, int],
    ) -> None:
        q_short = to_quantity(short_side)
        q_long = to_quantity(long_side)
        q_diag = to_quantity(diagonal)

        inclination = q_long / q_short
        feed = q_short / q_long
        area = (q_short * q_long) / Rational(2, 1)

        fields = {
            "short-side": q_short,
            "short_side": q_short,
            "long-side": q_long,
            "long_side": q_long,
            "diagonal": q_diag,
            "inclination": inclination,
            "feed": feed,
            "area": area,
        }
        super().__init__(fields)

    @classmethod
    def determine(
        cls,
        short_side: Optional[Union[Quantity, Rational, int]] = None,
        long_side: Optional[Union[Quantity, Rational, int]] = None,
        diagonal: Optional[Union[Quantity, Rational, int]] = None,
        allow_approx: bool = False,
    ) -> RightTriangleValue:
        """Solves the missing side of a right triangle using the Pythagorean relation."""
        count = sum(1 for s in (short_side, long_side, diagonal) if s is not None)
        if count < 2:
            raise DubSarGeometricError(
                "Right triangle determination requires at least two known sides"
            )

        q_s = to_quantity(short_side) if short_side is not None else None
        q_l = to_quantity(long_side) if long_side is not None else None
        q_d = to_quantity(diagonal) if diagonal is not None else None

        if q_s is not None and q_l is not None and q_d is None:
            d_sq = q_s.square() + q_l.square()
            q_d = d_sq.square_root(allow_approx=allow_approx)
        elif q_s is not None and q_d is not None and q_l is None:
            l_sq = q_d.square() - q_s.square()
            if l_sq.value < 0:
                raise DubSarGeometricError("Diagonal must be strictly greater than short side")
            q_l = l_sq.square_root(allow_approx=allow_approx)
        elif q_l is not None and q_d is not None and q_s is None:
            s_sq = q_d.square() - q_l.square()
            if s_sq.value < 0:
                raise DubSarGeometricError("Diagonal must be strictly greater than long side")
            q_s = s_sq.square_root(allow_approx=allow_approx)

        assert q_s is not None and q_l is not None and q_d is not None
        if q_s.base_value() > q_l.base_value():
            q_s, q_l = q_l, q_s

        return cls(q_s, q_l, q_d)

    def is_valid(self) -> bool:
        """Validates the exact Pythagorean consistency of the triangle."""
        s = self.fields["short-side"]
        l = self.fields["long-side"]
        d = self.fields["diagonal"]
        return (s.square() + l.square()) == d.square()

    def scale(self, factor: Union[Quantity, Rational, int]) -> RightTriangleValue:
        """Scales the triangle by a scalar ratio, preserving inclination and similarity."""
        r = to_rational(factor.value if isinstance(factor, Quantity) else factor)
        if r <= 0:
            raise DubSarGeometricError("Scale factor for geometric triangle must be positive")
        return RightTriangleValue(
            self.fields["short-side"] * r,
            self.fields["long-side"] * r,
            self.fields["diagonal"] * r,
        )

    def __repr__(self) -> str:
        return (
            f"right-triangle(short={self.fields['short-side']}, "
            f"long={self.fields['long-side']}, diagonal={self.fields['diagonal']}, "
            f"inclination={self.fields['inclination']})"
        )


def make_inclination(
    rise: Union[Quantity, Rational, int],
    run: Union[Quantity, Rational, int],
) -> DeterminationValue:
    """Creates a ratio-based inclination determination (rise / run)."""
    q_rise = to_quantity(rise)
    q_run = to_quantity(run)
    ratio = q_rise / q_run
    feed = q_run / q_rise
    return DeterminationValue({
        "rise": q_rise,
        "run": q_run,
        "ratio": ratio,
        "inclination": ratio,
        "feed": feed,
    })


# ==============================================================================
# Layer H: Reference DFT and Radix-2 FFT
# ==============================================================================

def sequence_to_directed_list(tablet_or_list: Any) -> List[DirectedQuantity]:
    """Extracts entries from a sequence tablet or list into a list of DirectedQuantity objects."""
    raw_entries: List[Any] = []
    if isinstance(tablet_or_list, WorkingTablet):
        for _, v in tablet_or_list.entries.items():
            raw_entries.append(v)
    elif hasattr(tablet_or_list, "entries"):
        entries = tablet_or_list.entries
        if isinstance(entries, dict):
            for _, v in entries.items():
                raw_entries.append(v)
        else:
            for _, v in entries:
                raw_entries.append(v)
    elif isinstance(tablet_or_list, (list, tuple)):
        raw_entries = list(tablet_or_list)
    else:
        raw_entries = [tablet_or_list]

    res: List[DirectedQuantity] = []
    for item in raw_entries:
        if isinstance(item, DirectedQuantity):
            res.append(item)
        elif isinstance(item, ApproximateQuantity):
            res.append(DirectedQuantity(item.quantity, Direction.reference()))
        else:
            q = to_quantity(item)
            res.append(DirectedQuantity(q, Direction.reference()))
    return res


def directed_list_to_tablet(
    directed_list: List[DirectedQuantity],
    name: str = "fourier-transform",
) -> WorkingTablet:
    """Packs a list of DirectedQuantity objects into a sequence WorkingTablet."""
    from dubsar.archive.models import TabletKind, TabletShape
    wt = WorkingTablet(name, shape=TabletShape.SEQUENCE, kind=TabletKind.MATHEMATICAL)
    for dq in directed_list:
        wt.append(dq)
    return wt


def reference_dft(
    input_data: Any,
    inverse: bool = False,
) -> WorkingTablet:
    """Computes the direct finite Discrete Fourier Transform (reference implementation).

    Per Section 14: Uses equal turn divisions and rotation of directed quantities.
    Serves as the semantic reference against which FFT is tested.
    """
    x = sequence_to_directed_list(input_data)
    N = len(x)
    if N == 0:
        return directed_list_to_tablet([], "dft-result")

    sign = 1 if inverse else -1
    result: List[DirectedQuantity] = []

    for k in range(N):
        acc: Optional[DirectedQuantity] = None
        for n in range(N):
            t = Turn.division(sign * (n * k), N)
            rotated_term = x[n].rotate(t)
            if acc is None:
                acc = rotated_term
            else:
                acc = acc.add(rotated_term)

        assert acc is not None
        if inverse:
            acc = acc.scale(Rational(1, N))
        result.append(acc)

    return directed_list_to_tablet(result, "dft-result")


def recursive_fft(
    input_data: Any,
    inverse: bool = False,
) -> WorkingTablet:
    """Computes the radix-2 Cooley-Tukey Fast Fourier Transform recursively.

    Per Section 16 Stage B: Decomposes N-point problem into even and odd entries,
    recursively transforms each half, and combines them by turn rotation.
    Preserves identical mathematical semantics to reference DFT.
    """
    x = sequence_to_directed_list(input_data)
    N = len(x)
    if N == 0:
        return directed_list_to_tablet([], "fft-result")

    if (N & (N - 1)) != 0:
        return reference_dft(x, inverse=inverse)

    def _fft_core(seq: List[DirectedQuantity], inv: bool) -> List[DirectedQuantity]:
        n_len = len(seq)
        if n_len <= 1:
            return seq

        even = _fft_core(seq[0::2], inv)
        odd = _fft_core(seq[1::2], inv)

        sign = 1 if inv else -1
        combined = [DirectedQuantity(0)] * n_len
        half_n = n_len // 2

        for k in range(half_n):
            twiddle = Turn.division(sign * k, n_len)
            rotated_odd = odd[k].rotate(twiddle)

            combined[k] = even[k].add(rotated_odd)
            combined[k + half_n] = even[k].add(rotated_odd.opposite())

        return combined

    transformed = _fft_core(x, inverse)
    if inverse:
        transformed = [dq.scale(Rational(1, N)) for dq in transformed]

    return directed_list_to_tablet(transformed, "fft-result")

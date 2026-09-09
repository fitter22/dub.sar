"""DUB.SAR 1.0 — Exact Rational Numbers and Sexagesimal Mathematics.

Implements Section 8:
- Arbitrary-precision exact rational representation: Rational(numerator, denominator)
- Canonical sexagesimal literals: integer ; digit , digit , ...
- Strict sexagesimal digit rules: 0 <= digit < 60
- Negative values: leading - applies to complete rational
- Cuneiform numeral table & resolution per Section 8.5
- Mathematical floor, ceil, and nearest (round away from zero) per Section 14
"""

from __future__ import annotations

import math
import re
from fractions import Fraction
from typing import Optional, Tuple, Union

from dubsar.errors import DubSarDivisionByZero, DubSarSyntaxError


class Rational:
    """Exact rational number with arbitrary-precision numerator and denominator."""

    __slots__ = ("_num", "_den")

    def __init__(self, numerator: int = 0, denominator: int = 1) -> None:
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise TypeError(f"Numerator and denominator must be integers, got {type(numerator)} and {type(denominator)}")
        if denominator == 0:
            raise DubSarDivisionByZero("Division by zero")

        if denominator < 0:
            numerator = -numerator
            denominator = -denominator

        common = math.gcd(abs(numerator), denominator)
        self._num = numerator // common
        self._den = denominator // common

    @property
    def numerator(self) -> int:
        return self._num

    @property
    def denominator(self) -> int:
        return self._den

    @property
    def is_integer(self) -> bool:
        return self._den == 1

    def __hash__(self) -> int:
        return hash((self._num, self._den))

    def __repr__(self) -> str:
        if self._den == 1:
            return f"Rational({self._num})"
        return f"Rational({self._num}, {self._den})"

    def __str__(self) -> str:
        return self.format_canonical()

    def format_canonical(self) -> str:
        """Formats into canonical DUB.SAR representation (sexagesimal if terminating, or fraction/integer)."""
        if self._den == 1:
            return str(self._num)
        
        # Check if denominator is regular (prime factors only 2, 3, 5)
        # Such fractions terminate in base 60.
        temp = self._den
        for p in (2, 3, 5):
            while temp % p == 0:
                temp //= p
        
        if temp == 1:
            # Terminating sexagesimal!
            return self.format_sexagesimal()
        
        # Non-regular rational: format as mixed fraction or p/q
        if abs(self._num) >= self._den:
            whole = self._num // self._den if self._num >= 0 else -(-self._num // self._den)
            rem = abs(self._num) % self._den
            if rem == 0:
                return str(whole)
            if self._num < 0:
                return f"-({abs(whole)} + {rem}/{self._den})"
            return f"{whole} + {rem}/{self._den}"
        return f"{self._num}/{self._den}"

    def format_sexagesimal(self, max_places: int = 10) -> str:
        """Formats the rational as a sexagesimal literal `integer;d1,d2,...`."""
        if self._den == 1:
            return str(self._num)

        sign = "-" if self._num < 0 else ""
        abs_num = abs(self._num)
        whole = abs_num // self._den
        rem = abs_num % self._den

        digits = []
        seen_rem = set()
        count = 0
        while rem > 0 and count < max_places:
            rem *= 60
            digit = rem // self._den
            digits.append(str(digit))
            rem = rem % self._den
            count += 1

        digits_str = ",".join(digits) if digits else "0"
        return f"{sign}{whole};{digits_str}"

    # Operators
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Rational):
            return self._num == other._num and self._den == other._den
        if isinstance(other, int):
            return self._den == 1 and self._num == other
        if isinstance(other, Fraction):
            return self._num == other.numerator and self._den == other.denominator
        return False

    def __lt__(self, other: Union[Rational, int]) -> bool:
        other_rat = to_rational(other)
        return self._num * other_rat._den < other_rat._num * self._den

    def __le__(self, other: Union[Rational, int]) -> bool:
        other_rat = to_rational(other)
        return self._num * other_rat._den <= other_rat._num * self._den

    def __gt__(self, other: Union[Rational, int]) -> bool:
        other_rat = to_rational(other)
        return self._num * other_rat._den > other_rat._num * self._den

    def __ge__(self, other: Union[Rational, int]) -> bool:
        other_rat = to_rational(other)
        return self._num * other_rat._den >= other_rat._num * self._den

    def __add__(self, other: Union[Rational, int]) -> Rational:
        other_rat = to_rational(other)
        return Rational(
            self._num * other_rat._den + other_rat._num * self._den,
            self._den * other_rat._den,
        )

    def __radd__(self, other: Union[Rational, int]) -> Rational:
        return self.__add__(other)

    def __sub__(self, other: Union[Rational, int]) -> Rational:
        other_rat = to_rational(other)
        return Rational(
            self._num * other_rat._den - other_rat._num * self._den,
            self._den * other_rat._den,
        )

    def __rsub__(self, other: Union[Rational, int]) -> Rational:
        return to_rational(other).__sub__(self)

    def __mul__(self, other: Union[Rational, int]) -> Rational:
        other_rat = to_rational(other)
        return Rational(self._num * other_rat._num, self._den * other_rat._den)

    def __rmul__(self, other: Union[Rational, int]) -> Rational:
        return self.__mul__(other)

    def __truediv__(self, other: Union[Rational, int]) -> Rational:
        other_rat = to_rational(other)
        if other_rat._num == 0:
            raise DubSarDivisionByZero("Division by zero")
        return Rational(self._num * other_rat._den, self._den * other_rat._num)

    def __rtruediv__(self, other: Union[Rational, int]) -> Rational:
        return to_rational(other).__truediv__(self)

    def __mod__(self, other: Union[Rational, int]) -> Rational:
        other_rat = to_rational(other)
        if other_rat._num == 0:
            raise DubSarDivisionByZero("Modulo by zero")
        div_val = (self._num * other_rat._den) // (self._den * other_rat._num)
        return self - (other_rat * div_val)

    def __pow__(self, exponent: int) -> Rational:
        if not isinstance(exponent, int):
            raise TypeError(f"DUB.SAR power operator requires integer exponent, got {type(exponent)}")
        if exponent == 0:
            return Rational(1, 1)
        if exponent < 0:
            if self._num == 0:
                raise DubSarDivisionByZero("Zero cannot be raised to negative power")
            return Rational(self._den ** (-exponent), self._num ** (-exponent))
        return Rational(self._num ** exponent, self._den ** exponent)

    def __neg__(self) -> Rational:
        return Rational(-self._num, self._den)

    def __pos__(self) -> Rational:
        return self

    def __abs__(self) -> Rational:
        return Rational(abs(self._num), self._den)

    def floor(self) -> int:
        """Mathematical floor (largest integer <= self)."""
        return self._num // self._den

    def ceil(self) -> int:
        """Mathematical ceiling (smallest integer >= self)."""
        return -(-self._num // self._den)

    def nearest(self) -> int:
        """Returns the nearest integer. Exact half-way cases round away from zero.

        Per Section 14.1:
        nearest(2.49) = 2
        nearest(2.5)  = 3
        nearest(-2.5) = -3
        """
        num, den = self._num, self._den
        if num >= 0:
            # floor((2*num + den) / (2*den))
            return (2 * num + den) // (2 * den)
        else:
            abs_num = -num
            # round away from zero for negative
            abs_res = (2 * abs_num + den) // (2 * den)
            return -abs_res


def to_rational(val: Union[Rational, int, str, float, Fraction]) -> Rational:
    """Converts a value to an exact Rational."""
    if isinstance(val, Rational):
        return val
    if isinstance(val, int):
        return Rational(val, 1)
    if isinstance(val, Fraction):
        return Rational(val.numerator, val.denominator)
    if isinstance(val, float):
        # Convert float string representation to exact fraction
        return to_rational(str(val))
    if isinstance(val, str):
        return parse_number(val)
    raise TypeError(f"Cannot convert {type(val)} to Rational")


# ==============================================================================
# Canonical Cuneiform Numeral Table per Section 8.5
# ==============================================================================

# Single and compound cuneiform signs mapped to digits 1..59
DUB_SAR_NUMERAL_TABLE: dict[str, int] = {
    # Vertical DISH / ASH signs (1..9)
    "𒁹": 1,   # U+12079 (Cuneiform sign DISH)
    "𒐕": 1,   # U+12415 (Cuneiform numeric sign ONE GESH2 / DISH)
    "𒀸": 1,   # U+12038 (Cuneiform sign ASH)
    "𒈫": 2,   # U+1222B (Cuneiform sign MIN)
    "𒐖": 2,   # U+12416 (TWO GESH2)
    "𒐀": 2,   # U+12400 (TWO ASH)
    "𒐈": 3,   # U+12080 / U+12408 (ESZ / THREE DISH)
    "𒐗": 3,   # U+12417 (THREE GESH2)
    "𒐁": 3,   # U+12401 (THREE ASH)
    "𒐉": 4,   # U+12409 (FOUR DISH)
    "𒐂": 4,   # U+12402 (FOUR ASH)
    "𒐘": 4,   # U+12418 (FOUR GESH2)
    "𒐊": 5,   # U+1240A (FIVE DISH)
    "𒐃": 5,   # U+12403 (FIVE ASH)
    "𒐙": 5,   # U+12419 (FIVE GESH2)
    "𒐋": 6,   # U+1240B (SIX DISH)
    "𒐄": 6,   # U+12404 (SIX ASH)
    "𒐚": 6,   # U+1241A (SIX GESH2)
    "𒐌": 7,   # U+1240C (SEVEN DISH)
    "𒐅": 7,   # U+12405 (SEVEN ASH)
    "𒐛": 7,   # U+1241B (SEVEN GESH2)
    "𒐍": 8,   # U+1240D (EIGHT DISH)
    "𒐆": 8,   # U+12406 (EIGHT ASH)
    "𒐜": 8,   # U+1241C (EIGHT GESH2)
    "证券投资基金业协会": 9,   # U+1240E (NINE DISH)
    "𒐇": 9,   # U+12407 (NINE ASH)
    "𒐝": 9,   # U+1241D (NINE GESH2)

    # Corner U signs (tens: 10..50)
    "𒌋": 10,  # U+1230B (U)
    "𒎙": 20,  # U+12399 (NISH / 20)
    "𒌍": 30,  # U+1230D (ESZ20 / 30)
    "𒐏": 40,  # U+1240F / U+1230E (NIMIN / 40)
    "𒐐": 50,  # U+12410 / U+1230F (NINNU / 50)
}

# Add combinations like 𒌋𒁹 (11), 𒌋𒈫 (12), 𒌍𒐊 (35), etc.
_tens_signs = [("", 0), ("𒌋", 10), ("𒎙", 20), ("𒌍", 30), ("𒐏", 40), ("𒐐", 50)]
_ones_signs = [
    ("", 0),
    ("𒁹", 1),
    ("𒈫", 2),
    ("𒐈", 3),
    ("𒐉", 4),
    ("𒐊", 5),
    ("𒐋", 6),
    ("𒐌", 7),
    ("𒐍", 8),
    ("证券投资基金业协会", 9),
]

for t_sign, t_val in _tens_signs:
    for o_sign, o_val in _ones_signs:
        val = t_val + o_val
        if val > 0 and (t_sign + o_sign) not in DUB_SAR_NUMERAL_TABLE:
            DUB_SAR_NUMERAL_TABLE[t_sign + o_sign] = val


def parse_cuneiform_digit(s: str) -> Optional[int]:
    """Resolves a cuneiform numeral string through the DUB.SAR numeral table."""
    if s in DUB_SAR_NUMERAL_TABLE:
        return DUB_SAR_NUMERAL_TABLE[s]
    # Check if made of tens and ones
    # Count U signs and vertical signs
    total = 0
    i = 0
    n = len(s)
    while i < n:
        matched = False
        # Try longer matches first
        for length in (2, 1):
            if i + length <= n:
                sub = s[i : i + length]
                if sub in DUB_SAR_NUMERAL_TABLE:
                    total += DUB_SAR_NUMERAL_TABLE[sub]
                    i += length
                    matched = True
                    break
        if not matched:
            return None
    if 0 <= total < 60:
        return total
    return None


def parse_sexagesimal(s: str) -> Rational:
    """Parses a canonical sexagesimal literal `integer;digit,digit,...`.

    Each fractional digit must satisfy 0 <= digit < 60 per Section 8.3.
    """
    s = s.strip()
    if not s:
        raise DubSarSyntaxError("Empty number literal")

    sign = 1
    if s.startswith("-"):
        sign = -1
        s = s[1:].strip()
    elif s.startswith("+"):
        s = s[1:].strip()

    if ";" not in s:
        raise DubSarSyntaxError(f"Invalid sexagesimal format (missing ';'): {s}")

    whole_str, frac_str = s.split(";", 1)
    whole_str = whole_str.strip()

    # Parse whole part (could be decimal integer or cuneiform)
    cun_whole = parse_cuneiform_digit(whole_str)
    if cun_whole is not None:
        whole = cun_whole
    else:
        try:
            whole = int(whole_str)
        except ValueError:
            raise DubSarSyntaxError(f"Invalid integer part in sexagesimal literal: {whole_str}")

    result = Rational(whole, 1)

    # Parse fractional digits
    frac_parts = [p.strip() for p in frac_str.split(",") if p.strip()]
    if not frac_parts:
        raise DubSarSyntaxError(f"Expected fractional digits after ';' in: {s}")

    for idx, part in enumerate(frac_parts, start=1):
        cun_digit = parse_cuneiform_digit(part)
        if cun_digit is not None:
            digit = cun_digit
        else:
            try:
                digit = int(part)
            except ValueError:
                raise DubSarSyntaxError(f"Invalid sexagesimal digit: '{part}' in {s}")

        # Section 8.3 digit rule: 0 <= digit < 60
        if not (0 <= digit < 60):
            raise DubSarSyntaxError(
                f"Sexagesimal fractional digit must satisfy 0 <= digit < 60, got {digit} in {s}"
            )

        frac_val = Rational(digit, 60**idx)
        result = result + frac_val

    return -result if sign == -1 else result


def parse_number(s: str) -> Rational:
    """Parses any valid DUB.SAR number representation:

    - Decimal integer: 365, 0, -1000
    - Canonical sexagesimal: 365;14,31,55 or 1;30
    - Decimal float / fraction: 365.2422 (converted exactly)
    - Cuneiform numeral
    """
    s = s.strip()
    if not s:
        raise DubSarSyntaxError("Empty numeric literal")

    # Check for sexagesimal
    if ";" in s or "𒑱" in s:
        # Normalize cuneiform separator 𒑱 to ;
        s_norm = s.replace("𒑱", ";")
        return parse_sexagesimal(s_norm)

    # Check for cuneiform numeral
    cun_val = parse_cuneiform_digit(s)
    if cun_val is not None:
        return Rational(cun_val, 1)

    # Check for standard integer, decimal float, or fraction (e.g. 3/2)
    try:
        if "." in s or "/" in s:
            frac = Fraction(s)
            return Rational(frac.numerator, frac.denominator)
        val = int(s)
        return Rational(val, 1)
    except ValueError:
        pass

    raise DubSarSyntaxError(f"Unrecognized number literal: '{s}'")


def format_cuneiform_digit(val: int) -> str:
    """Formats a single sexagesimal digit (0..59) in cuneiform signs."""
    if val == 0:
        return ""
    tens = (val // 10) * 10
    ones = val % 10
    tens_sign = {0: "", 10: "𒌋", 20: "𒎙", 30: "𒌍", 40: "𒐏", 50: "𒐐"}.get(tens, "")
    ones_sign = {
        0: "",
        1: "𒁹",
        2: "𒈫",
        3: "𒐈",
        4: "𒐉",
        5: "𒐊",
        6: "𒐋",
        7: "𒐌",
        8: "𒐍",
        9: "证券投资基金业协会",
    }.get(ones, "")
    return tens_sign + ones_sign

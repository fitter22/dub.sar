"""Tests for exact rational arithmetic and sexagesimal numbers."""

import unittest
from fractions import Fraction

from dubsar.errors import DubSarDivisionByZero, DubSarSyntaxError
from dubsar.numbers import (
    Rational,
    format_cuneiform_digit,
    parse_cuneiform_digit,
    parse_number,
    parse_sexagesimal,
    to_rational,
)


class TestNumbers(unittest.TestCase):
    def test_integers(self):
        r1 = parse_number("0")
        self.assertEqual(r1, 0)
        self.assertEqual(r1.numerator, 0)
        self.assertEqual(r1.denominator, 1)

        r2 = parse_number("365")
        self.assertEqual(r2, 365)
        self.assertEqual(str(r2), "365")

        r3 = parse_number("-100")
        self.assertEqual(r3, -100)

    def test_canonical_sexagesimals(self):
        # 1;30 = 1 + 30/60 = 3/2
        r1 = parse_number("1;30")
        self.assertEqual(r1, Rational(3, 2))
        self.assertEqual(r1.format_sexagesimal(), "1;30")

        # 0;30 = 1/2
        r2 = parse_number("0;30")
        self.assertEqual(r2, Rational(1, 2))
        self.assertEqual(r2.format_sexagesimal(), "0;30")

        # 1;0 = 1
        r3 = parse_number("1;0")
        self.assertEqual(r3, 1)

        # 365;14,31,55
        r_solar = parse_number("365;14,31,55")
        expected = Rational(365, 1) + Rational(14, 60) + Rational(31, 3600) + Rational(55, 216000)
        self.assertEqual(r_solar, expected)
        self.assertEqual(r_solar.format_sexagesimal(), "365;14,31,55")

    def test_sexagesimal_digit_rules(self):
        # Valid 1;59,59
        r = parse_number("1;59,59")
        self.assertIsNotNone(r)

        # Invalid 1;60,0 (Section 8.3 requires 0 <= digit < 60)
        with self.assertRaises(DubSarSyntaxError):
            parse_number("1;60,0")

        with self.assertRaises(DubSarSyntaxError):
            parse_number("1;75")

    def test_negative_values(self):
        # -1;30 means -(1 + 30/60) = -3/2 per Section 8.4
        r = parse_number("-1;30")
        self.assertEqual(r, Rational(-3, 2))
        self.assertEqual(r.format_sexagesimal(), "-1;30")

    def test_decimal_conversions(self):
        # Exact rational representation of decimal input
        r = parse_number("365.2422")
        self.assertEqual(r, Rational(1826211, 5000))
        self.assertEqual(r.numerator, 1826211)
        self.assertEqual(r.denominator, 5000)

    def test_cuneiform_numerals(self):
        # Section 8.5 numeral resolution
        self.assertEqual(parse_cuneiform_digit("𒁹"), 1)
        self.assertEqual(parse_cuneiform_digit("𒈫"), 2)
        self.assertEqual(parse_cuneiform_digit("𒐈"), 3)
        self.assertEqual(parse_cuneiform_digit("𒌋"), 10)
        self.assertEqual(parse_cuneiform_digit("𒎙"), 20)
        self.assertEqual(parse_cuneiform_digit("𒌍"), 30)

        # Compound cuneiform: 𒌍𒐊 = 35
        self.assertEqual(parse_cuneiform_digit("𒌍𒐊"), 35)

        # Cuneiform number parsing
        self.assertEqual(parse_number("𒐈"), 3)

    def test_nearest_rounding(self):
        # Section 14.1 nearest: exact half-way cases round away from zero
        self.assertEqual(parse_number("2.49").nearest(), 2)
        self.assertEqual(parse_number("2.5").nearest(), 3)
        self.assertEqual(parse_number("-2.5").nearest(), -3)
        self.assertEqual(parse_number("-2.49").nearest(), -2)

    def test_exact_arithmetic(self):
        # 1;30 + 0;30 = 2
        self.assertEqual(parse_number("1;30") + parse_number("0;30"), 2)
        # 2 * 0;30 = 1
        self.assertEqual(2 * parse_number("0;30"), 1)
        # 3 / 2 = 1;30
        self.assertEqual(parse_number("3") / parse_number("2"), parse_number("1;30"))

        # Zero division
        with self.assertRaises(DubSarDivisionByZero):
            _ = parse_number("1") / parse_number("0")


if __name__ == "__main__":
    unittest.main()

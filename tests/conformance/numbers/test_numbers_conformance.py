"""DUB.SAR 1.0 — Numbers Conformance Tests per Section 72."""

import unittest
from dubsar.numbers import Rational, parse_sexagesimal, parse_number

class TestNumbersConformance(unittest.TestCase):
    def test_sexagesimal_parsing(self):
        self.assertEqual(parse_sexagesimal("1;30"), Rational(3, 2))
        self.assertEqual(parse_sexagesimal("1;24,51,10"), Rational(30547, 21600))
        self.assertEqual(parse_sexagesimal("0;30"), Rational(1, 2))
        self.assertEqual(parse_number("60"), Rational(60, 1))

    def test_decimal_conversion(self):
        self.assertEqual(parse_number("365.2422"), Rational(1826211, 5000))

    def test_exact_rational_arithmetic(self):
        a = Rational(3, 2)
        b = Rational(1, 2)
        self.assertEqual(a + b, Rational(2, 1))
        self.assertEqual(a - b, Rational(1, 1))
        self.assertEqual(a * b, Rational(3, 4))
        self.assertEqual(a / b, Rational(3, 1))

    def test_sexagesimal_formatting(self):
        self.assertEqual(Rational(3, 2).format_sexagesimal(), "1;30")
        self.assertEqual(Rational(1, 2).format_sexagesimal(), "0;30")

if __name__ == "__main__":
    unittest.main()

"""DUB.SAR 1.0 — Conformance Suite: Numeric Conformance (CR-016).

Exhaustive tests for canonical numeric values:
0, 1, 2, 59, 60, 1;0, 1;30, 1;59,59, 365;14,31,55, -1;30
Validates:
- parsing
- normalization
- arithmetic
- comparison
- exact formatting
- round-trip source conversion
"""

import unittest

from dubsar.numbers import Rational, parse_number, to_rational


class TestNumericConformance(unittest.TestCase):
    """CR-016 exhaustive numeric conformance test suite."""

    def test_required_numeric_parsing(self):
        cases = [
            ("0", Rational(0)),
            ("1", Rational(1)),
            ("2", Rational(2)),
            ("59", Rational(59)),
            ("60", Rational(60)),
            ("1;0", Rational(1)),
            ("1;30", Rational(3, 2)),
            ("1;59,59", Rational(1) + Rational(59, 60) + Rational(59, 3600)),
            ("365;14,31,55", Rational(365) + Rational(14, 60) + Rational(31, 3600) + Rational(55, 216000)),
            ("-1;30", Rational(-3, 2)),
        ]

        for text, expected in cases:
            with self.subTest(text=text):
                parsed = parse_number(text)
                self.assertEqual(parsed, expected, f"Failed parsing {text}")

    def test_exact_formatting_and_round_trip(self):
        cases = [
            (Rational(0), "0", "0"),
            (Rational(1), "1", "1"),
            (Rational(2), "2", "2"),
            (Rational(59), "59", "59"),
            (Rational(60), "60", "60"),
            (Rational(3, 2), "1;30", "1;30"),
            (Rational(-3, 2), "-1;30", "-1;30"),
            (Rational(1) + Rational(59, 60) + Rational(59, 3600), "1;59,59", "1;59,59"),
            (
                Rational(365) + Rational(14, 60) + Rational(31, 3600) + Rational(55, 216000),
                "365;14,31,55",
                "365;14,31,55",
            ),
        ]

        for rat, expected_sexag, expected_canon in cases:
            with self.subTest(rat=rat):
                self.assertEqual(rat.format_sexagesimal(), expected_sexag)
                self.assertEqual(rat.format_canonical(), expected_canon)

                # Round-trip: parsing the formatted string must return the exact same Rational
                rt = parse_number(expected_sexag)
                self.assertEqual(rt, rat)

    def test_arithmetic_conformance(self):
        # 1;30 + 1;30 == 3
        a = parse_number("1;30")
        b = parse_number("1;30")
        self.assertEqual(a + b, Rational(3))
        self.assertEqual((a + b).format_canonical(), "3")

        # 365;14,31,55 - 365 == 0;14,31,55
        full = parse_number("365;14,31,55")
        whole = parse_number("365")
        frac = full - whole
        self.assertEqual(frac, parse_number("0;14,31,55"))

        # 1;30 * 2 == 3
        self.assertEqual(a * 2, Rational(3))

        # 1;30 / 2 == 0;45
        self.assertEqual(a / 2, parse_number("0;45"))

        # Modulo
        self.assertEqual(full % 365, frac)

    def test_comparisons_conformance(self):
        neg = parse_number("-1;30")
        zero = parse_number("0")
        one = parse_number("1")
        one_thirty = parse_number("1;30")
        two = parse_number("2")
        sixty = parse_number("60")

        self.assertTrue(neg < zero < one < one_thirty < two < sixty)
        self.assertTrue(sixty > two > one_thirty > one > zero > neg)
        self.assertEqual(parse_number("1;0"), one)
        self.assertNotEqual(one_thirty, one)


if __name__ == "__main__":
    unittest.main()

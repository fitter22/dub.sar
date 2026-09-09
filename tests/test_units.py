"""Tests for the Units and Quantities system."""

import unittest

from dubsar.errors import DubSarDivisionByZero, DubSarUnitError
from dubsar.numbers import Rational
from dubsar.units import (
    DIMENSIONLESS,
    Quantity,
    Unit,
    lookup_unit,
    to_quantity,
)


class TestUnits(unittest.TestCase):
    def setUp(self):
        self.day = lookup_unit("day")
        self.hour = lookup_unit("hour")
        self.second = lookup_unit("second")
        self.minute = lookup_unit("minute")
        self.year = lookup_unit("year")
        self.month = lookup_unit("month")
        self.ud = lookup_unit("𒌓")
        self.mu = lookup_unit("𒈬")
        self.iti = lookup_unit("𒌗")

    def test_unit_aliases(self):
        self.assertTrue(self.day.is_compatible_with(self.ud))
        self.assertTrue(self.year.is_compatible_with(self.mu))
        self.assertTrue(self.month.is_compatible_with(self.iti))

    def test_unit_addition_compatible(self):
        # 3 𒌓 + 2 𒌓 = 5 𒌓
        q1 = Quantity(3, self.ud)
        q2 = Quantity(2, self.ud)
        res = q1 + q2
        self.assertEqual(res.value, 5)
        self.assertEqual(res.unit.name, "𒌓")

        # 1 day + 24 hour = 2 day
        q_day = Quantity(1, self.day)
        q_hour = Quantity(24, self.hour)
        res2 = q_day + q_hour
        self.assertEqual(res2.value, 2)
        self.assertEqual(res2.unit.name, "day")

    def test_unit_addition_incompatible_rejected(self):
        # Section 9.1: 3 𒌓 + 2 𒌗 is rejected
        q1 = Quantity(3, self.ud)
        q_month = Quantity(2, self.iti)
        with self.assertRaises(DubSarUnitError):
            _ = q1 + q_month

        # 1 day + 2 year is rejected (Section 29)
        with self.assertRaises(DubSarUnitError):
            _ = Quantity(1, self.day) + Quantity(2, self.year)

        # Dimensionless + Quantity is rejected
        with self.assertRaises(DubSarUnitError):
            _ = Quantity(1, self.day) + Quantity(5, DIMENSIONLESS)

    def test_unit_multiplication_and_division(self):
        # Section 9.2: 2 𒌓 * 3 𒌓 has unit day^2
        q1 = Quantity(2, self.ud)
        q2 = Quantity(3, self.ud)
        res_mul = q1 * q2
        self.assertEqual(res_mul.value, 6)
        self.assertEqual(res_mul.unit.dimensions, {"time": 2})

        # Section 9.3: 10 𒌓 / 2 has unit day
        q10 = Quantity(10, self.day)
        res_div = q10 / 2
        self.assertEqual(res_div.value, 5)
        self.assertEqual(res_div.unit.dimensions, {"time": 1})

        # 10 𒌓 / 2 𒌓 is dimensionless
        res_cancel = q10 / Quantity(2, self.day)
        self.assertEqual(res_cancel.value, 5)
        self.assertTrue(res_cancel.is_dimensionless)

    def test_explicit_conversion(self):
        # 7200 seconds -> 2 hours
        q_sec = Quantity(7200, self.second)
        q_hr = q_sec.convert_to(self.hour)
        self.assertEqual(q_hr.value, 2)
        self.assertEqual(q_hr.unit.name, "hour")

        # 36 hours -> 1;30 days (1.5 days)
        q_36hr = Quantity(36, self.hour)
        q_day = q_36hr.convert_to(self.day)
        self.assertEqual(q_day.value, Rational(3, 2))
        self.assertEqual(q_day.format(format_mode="sexagesimal"), "1;30 day")

        # Incompatible conversion: year to day rejected per Section 16
        q_yr = Quantity(1, self.year)
        with self.assertRaises(DubSarUnitError):
            q_yr.convert_to(self.day)

    def test_comparisons(self):
        q1 = Quantity(1, self.day)
        q2 = Quantity(24, self.hour)
        self.assertTrue(q1 == q2)
        self.assertTrue(q1 <= q2)

        q3 = Quantity(25, self.hour)
        self.assertTrue(q1 < q3)

        # Incompatible comparison raises UnitError (Section 10)
        with self.assertRaises(DubSarUnitError):
            _ = (Quantity(1, self.day) < Quantity(1, self.year))


if __name__ == "__main__":
    unittest.main()

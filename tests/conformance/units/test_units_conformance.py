"""DUB.SAR 1.0 — Units Conformance Tests per Section 72."""

import unittest
from dubsar.units import lookup_unit, Quantity, DubSarUnitError
from dubsar.numbers import Rational

class TestUnitsConformance(unittest.TestCase):
    def test_units_addition_compatible(self):
        d = lookup_unit("day")
        q1 = Quantity(Rational(1), d)
        q2 = Quantity(Rational(2), d)
        res = q1 + q2
        self.assertEqual(res.value, Rational(3))
        self.assertEqual(res.unit, d)

    def test_units_addition_incompatible(self):
        d = lookup_unit("day")
        m = lookup_unit("meter")
        q1 = Quantity(Rational(1), d)
        q2 = Quantity(Rational(1), m)
        with self.assertRaises(DubSarUnitError):
            _ = q1 + q2

    def test_units_conversion(self):
        s = lookup_unit("second")
        hr = lookup_unit("hour")
        q = Quantity(Rational(7200), s)
        conv = q.convert_to(hr)
        self.assertEqual(conv.value, Rational(2))
        self.assertEqual(conv.unit, hr)

if __name__ == "__main__":
    unittest.main()

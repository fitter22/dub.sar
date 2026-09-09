"""DUB.SAR 1.0 — Conformance Suite: Units and Dimensional Algebra (CR-003, CR-030, CR-031).

Validates:
- Compile-time static rejection of dimensionally incompatible quantities (1 day + 2 year)
- Dimension compatibility across time units (hour, minute, second, day)
- Explicit conversions via convert(value, target_unit)
- Dimensional multiplication, division, and scaling
"""

import unittest

from dubsar.errors import DubSarUnitError
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer
from dubsar.units import Quantity, lookup_unit


class TestUnitConformance(unittest.TestCase):
    """CR-003 static unit checking and dimensional algebra conformance suite."""

    def _check(self, source: str) -> None:
        tokens = Lexer(source).tokenize()
        prog = Parser(tokens).parse()
        SemanticAnalyzer().analyze(prog)

    def test_static_rejection_of_day_plus_year(self):
        source = """PROBLEM
    x := 1 day + 2 year
RESULT
    output x
"""
        with self.assertRaises(DubSarUnitError) as ctx:
            self._check(source)
        self.assertIn("incompatible units", str(ctx.exception).lower())
        self.assertIn("day", str(ctx.exception))
        self.assertIn("year", str(ctx.exception))

    def test_static_rejection_of_day_minus_meter(self):
        source = """PROBLEM
    x := 10 day - 5 meter
RESULT
    output x
"""
        with self.assertRaises(DubSarUnitError):
            self._check(source)

    def test_static_rejection_of_incompatible_comparison(self):
        source = """PROBLEM
    if 1 day < 1 month:
        output "invalid comparison"
RESULT
    output "done"
"""
        with self.assertRaises(DubSarUnitError):
            self._check(source)

    def test_compatible_time_conversions(self):
        u_day = lookup_unit("day")
        u_hr = lookup_unit("hour")
        u_min = lookup_unit("minute")

        q_day = Quantity(1, u_day)
        q_hr = q_day.convert_to(u_hr)
        self.assertEqual(q_hr.value, 24)
        self.assertEqual(str(q_hr), "24 hour")

        q_min = q_hr.convert_to(u_min)
        self.assertEqual(q_min.value, 1440)
        self.assertEqual(str(q_min), "1440 minute")

    def test_dimensional_multiplication_and_division(self):
        u_day = lookup_unit("day")
        q1 = Quantity(10, u_day)
        q2 = Quantity(2, u_day)

        # Division yields dimensionless
        ratio = q1 / q2
        self.assertTrue(ratio.is_dimensionless)
        self.assertEqual(ratio.value, 5)

        # Multiplication yields day^2
        area = q1 * q2
        self.assertEqual(area.unit.dimensions, {"time": 2})


if __name__ == "__main__":
    unittest.main()

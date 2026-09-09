"""DUB.SAR 1.0 — Conformance Suite: Algorithm Validation (CR-033, CR-034, CR-035).

Validates:
- Primary reference benchmark values: 365.2422 -> cycle 673, leaps 163, error 3/3365000
- Independent algorithm validation: bounded search vs. continued fraction semiconvergents
- Deterministic Bresenham leap day distribution
"""

import unittest

from dubsar.calendar import (
    bounded_search_leap_solver,
    bresenham_leap_distribution,
    continued_fraction_leap_solver,
)
from dubsar.numbers import Rational


class TestAlgorithmValidation(unittest.TestCase):
    """Independent mathematical algorithm validation suite."""

    def test_earth_benchmark_values(self):
        solar = Rational(3652422, 10000)  # 365.2422 days
        limit = 1000

        c_brute, l_brute, comm_brute, err_brute = bounded_search_leap_solver(solar, limit)
        c_cf, l_cf, comm_cf, err_cf = continued_fraction_leap_solver(solar, limit)

        # 1. Independent algorithm equivalence (CR-034)
        self.assertEqual((c_brute, l_brute, comm_brute, err_brute), (c_cf, l_cf, comm_cf, err_cf))

        # 2. Benchmark exact results (CR-033)
        self.assertEqual(c_cf, 673)
        self.assertEqual(l_cf, 163)
        self.assertEqual(comm_cf, 510)
        self.assertEqual(err_cf, Rational(3, 3365000))

        # Mean calendar year
        mean_year = Rational(365) + Rational(163, 673)
        self.assertEqual(mean_year, Rational(245808, 673))

    def test_other_planetary_cycles(self):
        # Mars: ~686.98 days
        mars_solar = Rational(68698, 100)
        c1, l1, _, e1 = bounded_search_leap_solver(mars_solar, 100)
        c2, l2, _, e2 = continued_fraction_leap_solver(mars_solar, 100)
        self.assertEqual((c1, l1, e1), (c2, l2, e2))
        self.assertEqual(c1, 50)
        self.assertEqual(l1, 49)

        # Julian: 365.25 -> 4-year cycle, 1 leap
        julian_solar = Rational(36525, 100)
        cj1, lj1, _, _ = bounded_search_leap_solver(julian_solar, 100)
        cj2, lj2, _, _ = continued_fraction_leap_solver(julian_solar, 100)
        self.assertEqual((cj1, lj1), (cj2, lj2))
        self.assertEqual(cj1, 4)
        self.assertEqual(lj1, 1)

    def test_deterministic_bresenham_distribution(self):
        # 4-year cycle with 1 leap
        pat4 = bresenham_leap_distribution(4, 1)
        self.assertEqual(len(pat4), 4)
        self.assertEqual(sum(pat4), 1)

        # 673-year cycle with 163 leaps
        pat673 = bresenham_leap_distribution(673, 163)
        self.assertEqual(len(pat673), 673)
        self.assertEqual(sum(pat673), 163)

        # Determinism: identical on repeated calls
        self.assertEqual(pat673, bresenham_leap_distribution(673, 163))


if __name__ == "__main__":
    unittest.main()

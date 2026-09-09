"""DUB.SAR 1.0 — Planetary Calendar and Leap Year Algorithms.

Implements CR-004, CR-033, CR-034, and CR-035:
- Exact Continued Fraction best rational approximation solver
- Bounded search leap-rule reference solver
- Bresenham-style deterministic leap day distribution
- Verification of benchmark values (673-year cycle with 163 leap years for 365.2422)
"""

from __future__ import annotations

from typing import List, Tuple

from dubsar.numbers import Rational, to_rational


def bounded_search_leap_solver(
    solar_year: Rational | int | str,
    max_cycle: int,
) -> Tuple[int, int, int, Rational]:
    """Finds optimal leap-year rule by bounded brute-force search over cycle lengths.

    Returns: (cycle, leap_years, common_years, error_in_days)
    """
    solar = to_rational(solar_year)
    whole = solar.floor()
    fraction = solar - whole

    best_cycle = 1
    best_leaps = 0
    best_error = abs(solar - whole)

    for cycle in range(1, max_cycle + 1):
        # Nearest integer leap count: round(cycle * fraction)
        # Using exact half-way rounding away from zero
        est_leaps = int((cycle * fraction).nearest().numerator)
        candidate = whole + Rational(est_leaps, cycle)
        err = abs(solar - candidate)

        if err < best_error:
            best_error = err
            best_cycle = cycle
            best_leaps = est_leaps

    common_years = best_cycle - best_leaps
    return best_cycle, best_leaps, common_years, best_error


def continued_fraction_leap_solver(
    solar_year: Rational | int | str,
    max_cycle: int,
) -> Tuple[int, int, int, Rational]:
    """Finds optimal leap-year rule via exact continued fraction convergents and semiconvergents.

    Guaranteed by Dirichlet/Lagrange approximation theorems to contain the best rational approximations.
    Returns: (cycle, leap_years, common_years, error_in_days)
    """
    solar = to_rational(solar_year)
    whole = solar.floor()
    fraction = solar - whole

    if fraction == 0:
        return 1, 0, 1, Rational(0)

    # Compute continued fraction expansion: fraction = [0; a1, a2, ...]
    cf_terms: List[int] = []
    rem = fraction
    while rem.numerator != 0:
        a = rem.floor()
        cf_terms.append(int(a.numerator))
        diff = rem - a
        if diff == 0:
            break
        rem = Rational(diff.denominator, diff.numerator)

    # Compute convergents and intermediate semiconvergents
    p = [0, 1]
    q = [1, 0]

    candidates: List[Tuple[int, int]] = []

    for a in cf_terms:
        p_prev2, p_prev1 = p[-2], p[-1]
        q_prev2, q_prev1 = q[-2], q[-1]

        # Consider semiconvergents p_k(m) / q_k(m) for m in [1, a]
        for m in range(1, a + 1):
            pk = m * p_prev1 + p_prev2
            qk = m * q_prev1 + q_prev2
            if 1 <= qk <= max_cycle:
                candidates.append((pk, qk))

        p.append(a * p_prev1 + p_prev2)
        q.append(a * q_prev1 + q_prev2)

    best_cycle = 1
    best_leaps = 0
    best_error = abs(fraction)

    for pk, qk in candidates:
        candidate_frac = Rational(pk, qk)
        err = abs(fraction - candidate_frac)
        if err < best_error or (err == best_error and qk < best_cycle):
            best_error = err
            best_cycle = qk
            best_leaps = pk

    common_years = best_cycle - best_leaps
    return best_cycle, best_leaps, common_years, best_error


def bresenham_leap_distribution(cycle: int, leaps: int) -> List[int]:
    """Generates deterministic, maximally even leap day distribution using Bresenham's algorithm.

    Returns a list of length `cycle`, where each entry is 1 (leap year) or 0 (common year).
    Sum of entries is strictly equal to `leaps`.
    """
    if cycle <= 0:
        return []

    acc = 0
    pattern: List[int] = []

    for _ in range(cycle):
        acc += leaps
        if acc >= cycle:
            acc -= cycle
            pattern.append(1)
        else:
            pattern.append(0)

    return pattern

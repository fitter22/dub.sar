"""DUB.SAR 1.0 — Conformance Suite: Planetary Leap Benchmark & Distribution (CR-032, CR-033, CR-035).

Executes the planetary leap solver and even distribution reference examples
across both reference interpreter and bytecode VM with exact value checks.
"""

import unittest
from pathlib import Path

from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer
from dubsar.vm import VirtualMachine


class TestPlanetaryLeapConformance(unittest.TestCase):
    """Verifies that planetary leap benchmark and distribution conform to CR-032, CR-033, and CR-035."""

    def setUp(self):
        self.repo_root = Path(__file__).parent.parent.parent
        self.leap_path = self.repo_root / "examples" / "planetary_leap.dub"
        self.dist_path = self.repo_root / "examples" / "even_distribution.dub"

    def test_planetary_leap_benchmark_both_engines(self):
        source = self.leap_path.read_text(encoding="utf-8")
        tokens = Lexer(source).tokenize()
        program = Parser(tokens).parse()
        SemanticAnalyzer().analyze(program)

        # 1. AST Interpreter with Earth tropical year: 365.2422
        interp = Interpreter(input_fn=lambda p: "365.2422", output_fn=lambda s: None)
        interp_out = interp.run(program)

        # 2. Stack Bytecode VM
        compiler = Compiler()
        compiled = compiler.compile(program)
        vm = VirtualMachine(input_fn=lambda p: "365.2422", output_fn=lambda s: None)
        vm_out = vm.execute(compiled)

        # CR-046: AST Evaluator == VM
        self.assertEqual(interp_out, vm_out)

        # Section 26.3: Benchmark values
        self.assertIn("673", vm_out)
        self.assertIn("163 day", vm_out)
        self.assertIn("3/3365000 day", vm_out)

        # Independent continued-fraction / brute-force leap-year verification
        from fractions import Fraction
        solar_frac = Fraction(2422, 10000)
        best_cycle = 1
        best_leaps = 0
        best_err = abs(Fraction(0) - solar_frac)
        for q in range(1, 1001):
            p = round(q * solar_frac)
            err = abs(Fraction(p, q) - solar_frac)
            if err < best_err:
                best_err = err
                best_cycle = q
                best_leaps = p

        self.assertEqual(best_cycle, 673)
        self.assertEqual(best_leaps, 163)
        self.assertEqual(best_err, Fraction(3, 3365000))
        self.assertEqual(str(best_cycle), vm_out[0])
        self.assertEqual(f"{best_leaps} day", vm_out[1])
        self.assertEqual(f"{best_err.numerator}/{best_err.denominator} day", vm_out[2])

    def test_even_distribution_both_engines(self):
        source = self.dist_path.read_text(encoding="utf-8")
        tokens = Lexer(source).tokenize()
        program = Parser(tokens).parse()
        SemanticAnalyzer().analyze(program)

        interp = Interpreter(output_fn=lambda s: None)
        interp_out = interp.run(program)

        compiler = Compiler()
        compiled = compiler.compile(program)
        vm = VirtualMachine(output_fn=lambda s: None)
        vm_out = vm.execute(compiled)

        expected = [
            "year 1 extra day:", "0",
            "year 2 extra day:", "0",
            "year 3 extra day:", "0",
            "year 4 extra day:", "1",
        ]
        self.assertEqual(interp_out, expected)
        self.assertEqual(vm_out, expected)


if __name__ == "__main__":
    unittest.main()

"""Full conformance test suite covering Sections 26, 27, and 29 of the DUB.SAR 1.0 Specification."""

import unittest
from pathlib import Path

from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.numbers import parse_number
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer
from dubsar.vm import VirtualMachine


class TestConformance(unittest.TestCase):
    def test_section_29_numbers(self):
        # 1, 60, 1;0, 1;30, 365;14,31,55
        n1 = parse_number("1")
        n60 = parse_number("60")
        n_one = parse_number("1;0")
        n_one_half = parse_number("1;30")
        n_solar = parse_number("365;14,31,55")

        self.assertEqual(n1, 1)
        self.assertEqual(n60, 60)
        self.assertEqual(n_one, 1)
        self.assertEqual(n_one_half.format_sexagesimal(), "1;30")
        self.assertEqual(n_solar.format_sexagesimal(), "365;14,31,55")

    def test_section_29_arithmetic(self):
        # 1;30 + 0;30 = 2
        self.assertEqual(parse_number("1;30") + parse_number("0;30"), 2)
        # 2 * 0;30 = 1
        self.assertEqual(2 * parse_number("0;30"), 1)
        # 3 / 2 = 1;30
        res = parse_number("3") / parse_number("2")
        self.assertEqual(res.format_sexagesimal(), "1;30")

    def test_section_29_exactness(self):
        # Equivalent rational values MUST compare equal regardless of input spelling
        self.assertEqual(parse_number("1.5"), parse_number("1;30"))
        self.assertEqual(parse_number("1.5"), parse_number("3/2") if "/" in "3/2" else 1.5)
        self.assertEqual(parse_number("1"), parse_number("1;0"))
        self.assertEqual(parse_number("0.5"), parse_number("0;30"))

    def test_section_26_planetary_leap_rule_execution(self):
        example_path = Path(__file__).parent.parent / "examples" / "planetary_leap.dub"
        source = example_path.read_text(encoding="utf-8")

        tokens = Lexer(source).tokenize()
        program = Parser(tokens).parse()
        SemanticAnalyzer().analyze(program)

        # Run with Earth-like input Y = 365.2422 (Section 26.3)
        interp = Interpreter(input_fn=lambda p: "365.2422", output_fn=lambda s: None)
        outputs = interp.run(program)

        # Section 70 / Section 26.3 states:
        # cycle = 673, leaps = 163 day, error = 3/3365000 day
        self.assertIn("673", outputs)
        self.assertIn("163 day", outputs)
        self.assertIn("3/3365000 day", outputs)

        # Also test on VM
        compiled = Compiler().compile(program)
        vm = VirtualMachine(input_fn=lambda p: "365.2422", output_fn=lambda s: None)
        vm_outputs = vm.execute(compiled)
        self.assertEqual(outputs, vm_outputs)

    def test_section_27_even_distribution_execution(self):
        example_path = Path(__file__).parent.parent / "examples" / "even_distribution.dub"
        source = example_path.read_text(encoding="utf-8")

        tokens = Lexer(source).tokenize()
        program = Parser(tokens).parse()
        SemanticAnalyzer().analyze(program)

        interp = Interpreter(output_fn=lambda s: None)
        outputs = interp.run(program)

        self.assertEqual(outputs, [
            "year 1 extra day:", "0",
            "year 2 extra day:", "0",
            "year 3 extra day:", "0",
            "year 4 extra day:", "1",
        ])


if __name__ == "__main__":
    unittest.main()

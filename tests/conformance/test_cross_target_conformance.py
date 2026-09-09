"""DUB.SAR 1.0 — Conformance Suite: AST Evaluator vs VM Equivalence (CR-046).

For every semantic test:
AST evaluator result == VM result
must hold exactly using exact rational comparison.
"""

import unittest
from typing import List

from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer
from dubsar.vm import VirtualMachine


class TestCrossTargetConformance(unittest.TestCase):
    """Evaluates programs with both AST Interpreter and Bytecode VM, asserting identical exact results."""

    def _run_both(self, source: str, input_preset: str = "0") -> tuple[List[str], List[str]]:
        tokens = Lexer(source).tokenize()
        program = Parser(tokens).parse()
        SemanticAnalyzer().analyze(program)

        # 1. AST Interpreter
        ast_outputs: List[str] = []
        interp = Interpreter(
            input_fn=lambda prompt: input_preset,
            output_fn=lambda val: ast_outputs.append(str(val)),
            format_mode="canonical",
        )
        interp.run(program)

        # 2. Bytecode VM
        vm_outputs: List[str] = []
        compiler = Compiler()
        compiled = compiler.compile(program)
        vm = VirtualMachine(
            input_fn=lambda prompt: input_preset,
            output_fn=lambda val: vm_outputs.append(str(val)),
            format_mode="canonical",
        )
        vm.execute(compiled)

        return ast_outputs, vm_outputs

    def test_arithmetic_equivalence(self):
        source = """PROBLEM
    a : 1;30
    b : 2
    c := a * b + 0;15
RESULT
    output c
"""
        ast_out, vm_out = self._run_both(source)
        self.assertEqual(ast_out, vm_out)
        self.assertEqual(vm_out, ["3;15"])

    def test_procedure_tuple_unpack_equivalence(self):
        source = """PROBLEM
    x, y := split_halves(10)
procedure split_halves(n):
    h1 := n / 2
    h2 := n - h1
    return h1, h2
RESULT
    output x
    output y
"""
        ast_out, vm_out = self._run_both(source)
        self.assertEqual(ast_out, vm_out)
        self.assertEqual(vm_out, ["5", "5"])

    def test_bounded_repetition_and_conditional(self):
        source = """PROBLEM
    evens : 0
    repeat i 1 to 6:
        if i % 2 == 0:
            evens := evens + 1
RESULT
    output evens
"""
        ast_out, vm_out = self._run_both(source)
        self.assertEqual(ast_out, vm_out)
        self.assertEqual(vm_out, ["3"])

    def test_builtins_equivalence(self):
        source = """PROBLEM
    n1 := nearest(365;14,31,55)
    f1 := floor(365;14,31,55)
    c1 := ceil(365;14,31,55)
    g  := gcd(24, 36)
RESULT
    output n1
    output f1
    output c1
    output g
"""
        ast_out, vm_out = self._run_both(source)
        self.assertEqual(ast_out, vm_out)
        self.assertEqual(vm_out, ["365", "365", "366", "12"])

    def test_units_equivalence(self):
        source = """PROBLEM
    d1 : 5 day
    d2 : 3 day
    sum := d1 + d2
RESULT
    output sum
"""
        ast_out, vm_out = self._run_both(source)
        self.assertEqual(ast_out, vm_out)
        self.assertEqual(vm_out, ["8 day"])


if __name__ == "__main__":
    unittest.main()

"""Tests for Interpreter and Virtual Machine parity."""

import unittest

from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer
from dubsar.vm import VirtualMachine


class TestInterpreterAndVM(unittest.TestCase):
    def _run_both(self, source: str, input_str: str = "0"):
        tokens = Lexer(source).tokenize()
        prog = Parser(tokens).parse()
        SemanticAnalyzer().analyze(prog)

        # Run with Interpreter
        interp = Interpreter(input_fn=lambda p: input_str, output_fn=lambda s: None)
        out_interp = interp.run(prog)

        # Run with VM
        compiled = Compiler().compile(prog)
        vm = VirtualMachine(input_fn=lambda p: input_str, output_fn=lambda s: None)
        out_vm = vm.execute(compiled)

        self.assertEqual(out_interp, out_vm)
        return out_interp

    def test_basic_arithmetic(self):
        source = """PROBLEM
    a : 10
    b : 3
    c := a + b
    d := a - b
    e := a * b
    f := a / b
    g := a % b
RESULT
    output c
    output d
    output e
    output f
    output g
"""
        outputs = self._run_both(source)
        self.assertEqual(outputs, ["13", "7", "30", "3;20", "1"])

    def test_conditionals_and_branches(self):
        source = """PROBLEM
    x : 5
    if x > 3:
        y : 100
    else:
        y : 200
RESULT
    output y
"""
        outputs = self._run_both(source)
        self.assertEqual(outputs, ["100"])

    def test_procedures_and_tuple_unpacking(self):
        source = """PROBLEM
    q, r := divmod(17, 5)

procedure divmod(n, d):
    quot := floor(n / d)
    rem := n % d
    return quot, rem

RESULT
    output q
    output r
"""
        outputs = self._run_both(source)
        self.assertEqual(outputs, ["3", "2"])

    def test_builtins(self):
        source = """PROBLEM
    a := abs(-5)
    f := floor(7 / 2)
    c := ceil(7 / 2)
    n1 := nearest(2.5)
    n2 := nearest(-2.5)
    g := gcd(48, 18)
    l := lcm(12, 15)
RESULT
    output a
    output f
    output c
    output n1
    output n2
    output g
    output l
"""
        outputs = self._run_both(source)
        self.assertEqual(outputs, ["5", "3", "4", "3", "-3", "6", "60"])


if __name__ == "__main__":
    unittest.main()

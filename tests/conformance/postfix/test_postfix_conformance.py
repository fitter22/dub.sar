"""DUB.SAR 1.0 — Postfix Conformance Tests per Section 72."""

import unittest
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.vm import VirtualMachine

class TestPostfixConformance(unittest.TestCase):
    def _run(self, source: str):
        prog = Parser(Lexer(source).tokenize()).parse()
        ast_out = Interpreter().run(prog)
        vm_out = VirtualMachine().execute(Compiler().compile(prog))
        self.assertEqual(ast_out, vm_out)
        return vm_out

    def test_multiline_arithmetic(self):
        source = """problem
    calc :
        10
        2
        divide
        3
        multiply
        1
        add
result
    calc
"""
        out = self._run(source)
        self.assertEqual(out, ["16"])

    def test_single_line_arithmetic(self):
        source = """problem
    calc : 10 2 / 3 * 1 +
result
    calc
"""
        out = self._run(source)
        self.assertEqual(out, ["16"])

    def test_floor_ceil_nearest_abs(self):
        source = """problem
    f : 1;30 floor
    c : 1;30 ceil
    n : 1;30 nearest
    a : -5 absolute
result
    f
    c
    n
    a
"""
        out = self._run(source)
        self.assertEqual(out, ["1", "2", "2", "5"])

if __name__ == "__main__":
    unittest.main()

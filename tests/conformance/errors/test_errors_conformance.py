"""DUB.SAR 1.0 — Errors Conformance Tests per Section 59 & Section 72."""

import unittest
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer
from dubsar.interpreter import Interpreter
from dubsar.errors import (
    DubSarSyntaxError,
    DubSarNameError,
    DubSarUnitError,
    DubSarDivisionByZero,
)

class TestErrorsConformance(unittest.TestCase):
    def test_syntax_error(self):
        source = """problem
    x : : 10
result
    x
"""
        with self.assertRaises(DubSarSyntaxError):
            prog = Parser(Lexer(source).tokenize()).parse()

    def test_name_error(self):
        source = """problem
    x : unknown_var
result
    x
"""
        prog = Parser(Lexer(source).tokenize()).parse()
        with self.assertRaises(DubSarNameError):
            SemanticAnalyzer().analyze(prog)

    def test_unit_error(self):
        source = """problem
    a : 1 day
    b : 1 meter
    c : a b +
result
    c
"""
        prog = Parser(Lexer(source).tokenize()).parse()
        with self.assertRaises(DubSarUnitError):
            SemanticAnalyzer().analyze(prog)

    def test_division_by_zero(self):
        source = """problem
    c : 1 0 /
result
    c
"""
        prog = Parser(Lexer(source).tokenize()).parse()
        with self.assertRaises(DubSarDivisionByZero):
            Interpreter().run(prog)

if __name__ == "__main__":
    unittest.main()

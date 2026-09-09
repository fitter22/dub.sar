"""Tests for Semantic Analyzer."""

import unittest

from dubsar.errors import (
    DubSarNameError,
    DubSarRangeError,
    DubSarReturnError,
    DubSarSyntaxError,
)
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer


class TestSemantic(unittest.TestCase):
    def test_undefined_variable_raises_name_error(self):
        source = """PROBLEM
    a := undefined_var + 1
RESULT
    output a
"""
        prog = Parser(Lexer(source).tokenize()).parse()
        with self.assertRaises(DubSarNameError):
            SemanticAnalyzer().analyze(prog)

    def test_duplicate_procedure_raises_syntax_error(self):
        source = """PROBLEM
    a : 1
procedure calc(x):
    return x
procedure calc(x):
    return x + 1
RESULT
    output a
"""
        prog = Parser(Lexer(source).tokenize()).parse()
        with self.assertRaises(DubSarSyntaxError):
            SemanticAnalyzer().analyze(prog)

    def test_procedure_without_return_raises_return_error(self):
        source = """PROBLEM
    a : 1
procedure no_ret(x):
    y := x + 1
RESULT
    output a
"""
        prog = Parser(Lexer(source).tokenize()).parse()
        with self.assertRaises(DubSarReturnError):
            SemanticAnalyzer().analyze(prog)

    def test_negative_repetition_bound_raises_range_error(self):
        source = """PROBLEM
    repeat i -5:
        output i
RESULT
    output 0
"""
        prog = Parser(Lexer(source).tokenize()).parse()
        with self.assertRaises(DubSarRangeError):
            SemanticAnalyzer().analyze(prog)


if __name__ == "__main__":
    unittest.main()

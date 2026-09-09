"""Tests for AST Parser."""

import unittest

from dubsar.ast import (
    Assignment,
    CallExpr,
    Conditional,
    Declaration,
    NumberLiteral,
    OutputStatement,
    Repetition,
    ReturnStatement,
)
from dubsar.errors import DubSarSyntaxError
from dubsar.lexer import Lexer
from dubsar.parser import Parser


class TestParser(unittest.TestCase):
    def test_basic_tablet_parsing(self):
        source = """PROBLEM
    a : 5
    b := a + 1
RESULT
    output b
"""
        tokens = Lexer(source).tokenize()
        program = Parser(tokens).parse()

        self.assertEqual(len(program.problem.body), 2)
        self.assertIsInstance(program.problem.body[0], Declaration)
        self.assertIsInstance(program.problem.body[1], Assignment)

        self.assertEqual(len(program.result.body), 1)
        self.assertIsInstance(program.result.body[0], OutputStatement)

    def test_procedures_and_tuple_returns(self):
        source = """PROBLEM
    x, y := split(10)

procedure split(val):
    a := val / 2
    b := val - a
    return a, b

RESULT
    output x
"""
        tokens = Lexer(source).tokenize()
        program = Parser(tokens).parse()

        self.assertEqual(len(program.procedures), 1)
        proc = program.procedures[0]
        self.assertEqual(proc.name, "split")
        self.assertEqual(proc.parameters, ["val"])

        # Check return
        ret_stmt = proc.body[-1]
        self.assertIsInstance(ret_stmt, ReturnStatement)
        self.assertEqual(len(ret_stmt.values), 2)

    def test_repetitions_both_forms(self):
        # Single-bound form
        src1 = """PROBLEM
    repeat i 10:
        output i
RESULT
    output 0
"""
        prog1 = Parser(Lexer(src1).tokenize()).parse()
        rep1 = prog1.problem.body[0]
        self.assertIsInstance(rep1, Repetition)
        self.assertIsNone(rep1.start)

        # Explicit-range form
        src2 = """PROBLEM
    repeat i 1 to 10:
        output i
RESULT
    output 0
"""
        prog2 = Parser(Lexer(src2).tokenize()).parse()
        rep2 = prog2.problem.body[0]
        self.assertIsInstance(rep2, Repetition)
        self.assertIsNotNone(rep2.start)


if __name__ == "__main__":
    unittest.main()

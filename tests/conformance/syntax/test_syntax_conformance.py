"""DUB.SAR 1.0 — Syntax Conformance Tests per Section 72."""

import unittest
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.ast import Program, ProblemSection, ResultSection

class TestSyntaxConformance(unittest.TestCase):
    def test_minimal_problem_result(self):
        source = """problem
    x : 10
result
    x
"""
        tokens = Lexer(source).tokenize()
        prog = Parser(tokens).parse()
        self.assertIsInstance(prog, Program)
        self.assertIsInstance(prog.problem, ProblemSection)
        self.assertIsInstance(prog.result, ResultSection)
        self.assertEqual(len(prog.problem.body), 1)
        self.assertEqual(len(prog.result.body), 1)

    def test_cuneiform_structure(self):
        source = """𒂊𒁹
    x : 10
𒅗𒁹
    x
"""
        tokens = Lexer(source).tokenize()
        prog = Parser(tokens).parse()
        self.assertIsInstance(prog, Program)
        self.assertEqual(len(prog.problem.body), 1)
        self.assertEqual(len(prog.result.body), 1)

    def test_multiline_block_indentation(self):
        source = """problem
    calc :
        10
        20
        +
result
    calc
"""
        tokens = Lexer(source).tokenize()
        prog = Parser(tokens).parse()
        self.assertEqual(len(prog.problem.body), 1)

if __name__ == "__main__":
    unittest.main()

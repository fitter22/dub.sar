"""DUB.SAR 1.0 — WASM Conformance Tests per Section 57, 58 & Section 72."""

import unittest
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.wasm import compile_to_wat

class TestWasmConformance(unittest.TestCase):
    def test_wat_generation(self):
        source = """problem
    x : 10
    y : 20
    sum : x y +
result
    sum
"""
        prog = Parser(Lexer(source).tokenize()).parse()
        wat = compile_to_wat(prog)
        self.assertIn("(module", wat)
        self.assertIn('export "run"', wat)
        self.assertIn('memory', wat)

if __name__ == "__main__":
    unittest.main()

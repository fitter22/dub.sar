"""Tests for WebAssembly backend and Tablet Renderer."""

import unittest

from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.renderer import render_svg, render_terminal_tablet
from dubsar.wasm import compile_to_wat


class TestWasmAndRenderer(unittest.TestCase):
    def setUp(self):
        self.source = """PROBLEM
    a : 10
    output "result:"
    output a
RESULT
    output "done"
"""
        tokens = Lexer(self.source).tokenize()
        self.program = Parser(tokens).parse()

    def test_wasm_generation(self):
        wat = compile_to_wat(self.program)
        self.assertIn("(module", wat)
        self.assertIn('$print_str', wat)
        self.assertIn('$print_int', wat)
        self.assertIn('(func (export "run")', wat)

    def test_svg_rendering(self):
        svg = render_svg(self.source, title="TEST TABLET")
        self.assertIn("<svg", svg)
        self.assertIn("</svg>", svg)
        self.assertIn("clayGradient", svg)
        self.assertIn("TEST TABLET", svg)

    def test_terminal_text_rendering(self):
        text = render_terminal_tablet(self.source, title="TERMINAL TABLET")
        self.assertIn("╔", text)
        self.assertIn("╝", text)
        self.assertIn("TERMINAL TABLET", text)


if __name__ == "__main__":
    unittest.main()

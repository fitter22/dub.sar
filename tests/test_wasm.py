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
        self.assertIn('(local.set $a_num)', wat)

    def test_wasm_procedure_and_loop_lowering(self):
        proc_src = """PROBLEM
    total := sum_range(5)
procedure sum_range(n):
    acc : 0
    repeat i 1 to n:
        if i < 3:
            acc := acc + i
    return acc
RESULT
    output total
"""
        tokens = Lexer(proc_src).tokenize()
        prog = Parser(tokens).parse()
        wat = compile_to_wat(prog)
        self.assertIn("(func $sum_range (param $n_num i64) (param $n_den i64) (result i64 i64)", wat)
        self.assertIn("(local $acc_num i64) (local $acc_den i64)", wat)
        self.assertIn("(local $i_num i64) (local $i_den i64)", wat)
        self.assertIn("(block $break_loop_1", wat)
        self.assertIn("(call $rat_add)", wat)
        self.assertIn("(call $rat_cmp)", wat)
        self.assertIn("(if", wat)
        self.assertIn("(call $sum_range)", wat)

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

    def test_render_strip_comments(self):
        source_with_comments = """# Scholar comment
𒑰 Cuneiform comment
PROBLEM
    a : 10
RESULT
    output a
"""
        # Test text renderer
        full_text = render_terminal_tablet(source_with_comments)
        self.assertIn("# Scholar comment", full_text)
        self.assertIn("𒑰 Cuneiform comment", full_text)

        stripped_text = render_terminal_tablet(source_with_comments, strip_comments=True)
        self.assertNotIn("# Scholar comment", stripped_text)
        self.assertNotIn("𒑰 Cuneiform comment", stripped_text)
        self.assertIn("PROBLEM", stripped_text)

        # Test SVG renderer
        full_svg = render_svg(source_with_comments)
        self.assertIn("# Scholar comment", full_svg)
        stripped_svg = render_svg(source_with_comments, strip_comments=True)
        self.assertNotIn("# Scholar comment", stripped_svg)
        self.assertNotIn("𒑰 Cuneiform comment", stripped_svg)


if __name__ == "__main__":
    unittest.main()

"""DUB.SAR 1.0 — Mathematical Tablet Redesign Conformance Suite.

Verifies the mathematical tablet execution model:
- Postfix arithmetic calculations (both multiline and single-line)
- Quantity establishment (name : expr)
- Mathematical determinations and empty sentinels (best : empty, candidate : a, b, c)
- Atomic selection (retain candidate when condition)
- Finite search domains (consider ... from ... through ...)
- Field access (record.field and field of record)
- Implicit inscription in result sections
- Dual-mode compilation equivalence (Scholar mode == Tablet mode) across Interpreter and VM
"""

import unittest
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer
from dubsar.vm import VirtualMachine
from dubsar.wasm import compile_to_wat


class TestRedesignConformance(unittest.TestCase):
    def _run_both(self, source: str, input_str: str = "0"):
        tokens = Lexer(source).tokenize()
        prog = Parser(tokens).parse()
        SemanticAnalyzer().analyze(prog)

        interp = Interpreter(input_fn=lambda p: input_str, output_fn=lambda s: None)
        ast_out = interp.run(prog)

        comp = Compiler().compile(prog)
        vm = VirtualMachine(input_fn=lambda p: input_str, output_fn=lambda s: None)
        vm_out = vm.execute(comp)

        self.assertEqual(ast_out, vm_out)
        return vm_out

    def test_multiline_postfix_and_determinations(self):
        source = """problem
    solar-year : 365;14,31,55 day

    whole-days :
        solar-year
        floor

    fraction :
        solar-year
        whole-days
        subtract

    best : empty

    consider cycle from 1 through 5:
        leaps :
            cycle
            fraction
            multiply
            nearest

        error :
            whole-days
            leaps
            cycle
            divide
            add
            solar-year
            subtract
            absolute

        candidate :
            cycle
            leaps
            error

        retain candidate when error is lesser than best.error

result
    best.cycle
    best.leaps
    best.error
"""
        out = self._run_both(source)
        self.assertEqual(len(out), 3)
        self.assertEqual(out[0], "4")
        self.assertEqual(out[1], "1 day")

    def test_single_line_postfix(self):
        source = """problem
    a : 10
    b : 4
    diff : a b subtract
    prod : a b multiply
    quot : a b divide
result
    diff
    prod
    quot
"""
        out = self._run_both(source)
        self.assertEqual(out, ["6", "40", "2;30"])

    def test_field_of_syntax(self):
        source = """problem
    a : 42
    b : 7
    pair : a, b
    first : a of pair
    second : b of pair
result
    first
    second
"""
        out = self._run_both(source)
        self.assertEqual(out, ["42", "7"])

    def test_cuneiform_tablet_equivalence(self):
        scholar_src = """problem
    x : 10
    y : 20
    candidate : x, y
    best : empty
    retain candidate when best is empty
result
    best
"""
        tablet_src = """𒂊𒁹
    x : 10
    y : 20
    candidate : x, y
    best : 𒉡
    𒋼 candidate 𒂊𒀀 best 𒈨 𒉡
𒅗𒁹
    best
"""
        scholar_out = self._run_both(scholar_src)
        tablet_out = self._run_both(tablet_src)
        self.assertEqual(scholar_out, tablet_out)
        self.assertEqual(scholar_out, ["10", "20"])

    def test_wasm_compilation_of_redesign_features(self):
        source = """problem
    limit : 10
    best : empty
    consider c from 1 through limit:
        candidate : c, limit
        retain candidate when c < 5
result
    best.c
"""
        tokens = Lexer(source).tokenize()
        prog = Parser(tokens).parse()
        wat = compile_to_wat(prog)
        self.assertIn("(module", wat)
        self.assertIn("Make Determination", wat)
        self.assertIn("Retain", wat)


if __name__ == "__main__":
    unittest.main()

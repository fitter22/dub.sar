"""DUB.SAR 1.0 — Determinations Conformance Tests per Section 72."""

import unittest
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.vm import VirtualMachine

class TestDeterminationsConformance(unittest.TestCase):
    def _run(self, source: str):
        prog = Parser(Lexer(source).tokenize()).parse()
        ast_out = Interpreter().run(prog)
        vm_out = VirtualMachine().execute(Compiler().compile(prog))
        self.assertEqual(ast_out, vm_out)
        return vm_out

    def test_empty_sentinel_and_field_access(self):
        source = """problem
    best : empty
    c : 10
    d : 20
    cand :
        c
        d
result
    cand.c
    c of cand
"""
        out = self._run(source)
        self.assertEqual(out, ["10", "10"])

    def test_multi_field_determination(self):
        source = """problem
    a : 1
    b : 2
    res : a, b
result
    res
"""
        out = self._run(source)
        self.assertEqual(out, ["1", "2"])

if __name__ == "__main__":
    unittest.main()

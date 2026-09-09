"""DUB.SAR 1.0 — Retention Conformance Tests per Section 72."""

import unittest
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.vm import VirtualMachine

class TestRetentionConformance(unittest.TestCase):
    def _run(self, source: str):
        prog = Parser(Lexer(source).tokenize()).parse()
        ast_out = Interpreter().run(prog)
        vm_out = VirtualMachine().execute(Compiler().compile(prog))
        self.assertEqual(ast_out, vm_out)
        return vm_out

    def test_atomic_retention_minimum(self):
        source = """problem
    best : empty
    consider val from 1 through 5:
        err : val
        candidate :
            val
            err
        retain candidate when err is lesser than best.err
result
    best.val
"""
        out = self._run(source)
        self.assertEqual(out, ["1"])

    def test_retention_multiline_syntax(self):
        source = """problem
    best : empty
    consider val from 1 through 5:
        err : val
        candidate :
            val
            err
        retain candidate
            when err of candidate
            is lesser than err of best
result
    best.val
"""
        out = self._run(source)
        self.assertEqual(out, ["1"])

if __name__ == "__main__":
    unittest.main()

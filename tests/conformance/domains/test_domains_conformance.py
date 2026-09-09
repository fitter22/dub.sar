"""DUB.SAR 1.0 — Domains Conformance Tests per Section 72."""

import unittest
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.vm import VirtualMachine

class TestDomainsConformance(unittest.TestCase):
    def _run(self, source: str):
        prog = Parser(Lexer(source).tokenize()).parse()
        ast_out = Interpreter().run(prog)
        vm_out = VirtualMachine().execute(Compiler().compile(prog))
        self.assertEqual(ast_out, vm_out)
        return vm_out

    def test_finite_domain_scholar(self):
        source = """problem
    sum : 0
    consider i from 1 through 5:
        next : sum i +
        sum : next
result
    sum
"""
        out = self._run(source)
        self.assertEqual(out, ["15"])

    def test_finite_domain_cuneiform(self):
        source = """𒂊𒁹
    prod : 1
    𒄀 i 𒋫 1 𒂗 4:
        next : prod i *
        prod : next
𒅗𒁹
    prod
"""
        out = self._run(source)
        self.assertEqual(out, ["24"])

if __name__ == "__main__":
    unittest.main()

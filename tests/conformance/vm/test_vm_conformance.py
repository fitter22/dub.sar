"""DUB.SAR 1.0 — VM Conformance Tests per Section 72 & Section 74."""

import unittest
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.vm import VirtualMachine

class TestVmConformance(unittest.TestCase):
    def test_vm_matches_ast_evaluator(self):
        source = """problem
    acc : 0
    consider i from 1 through 10:
        next : acc i +
        acc : next
result
    acc
"""
        prog = Parser(Lexer(source).tokenize()).parse()
        ast_out = Interpreter().run(prog)
        compiled = Compiler().compile(prog)
        vm_out = VirtualMachine().execute(compiled)
        self.assertEqual(ast_out, vm_out)
        self.assertEqual(vm_out, ["55"])

if __name__ == "__main__":
    unittest.main()

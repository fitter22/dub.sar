"""DUB.SAR 1.0 — Input Conformance Tests per Section 72."""

import unittest
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.vm import VirtualMachine

class TestInputConformance(unittest.TestCase):
    def test_ask_input(self):
        source = """problem
    val : ask "enter number:"
    doubled : val 2 *
result
    doubled
"""
        prog = Parser(Lexer(source).tokenize()).parse()
        ast_out = Interpreter(input_fn=lambda p: "1;30").run(prog)
        vm_out = VirtualMachine(input_fn=lambda p: "1;30").execute(Compiler().compile(prog))
        self.assertEqual(ast_out, ["3"])
        self.assertEqual(vm_out, ["3"])

if __name__ == "__main__":
    unittest.main()

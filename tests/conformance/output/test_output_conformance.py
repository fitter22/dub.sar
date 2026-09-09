"""DUB.SAR 1.0 — Output Conformance Tests per Section 72."""

import unittest
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.vm import VirtualMachine

class TestOutputConformance(unittest.TestCase):
    def test_implicit_result_inscription(self):
        source = """problem
    msg : "hello world"
    num : 1;30
result
    msg
    num
"""
        prog = Parser(Lexer(source).tokenize()).parse()
        ast_out = Interpreter().run(prog)
        vm_out = VirtualMachine().execute(Compiler().compile(prog))
        self.assertEqual(ast_out, ["hello world", "1;30"])
        self.assertEqual(vm_out, ["hello world", "1;30"])

    def test_explicit_output_statement(self):
        source = """problem
    num : 42
result
    output num
"""
        prog = Parser(Lexer(source).tokenize()).parse()
        ast_out = Interpreter().run(prog)
        vm_out = VirtualMachine().execute(Compiler().compile(prog))
        self.assertEqual(ast_out, ["42"])
        self.assertEqual(vm_out, ["42"])

if __name__ == "__main__":
    unittest.main()

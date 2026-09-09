"""DUB.SAR 1.0 — Recipes Conformance Tests per Section 72."""

import unittest
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.vm import VirtualMachine

class TestRecipesConformance(unittest.TestCase):
    def _run(self, source: str):
        prog = Parser(Lexer(source).tokenize()).parse()
        ast_out = Interpreter().run(prog)
        vm_out = VirtualMachine().execute(Compiler().compile(prog))
        self.assertEqual(ast_out, vm_out)
        return vm_out

    def test_recipe_definition_and_application(self):
        source = """problem
    val :
        5
        3
        apply double-sum

recipe double-sum a b:
    s : a b +
    res : s 2 *
    determine res

result
    val
"""
        out = self._run(source)
        self.assertEqual(out, ["16"])

    def test_cuneiform_recipe_ak(self):
        source = """𒂊𒁹
    val :
        4
        2
        𒀝 multiply-by-two

𒁾𒊬 multiply-by-two x y:
    res : x y *
    𒉆 res

𒅗𒁹
    val
"""
        out = self._run(source)
        self.assertEqual(out, ["8"])

if __name__ == "__main__":
    unittest.main()

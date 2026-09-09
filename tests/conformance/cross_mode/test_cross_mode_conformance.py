"""DUB.SAR 1.0 — Cross-Mode Conformance Tests per Section 72 & Section 73."""

import unittest
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.vm import VirtualMachine

class TestCrossModeConformance(unittest.TestCase):
    def test_tablet_and_scholar_equivalence(self):
        tablet_source = """𒂊𒁹
    a : 1;30
    b : 0;30
    sum :
        a
        b
        𒍣
𒅗𒁹
    sum
"""
        scholar_source = """problem
    a : 1;30
    b : 0;30
    sum :
        a
        b
        add
result
    sum
"""
        prog_tab = Parser(Lexer(tablet_source).tokenize()).parse()
        prog_sch = Parser(Lexer(scholar_source).tokenize()).parse()

        out_tab_ast = Interpreter().run(prog_tab)
        out_sch_ast = Interpreter().run(prog_sch)
        out_tab_vm = VirtualMachine().execute(Compiler().compile(prog_tab))
        out_sch_vm = VirtualMachine().execute(Compiler().compile(prog_sch))

        self.assertEqual(out_tab_ast, out_sch_ast)
        self.assertEqual(out_tab_vm, out_sch_vm)
        self.assertEqual(out_tab_ast, out_tab_vm)
        self.assertEqual(out_tab_ast, ["2"])

if __name__ == "__main__":
    unittest.main()

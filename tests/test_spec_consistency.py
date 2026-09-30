"""Conformance checks for the specification decisions in issues 29-32."""

from __future__ import annotations

import shutil
import unittest

from dubsar.errors import DubSarMathError, DubSarSyntaxError, DubSarUnitError
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.normalizer import cuneiformize, transliterate
from dubsar.parser import Parser
from dubsar.tokens import TokenType
from dubsar.vm import VirtualMachine
from dubsar.wasm import compile_to_wat


def run(src: str) -> list[str]:
    ast = Parser(Lexer(src).tokenize()).parse()
    return Interpreter().run(ast)


class TestPositionRules(unittest.TestCase):
    def test_iti_and_cuneiform_month_follow_a_number(self) -> None:
        self.assertEqual(run("problem\n    m : 24 iti\nresult\n    m\n"), ["24 month"])
        self.assertEqual(run("problem\n    m : 24 𒌗\nresult\n    m\n"), ["24 𒌗"])

    def test_gi_after_a_number_is_a_reed(self) -> None:
        self.assertEqual(run("problem\n    r : 2 gi\nresult\n    r\n"), ["2 gi"])

    def test_through_inside_consider_is_not_a_month(self) -> None:
        out = run(
            "problem\n"
            "    total : 0\n"
            "    consider n from 1 through 3:\n"
            "        total : total + n\n"
            "result\n"
            "    total\n"
        )
        self.assertEqual(out, ["6"])

    def test_nu_and_cuneiform_empty_are_the_same_token(self) -> None:
        nu = [t for t in Lexer("nu").tokenize() if t.type != TokenType.EOF][0]
        cun = [t for t in Lexer("𒉡").tokenize() if t.type != TokenType.EOF][0]
        self.assertEqual(nu.type, TokenType.EMPTY)
        self.assertEqual(cun.type, TokenType.EMPTY)
        self.assertEqual(run("problem\n    best : nu\nresult\n    best\n"), ["empty"])

    def test_mash_sign_can_name_a_quantity(self) -> None:
        # 𒈦 is an identifier. Reciprocal tablets use it as a quantity name.
        self.assertEqual(
            run("problem\n    𒈦 : 0;30\nresult\n    𒈦\n"),
            ["0;30"],
        )

    def test_retain_sign_still_selects_and_pipeline_sign_is_absolute(self) -> None:
        out = run(
            "problem\n"
            "    best : empty\n"
            "    consider n from 1 through 3:\n"
            "        retain n when n > 1\n"
            "    mag :\n"
            "        -4\n"
            "        𒋼\n"
            "result\n"
            "    best\n"
            "    mag\n"
        )
        self.assertEqual(out, ["3", "4"])

    def test_unconsumed_token_is_a_syntax_error(self) -> None:
        with self.assertRaises(DubSarSyntaxError):
            run("problem\n    m : 24 iti leftover\nresult\n    m\n")


class TestExactnessAndUnits(unittest.TestCase):
    def test_square_root_of_a_non_square_errors(self) -> None:
        with self.assertRaises(DubSarMathError):
            run("problem\n    r : 2 square-root\nresult\n    r\n")

    def test_square_root_call_of_a_square(self) -> None:
        self.assertEqual(run("problem\n    r : square-root(9)\nresult\n    r\n"), ["3"])

    def test_nearest_keeps_the_unit(self) -> None:
        self.assertEqual(run("problem\n    n : 2;30 day nearest\nresult\n    n\n"), ["3 day"])

    def test_meter_does_not_add_to_the_cubit(self) -> None:
        with self.assertRaises(DubSarUnitError):
            run("problem\n    s : 1 meter + 1 kus\nresult\n    s\n")

    def test_shekel_is_the_mass_base(self) -> None:
        src = "problem\n    b :\n        convert(1 mina, \"shekel\")\nresult\n    b\n"
        self.assertEqual(run(src), ["60 shekel"])

    def test_feed_is_run_over_rise(self) -> None:
        self.assertEqual(run("problem\n    f : 1 2 feed\nresult\n    f\n"), ["2"])

    def test_keywords_are_case_insensitive(self) -> None:
        self.assertEqual(run("PROBLEM\n    n : 1\nRESULT\n    n\n"), ["1"])


EXACT_ROOT = "problem\n    r : square-root(9)\nresult\n    r\n"
NON_SQUARE = "problem\n    r : 2 square-root\nresult\n    r\n"
METER_ROOT = "problem\n    area : 3 meter square\n    side : area square-root\nresult\n    side\n"
APPROX = "problem\n    a : 2 approximate\nresult\n    a\n"


class TestBackendAgreement(unittest.TestCase):
    def test_vm_matches_exact_square_root(self) -> None:
        ast = Parser(Lexer(EXACT_ROOT).tokenize()).parse()
        self.assertEqual(VirtualMachine().execute(Compiler().compile(ast)), ["3"])

    def test_vm_rejects_a_non_square(self) -> None:
        ast = Parser(Lexer(NON_SQUARE).tokenize()).parse()
        with self.assertRaises(DubSarMathError):
            VirtualMachine().execute(Compiler().compile(ast))

    def test_wasm_lowers_square_root_to_the_exact_helper(self) -> None:
        ast = Parser(Lexer(EXACT_ROOT).tokenize()).parse()
        wat = compile_to_wat(ast)
        self.assertIn("$rat_sqrt_exact", wat)
        self.assertIn("(call $rat_sqrt_exact)", wat)

    def test_not_stays_a_scholar_word(self) -> None:
        cun = cuneiformize("not")
        self.assertIn("not", cun)
        self.assertNotIn("𒉡", cun)

    def test_retain_and_absolute_round_trip(self) -> None:
        tablet = "    𒋼 best when x is greater than best\n    x 𒋼\n"
        scholar = transliterate(tablet)
        self.assertIn("retain best", scholar)
        self.assertIn("absolute", scholar)
        again = transliterate(cuneiformize(scholar))
        self.assertIn("retain best", again)
        self.assertIn("absolute", again)


class TestNativeExactness(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not (shutil.which("clang") or shutil.which("gcc") or shutil.which("cc")):
            raise unittest.SkipTest("No host C compiler available.")
        from dubsar.native.compiler import NativeCompiler
        cls.compiler = NativeCompiler()

    def _run(self, source: str) -> list[str]:
        ast = Parser(Lexer(source).tokenize()).parse()
        code, out, err = self.compiler.run(ast)
        self.assertEqual(code, 0, err)
        return out

    def test_prefix_square_root_is_exact(self) -> None:
        self.assertEqual(self._run(EXACT_ROOT), ["3"])

    def test_square_root_keeps_a_squared_unit(self) -> None:
        self.assertEqual(self._run(METER_ROOT), ["3 meter"])

    def test_approximate_is_marked(self) -> None:
        self.assertEqual(self._run(APPROX), ["~2"])

    def test_non_square_exits(self) -> None:
        ast = Parser(Lexer(NON_SQUARE).tokenize()).parse()
        code, _out, err = self.compiler.run(ast)
        self.assertNotEqual(code, 0)
        self.assertIn("exact rational square", err)


if __name__ == "__main__":
    unittest.main()

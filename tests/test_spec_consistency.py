"""Conformance checks for the specification decisions in issues 29-32."""

from __future__ import annotations

import unittest

from dubsar.errors import DubSarMathError, DubSarSyntaxError, DubSarUnitError
from dubsar.interpreter import Interpreter
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.tokens import TokenType


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


if __name__ == "__main__":
    unittest.main()

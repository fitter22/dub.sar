"""Tests for transliteration and cuneiform normalizer."""

import unittest

from dubsar.lexer import Lexer
from dubsar.normalizer import cuneiformize, transliterate
from dubsar.parser import Parser


class TestNormalizer(unittest.TestCase):
    def test_transliterate_cuneiform_to_scholar(self):
        cun_src = """𒂊𒁹
    𒈬 : 365 𒌓
    cycle : 1
    𒂊𒀀 cycle < 10:
        cycle := cycle + 1
    𒄑 cycle
𒅗𒁹
    𒁹𒀀 cycle
"""
        scholar_src = transliterate(cun_src)
        self.assertIn("PROBLEM", scholar_src)
        self.assertIn("day", scholar_src)
        self.assertIn("if", scholar_src)
        self.assertIn("return", scholar_src)
        self.assertIn("RESULT", scholar_src)
        self.assertIn("output", scholar_src)

        # Ensure transliterated source is valid and parses
        tokens = Lexer(scholar_src).tokenize()
        prog = Parser(tokens).parse()
        self.assertEqual(len(prog.problem.body), 4)

    def test_cuneiformize_scholar_to_cuneiform(self):
        scholar_src = """PROBLEM
    mu : 365 day
    repeat cycle 1 to 10:
        output cycle
RESULT
    output mu
"""
        cun_src = cuneiformize(scholar_src)
        self.assertIn("𒂊𒁹", cun_src)
        self.assertIn("𒌓", cun_src)
        self.assertIn("𒄀", cun_src)
        self.assertIn("𒁹𒀀", cun_src)
        self.assertIn("𒅗𒁹", cun_src)

        tokens = Lexer(cun_src).tokenize()
        prog = Parser(tokens).parse()
        self.assertEqual(len(prog.problem.body), 2)


if __name__ == "__main__":
    unittest.main()

"""Tests for Tablet Mode genuine cuneiform representation, identifier rules, and string literal preservation.

Covers Issue #13:
- Authentic / symbolic cuneiform identifiers without Latin tokens
- String literals as data preserving arbitrary Unicode (modern text, cuneiform, international scripts)
- Bidirectional Scholar <-> Tablet round-trip conversion
- AST and execution equivalence across engines
"""

import unittest
from pathlib import Path

from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.normalizer import (
    cuneiformize,
    transliterate,
)
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer
from dubsar.vm import VirtualMachine


class TestTabletMode(unittest.TestCase):
    """Test suite for genuine cuneiform Tablet Mode syntax and string preservation."""

    def test_unicode_strings_preserved_in_both_directions(self):
        """String literals must remain untouched in both transliterate and cuneiformize."""
        test_strings = [
            '"365.2422"',
            '"solar year in days"',
            '"𒀭𒂗𒆠"',
            '"こんにちは"',
            '"value with # and 𒑰 comment-like symbols"',
            '"problem recipe result when consider"',
        ]

        for s in test_strings:
            scholar_source = f"""problem
    txt : {s}
result
    output txt
"""
            cun_source = cuneiformize(scholar_source)
            self.assertIn(s, cun_source, f"cuneiformize corrupted string literal {s}")

            round_trip_scholar = transliterate(cun_source)
            self.assertIn(s, round_trip_scholar, f"transliterate corrupted string literal {s}")

    def test_genuine_cuneiform_lexing_and_execution(self):
        """Genuine cuneiform program with zero Latin identifiers executes correctly."""
        tablet_source = """𒑰 Pure cuneiform tablet program
𒂊𒁹
    𒊕 : 10
    𒅎 : 20
    𒁇 := 𒊕 + 𒅎
𒅗𒁹
    𒁹𒀀 "sum is:"
    𒁹𒀀 𒁇
"""
        tokens = Lexer(tablet_source).tokenize()
        ident_tokens = [t.value for t in tokens if t.type.name == "IDENTIFIER"]
        # Ensure all identifiers are authentic cuneiform
        for ident in ident_tokens:
            self.assertTrue(
                all(0x12000 <= ord(c) <= 0x1254F for c in ident),
                f"Identifier {ident} should be pure cuneiform",
            )

        program = Parser(tokens).parse()
        SemanticAnalyzer().analyze(program)
        out = Interpreter(output_fn=lambda s: None).run(program)
        self.assertEqual(out, ["sum is:", "30"])

    def test_multi_sign_cuneiform_identifiers_not_split(self):
        """Compound cuneiform words like 𒈬𒁶 and 𒅆𒁀 must be tokenized as single identifiers."""
        tablet_source = """𒂊𒁹
    𒈬𒁶 : 42
    𒅆𒁀 : 100
    res : 𒈬𒁶 + 𒅆𒁀
𒅗𒁹
    res
"""
        tokens = Lexer(tablet_source).tokenize()
        idents = [t.value for t in tokens if t.type.name == "IDENTIFIER"]
        self.assertIn("𒈬𒁶", idents)
        self.assertIn("𒅆𒁀", idents)

        program = Parser(tokens).parse()
        SemanticAnalyzer().analyze(program)
        out = Interpreter(output_fn=lambda s: None).run(program)
        self.assertEqual(out, ["142"])

    def test_domain_loop_with_cuneiform_identifiers(self):
        """Domain repetition 𒄀 𒁄 𒋫 1 𒂗 𒍠 transliterates to consider ... from ... through."""
        tablet_snippet = "    𒄀 𒁄 𒋫 1 𒂗 𒍠:\n        x : 𒁄"
        scholar = transliterate(tablet_snippet, identifier_map={"𒁄": "cycle", "𒍠": "limit"})
        self.assertIn("consider cycle from 1 through limit:", scholar)

    def test_retain_statement_with_cuneiform_identifiers(self):
        """Retain statement 𒋼 𒊮 transliterates to retain ..."""
        tablet_snippet = "    𒋼 𒊮\n        𒂊𒀀 𒇲 𒊭 𒊮\n        𒈨 𒌉 𒋫 𒇲 𒊭 𒊕"
        scholar = transliterate(
            tablet_snippet,
            identifier_map={"𒊮": "candidate", "𒇲": "error", "𒊕": "best"},
        )
        self.assertIn("retain candidate", scholar)
        self.assertIn("when error of candidate", scholar)
        self.assertIn("is lesser than error of best", scholar)

    def test_flagship_planetary_leap_round_trip(self):
        """Planetary leap example round-trips cleanly between Scholar and Tablet forms."""
        repo_root = Path(__file__).parent.parent
        scholar_path = repo_root / "examples" / "planetary_leap_scholar.dub"
        tablet_path = repo_root / "examples" / "planetary_leap.dub"

        scholar_src = scholar_path.read_text(encoding="utf-8")
        tablet_src = tablet_path.read_text(encoding="utf-8")

        # Cuneiformize scholar source using canonical identifier mappings
        cun_generated = cuneiformize(scholar_src, use_canonical_identifiers=True)
        tokens = Lexer(cun_generated).tokenize()
        prog = Parser(tokens).parse()
        SemanticAnalyzer().analyze(prog)
        out = Interpreter(input_fn=lambda p: "365.2422", output_fn=lambda s: None).run(prog)
        self.assertIn("673", out)
        self.assertIn("163 day", out)
        self.assertIn("3/3365000 day", out)

        # Transliterate tablet source back to scholar mode
        trans_scholar = transliterate(tablet_src, use_canonical_identifiers=True)
        tokens_tr = Lexer(trans_scholar).tokenize()
        prog_tr = Parser(tokens_tr).parse()
        SemanticAnalyzer().analyze(prog_tr)
        out_tr = Interpreter(input_fn=lambda p: "365.2422", output_fn=lambda s: None).run(prog_tr)
        self.assertEqual(out, out_tr)

    def test_flagship_babylonian_sqrt2_execution(self):
        """Babylonian sqrt2 tablet example executes identically in interpreter and VM."""
        repo_root = Path(__file__).parent.parent
        tablet_path = repo_root / "examples" / "babylonian_sqrt2.dub"
        tablet_src = tablet_path.read_text(encoding="utf-8")

        tokens = Lexer(tablet_src).tokenize()
        prog = Parser(tokens).parse()
        SemanticAnalyzer().analyze(prog)

        interp_out = Interpreter(output_fn=lambda s: None).run(prog)
        compiled = Compiler().compile(prog)
        vm_out = VirtualMachine(output_fn=lambda s: None).execute(compiled)

        self.assertEqual(interp_out, vm_out)
        self.assertIn("Babylonian sqrt(2) approximation:", interp_out)
        self.assertIn("Square with side 30 has diagonal:", interp_out)

    def test_flagship_even_distribution_execution(self):
        """Even distribution tablet example executes identically in interpreter and VM."""
        repo_root = Path(__file__).parent.parent
        tablet_path = repo_root / "examples" / "even_distribution.dub"
        tablet_src = tablet_path.read_text(encoding="utf-8")

        tokens = Lexer(tablet_src).tokenize()
        prog = Parser(tokens).parse()
        SemanticAnalyzer().analyze(prog)

        interp_out = Interpreter(output_fn=lambda s: None).run(prog)
        compiled = Compiler().compile(prog)
        vm_out = VirtualMachine(output_fn=lambda s: None).execute(compiled)

        expected = [
            "year 1 extra day:",
            "0",
            "year 2 extra day:",
            "0",
            "year 3 extra day:",
            "0",
            "year 4 extra day:",
            "1",
        ]
        self.assertEqual(interp_out, expected)
        self.assertEqual(vm_out, expected)

    def test_flagship_reciprocal_lookup_execution(self):
        """Reciprocal lookup tablet example executes with cuneiform identifiers."""
        repo_root = Path(__file__).parent.parent
        tablet_path = repo_root / "examples" / "reciprocal_lookup.dub"
        tablet_src = tablet_path.read_text(encoding="utf-8")

        tokens = Lexer(tablet_src).tokenize()
        prog = Parser(tokens).parse()
        SemanticAnalyzer().analyze(prog)

        interp_out = Interpreter(output_fn=lambda s: None).run(prog)
        self.assertEqual(interp_out, ["0;7,30", "3;45"])


if __name__ == "__main__":
    unittest.main()

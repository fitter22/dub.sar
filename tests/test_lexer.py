"""Tests for Lexer and Tokenizer."""

import unittest

from dubsar.errors import DubSarSyntaxError
from dubsar.lexer import Lexer
from dubsar.tokens import TokenType


class TestLexer(unittest.TestCase):
    def test_cuneiform_tokens(self):
        source = "𒂊𒁹 𒁾𒊬 𒅗𒁹 𒂊𒀀 𒉡𒂊𒀀 𒄀 𒄑 𒁹𒀀 𒀀𒁹"
        tokens = Lexer(source).tokenize()
        expected = [
            TokenType.PROBLEM,
            TokenType.PROCEDURE,
            TokenType.RESULT,
            TokenType.IF,
            TokenType.ELSE,
            TokenType.REPEAT,
            TokenType.RETURN,
            TokenType.OUTPUT,
            TokenType.INPUT,
            TokenType.NEWLINE,
            TokenType.EOF,
        ]
        self.assertEqual([t.type for t in tokens], expected)

    def test_scholar_tokens(self):
        source = "PROBLEM procedure RESULT if else repeat return output input"
        tokens = Lexer(source).tokenize()
        expected = [
            TokenType.PROBLEM,
            TokenType.PROCEDURE,
            TokenType.RESULT,
            TokenType.IF,
            TokenType.ELSE,
            TokenType.REPEAT,
            TokenType.RETURN,
            TokenType.OUTPUT,
            TokenType.INPUT,
            TokenType.NEWLINE,
            TokenType.EOF,
        ]
        self.assertEqual([t.type for t in tokens], expected)

    def test_operators(self):
        source = "+ - * / % ** == != < <= > >= := : ,"
        tokens = Lexer(source).tokenize()
        types = [t.type for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
        expected = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.STAR,
            TokenType.SLASH,
            TokenType.MOD,
            TokenType.POW,
            TokenType.EQ,
            TokenType.NEQ,
            TokenType.LT,
            TokenType.LTE,
            TokenType.GT,
            TokenType.GTE,
            TokenType.ASSIGN,
            TokenType.COLON,
            TokenType.COMMA,
        ]
        self.assertEqual(types, expected)

    def test_indentation_tracking(self):
        source = """PROBLEM
    a : 1
    if a == 1:
        b : 2
    c : 3
"""
        tokens = Lexer(source).tokenize()
        tok_types = [t.type for t in tokens]
        self.assertIn(TokenType.INDENT, tok_types)
        self.assertIn(TokenType.DEDENT, tok_types)

    def test_comments(self):
        source = """# Scholar comment
PROBLEM
    x : 10 𒑰 Tablet comment
"""
        tokens = Lexer(source).tokenize()
        idents = [t.value for t in tokens if t.type == TokenType.IDENTIFIER]
        self.assertEqual(idents, ["x"])

    def test_kebab_case_identifiers(self):
        source = "maximum-cycle := best-cycle - 1"
        tokens = Lexer(source).tokenize()
        idents = [t.value for t in tokens if t.type == TokenType.IDENTIFIER]
        self.assertEqual(idents, ["maximum-cycle", "best-cycle"])


if __name__ == "__main__":
    unittest.main()

"""DUB.SAR 1.0 — Lexer.

Implements Sections 2, 3, and 4:
- Significant indentation (INDENT, DEDENT, NEWLINE)
- Tablet mode (cuneiform), Scholar mode (ASCII/Latin), Mixed mode
- Comments: # (Scholar) and 𒑰 (Tablet)
- Canonical cuneiform vocabulary and Scholar aliases
- Canonical sexagesimal numbers (integer;d1,d2,...), integers, floats, cuneiform numerals
- Strings and escape sequences
- Identifiers with kebab-case support ([A-Za-z_][A-Za-z0-9_-]*) and cuneiform signs
"""

from __future__ import annotations

import re
from typing import Iterator, List, Optional

from dubsar.errors import DubSarSyntaxError
from dubsar.numbers import DUB_SAR_NUMERAL_TABLE, parse_number
from dubsar.tokens import (
    CUNEIFORM_KEYWORDS,
    SCHOLAR_KEYWORDS,
    Token,
    TokenType,
)


class Lexer:
    """Unicode Lexer with indentation handling for DUB.SAR 1.0."""

    def __init__(self, source: str, source_file: Optional[str] = None) -> None:
        self.source = source
        self.source_file = source_file
        self.length = len(source)
        self.pos = 0
        self.line = 1
        self.col = 1
        self.indent_stack: List[int] = [0]
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        """Tokenizes the entire source and returns a list of Tokens."""
        # Process line by line to handle indentation cleanly
        lines = self.source.splitlines(keepends=True)
        tokens: List[Token] = []
        indent_stack: List[int] = [0]

        line_num = 1
        for raw_line in lines:
            # Strip newline characters for indent calculation
            line_content = raw_line.rstrip("\r\n")

            # Check indentation and content
            # Expand tabs to 4 spaces if any
            expanded = line_content.expandtabs(4)
            stripped = expanded.strip()

            # Check if line is empty or comment-only
            if not stripped or stripped.startswith("#") or stripped.startswith("𒑰"):
                line_num += 1
                continue

            # Calculate indentation level (number of leading spaces)
            indent_level = len(expanded) - len(expanded.lstrip(" "))

            # Handle indent / dedent
            current_indent = indent_stack[-1]
            if indent_level > current_indent:
                indent_stack.append(indent_level)
                tokens.append(Token(TokenType.INDENT, indent_level, line_num, 1, "INDENT"))
            elif indent_level < current_indent:
                while indent_stack and indent_stack[-1] > indent_level:
                    indent_stack.pop()
                    tokens.append(Token(TokenType.DEDENT, indent_level, line_num, 1, "DEDENT"))
                if not indent_stack or indent_stack[-1] != indent_level:
                    raise DubSarSyntaxError(
                        f"Inconsistent indentation: level {indent_level} does not match any outer indentation level",
                        line=line_num,
                        col=1,
                        source_file=self.source_file,
                    )

            # Tokenize the line content (starting after leading spaces)
            leading_spaces = len(raw_line) - len(raw_line.lstrip(" \t"))
            line_tokens = self._tokenize_line(raw_line[leading_spaces:], line_num, leading_spaces + 1)
            tokens.extend(line_tokens)

            # Emit NEWLINE at the end of every non-empty logical line
            tokens.append(Token(TokenType.NEWLINE, "\n", line_num, len(line_content) + 1, "NEWLINE"))
            line_num += 1

        # At EOF, emit DEDENT for each remaining indent level > 0
        while len(indent_stack) > 1:
            indent_stack.pop()
            tokens.append(Token(TokenType.DEDENT, 0, line_num, 1, "DEDENT"))

        tokens.append(Token(TokenType.EOF, "", line_num, 1, "EOF"))
        self.tokens = tokens
        return tokens

    def _tokenize_line(self, line: str, line_num: int, start_col: int) -> List[Token]:
        tokens: List[Token] = []
        i = 0
        n = len(line)

        while i < n:
            ch = line[i]
            col = start_col + i

            # Whitespace
            if ch in (" ", "\t", "\r", "\n"):
                i += 1
                continue

            # Comments: Scholar (#) or Tablet (𒑰)
            if ch in ("#", "𒑰"):
                # Rest of line is comment
                break

            # Two-character operators & punctuation
            two_ch = line[i : i + 2]
            if two_ch == ":=":
                tokens.append(Token(TokenType.ASSIGN, ":=", line_num, col))
                i += 2
                continue
            if two_ch == "**":
                tokens.append(Token(TokenType.POW, "**", line_num, col))
                i += 2
                continue
            if two_ch == "==":
                tokens.append(Token(TokenType.EQ, "==", line_num, col))
                i += 2
                continue
            if two_ch == "!=":
                tokens.append(Token(TokenType.NEQ, "!=", line_num, col))
                i += 2
                continue
            if two_ch == "<=":
                tokens.append(Token(TokenType.LTE, "<=", line_num, col))
                i += 2
                continue
            if two_ch == ">=":
                tokens.append(Token(TokenType.GTE, ">=", line_num, col))
                i += 2
                continue
            if two_ch == "..":
                tokens.append(Token(TokenType.RANGE_SEP, "..", line_num, col))
                i += 2
                continue

            # Single-character operators & punctuation
            if ch == ":":
                tokens.append(Token(TokenType.COLON, ":", line_num, col))
                i += 1
                continue
            if ch == ",":
                tokens.append(Token(TokenType.COMMA, ",", line_num, col))
                i += 1
                continue
            if ch == "(":
                tokens.append(Token(TokenType.LPAREN, "(", line_num, col))
                i += 1
                continue
            if ch == ")":
                tokens.append(Token(TokenType.RPAREN, ")", line_num, col))
                i += 1
                continue
            if ch == "+":
                tokens.append(Token(TokenType.PLUS, "+", line_num, col))
                i += 1
                continue
            if ch == "-":
                # Check if it is a negative number literal e.g. -1;30 or -5
                # Negative literal occurs if preceded by an operator, LPAREN, COMMA, ASSIGN, COLON, or start of line
                prev_is_op = (
                    not tokens
                    or tokens[-1].type
                    in (
                        TokenType.ASSIGN,
                        TokenType.COLON,
                        TokenType.COMMA,
                        TokenType.LPAREN,
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
                        TokenType.RETURN,
                        TokenType.OUTPUT,
                        TokenType.IF,
                        TokenType.RANGE_SEP,
                    )
                )
                if prev_is_op and i + 1 < n and (line[i + 1].isdigit() or self._is_cuneiform_digit(line[i + 1])):
                    # Parse as negative number
                    num_tok, consumed = self._scan_number(line[i:], line_num, col)
                    tokens.append(num_tok)
                    i += consumed
                    continue

                tokens.append(Token(TokenType.MINUS, "-", line_num, col))
                i += 1
                continue
            if ch == "*":
                tokens.append(Token(TokenType.STAR, "*", line_num, col))
                i += 1
                continue
            if ch == "/":
                tokens.append(Token(TokenType.SLASH, "/", line_num, col))
                i += 1
                continue
            if ch == "%":
                tokens.append(Token(TokenType.MOD, "%", line_num, col))
                i += 1
                continue
            if ch == "<":
                tokens.append(Token(TokenType.LT, "<", line_num, col))
                i += 1
                continue
            if ch == ">":
                tokens.append(Token(TokenType.GT, ">", line_num, col))
                i += 1
                continue

            # Strings: "..." or '...'
            if ch in ('"', "'"):
                quote = ch
                start_i = i
                i += 1
                chars = []
                while i < n and line[i] != quote:
                    if line[i] == "\\" and i + 1 < n:
                        esc = line[i + 1]
                        if esc == "n":
                            chars.append("\n")
                        elif esc == "t":
                            chars.append("\t")
                        elif esc == quote:
                            chars.append(quote)
                        elif esc == "\\":
                            chars.append("\\")
                        else:
                            chars.append(esc)
                        i += 2
                    else:
                        chars.append(line[i])
                        i += 1
                if i >= n or line[i] != quote:
                    raise DubSarSyntaxError(
                        "Unterminated string literal",
                        line=line_num,
                        col=col,
                        source_file=self.source_file,
                    )
                i += 1  # skip closing quote
                val = "".join(chars)
                tokens.append(Token(TokenType.STRING, val, line_num, col, raw=line[start_i:i]))
                continue

            # Cuneiform multi-sign tokens first (e.g. 𒉡𒂊𒀀, 𒂊𒁹, 𒁾𒊬, 𒅗𒁹, etc.)
            matched_cun = False
            for length in (3, 2, 1):
                if i + length <= n:
                    sub = line[i : i + length]
                    if sub in CUNEIFORM_KEYWORDS:
                        tok_type = CUNEIFORM_KEYWORDS[sub]
                        tokens.append(Token(tok_type, sub, line_num, col))
                        i += length
                        matched_cun = True
                        break
            if matched_cun:
                continue

            # Numbers (integer, sexagesimal, decimal, or cuneiform numerals)
            if ch.isdigit() or (self._is_cuneiform_digit(ch) and not self._is_cuneiform_ident_start(line[i:])):
                num_tok, consumed = self._scan_number(line[i:], line_num, col)
                tokens.append(num_tok)
                i += consumed
                continue

            # Identifiers (ASCII or Cuneiform)
            ident_tok, consumed = self._scan_identifier(line[i:], line_num, col)
            if ident_tok:
                tokens.append(ident_tok)
                i += consumed
                continue

            raise DubSarSyntaxError(
                f"Unexpected character: {ch!r} (U+{ord(ch):04X})",
                line=line_num,
                col=col,
                source_file=self.source_file,
            )

        return tokens

    def _is_cuneiform_digit(self, ch: str) -> bool:
        return ch in DUB_SAR_NUMERAL_TABLE

    def _is_cuneiform_ident_start(self, text: str) -> bool:
        # If it's a known cuneiform word like 𒈬 or 𒌓, it's an identifier/unit rather than number
        if text.startswith("𒈬") or text.startswith("𒌓"):
            return True
        return False

    def _scan_number(self, text: str, line_num: int, col: int) -> tuple[Token, int]:
        """Scans a number: integer, sexagesimal (integer;d1,d2,...), float, or cuneiform number."""
        i = 0
        n = len(text)

        # Optional sign
        if text[0] in ("+", "-"):
            i += 1

        # Scan integer part
        if i < n and text[i].isdigit():
            while i < n and text[i].isdigit():
                i += 1

            # Check for sexagesimal separator ';' or '𒑱'
            if i < n and text[i] in (";", "𒑱"):
                i += 1
                # Scan fractional digits separated by commas
                while i < n and (text[i].isdigit() or text[i] in (",", " ")):
                    i += 1
                num_str = text[:i].strip()
                # Parse exact rational
                rat = parse_number(num_str)
                return Token(TokenType.NUMBER, rat, line_num, col, raw=num_str), i

            # Check for decimal point '.'
            if i < n and text[i] == "." and (i + 1 >= n or text[i + 1] != "."):
                i += 1
                while i < n and text[i].isdigit():
                    i += 1
                num_str = text[:i].strip()
                rat = parse_number(num_str)
                return Token(TokenType.NUMBER, rat, line_num, col, raw=num_str), i

            # Just integer
            num_str = text[:i].strip()
            rat = parse_number(num_str)
            return Token(TokenType.NUMBER, rat, line_num, col, raw=num_str), i

        # Scan cuneiform numerals
        while i < n and (text[i] in DUB_SAR_NUMERAL_TABLE or text[i] in (";", "𒑱", ",")):
            i += 1

        if i > 0:
            num_str = text[:i].strip()
            rat = parse_number(num_str)
            return Token(TokenType.NUMBER, rat, line_num, col, raw=num_str), i

        raise DubSarSyntaxError(
            f"Invalid numeric literal: {text[:5]!r}",
            line=line_num,
            col=col,
            source_file=self.source_file,
        )

    def _scan_identifier(self, text: str, line_num: int, col: int) -> tuple[Optional[Token], int]:
        """Scans an identifier (ASCII kebab-case or Cuneiform) or Scholar keyword."""
        # Check Cuneiform identifier: 1 or more cuneiform characters that are not keywords
        ch = text[0]
        cp = ord(ch)
        if 0x12000 <= cp <= 0x1247F:
            # Cuneiform sign!
            i = 0
            n = len(text)
            while i < n and 0x12000 <= ord(text[i]) <= 0x1247F:
                i += 1
            ident_str = text[:i]

            # Check if keyword (e.g. 𒈬, 𒌓, 𒌗)
            if ident_str in CUNEIFORM_KEYWORDS:
                tok_type = CUNEIFORM_KEYWORDS[ident_str]
                return Token(tok_type, ident_str, line_num, col), i

            return Token(TokenType.IDENTIFIER, ident_str, line_num, col), i

        # ASCII identifier: [A-Za-z_][A-Za-z0-9_-]*
        if ch.isalpha() or ch == "_":
            i = 1
            n = len(text)
            while i < n:
                c = text[i]
                if c.isalnum() or c == "_":
                    i += 1
                elif c == "-":
                    # Hyphen in identifier: must be followed by alphanumeric or underscore to not be subtraction
                    if i + 1 < n and (text[i + 1].isalnum() or text[i + 1] == "_"):
                        i += 2
                    else:
                        break
                else:
                    break

            ident_str = text[:i]

            # Check Scholar keywords (case-insensitive for keywords)
            lower_str = ident_str.lower()
            if lower_str in SCHOLAR_KEYWORDS:
                tok_type = SCHOLAR_KEYWORDS[lower_str]
                return Token(tok_type, ident_str, line_num, col), i

            return Token(TokenType.IDENTIFIER, ident_str, line_num, col), i

        return None, 0

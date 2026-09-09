"""DUB.SAR 1.0 — Token Definitions and Vocabulary.

Implements Sections 3, 4, and 6:
- Canonical vocabulary mappings (Cuneiform <-> Scholar)
- Token types and Token data structure
- Source-mode normalization
"""

from __future__ import annotations

from enum import Enum, auto
from typing import Any, Dict, Optional, Set


class TokenType(Enum):
    # Structural sections
    PROBLEM = auto()      # 𒂊𒁹 / PROBLEM
    PROCEDURE = auto()    # 𒁾𒊬 / PROCEDURE / procedure / dub-sar
    RESULT = auto()       # 𒅗𒁹 / RESULT

    # Control flow & declarations
    IF = auto()           # 𒂊𒀀 / if / e-a
    ELSE = auto()         # 𒉡𒂊𒀀 / else / nu-e-a
    REPEAT = auto()       # 𒄀 / repeat / for / gi
    RETURN = auto()       # 𒄑 / return / ges / ĝeš
    OUTPUT = auto()       # 𒁹𒀀 / output / print / diš-a / dis-a
    INPUT = auto()        # 𒀀𒁹 / input / a-diš / a-dis
    RANGE_SEP = auto()    # 𒌗 / iti / to / ..

    # Assignment & Punctuation
    ASSIGN = auto()       # :=
    COLON = auto()        # :
    COMMA = auto()        # ,
    LPAREN = auto()       # (
    RPAREN = auto()       # )

    # Operators
    PLUS = auto()         # + / 𒍣 / zi / add
    MINUS = auto()        # - / 𒋫 / ta / sub
    STAR = auto()         # * / 𒊭 / ša / sha / mul
    SLASH = auto()        # / / 𒉌 / ni / div
    MOD = auto()          # %
    POW = auto()          # **
    NOT = auto()          # 𒉡 / not / nu

    # Comparison
    EQ = auto()           # ==
    NEQ = auto()          # !=
    LT = auto()           # <
    LTE = auto()          # <=
    GT = auto()           # >
    GTE = auto()          # >=

    # Literals
    NUMBER = auto()       # 365, 365;14,31,55, 1;30, 365.2422, cuneiform numerals
    STRING = auto()       # "..."
    IDENTIFIER = auto()   # ASCII or cuneiform identifier

    # Layout
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()


class Token:
    """A lexical token with type, value, and source location."""

    __slots__ = ("type", "value", "line", "col", "raw")

    def __init__(
        self,
        type_: TokenType,
        value: Any,
        line: int,
        col: int,
        raw: Optional[str] = None,
    ) -> None:
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
        self.raw = raw if raw is not None else str(value)

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:C{self.col})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value


# Canonical Cuneiform vocabulary mappings (§4)
CUNEIFORM_KEYWORDS: Dict[str, TokenType] = {
    "𒂊𒁹": TokenType.PROBLEM,
    "𒁾𒊬": TokenType.PROCEDURE,
    "𒅗𒁹": TokenType.RESULT,
    "𒂊𒀀": TokenType.IF,
    "𒉡𒂊𒀀": TokenType.ELSE,
    "𒄀": TokenType.REPEAT,
    "𒄑": TokenType.RETURN,
    "𒁹𒀀": TokenType.OUTPUT,
    "𒀀𒁹": TokenType.INPUT,
    "𒍣": TokenType.PLUS,
    "𒋫": TokenType.MINUS,
    "𒊭": TokenType.STAR,
    "𒉌": TokenType.SLASH,
    "𒉡": TokenType.NOT,
    "𒌗": TokenType.RANGE_SEP,
}

# Scholar / Transliteration keyword mappings (§2.2, §4, §6)
SCHOLAR_KEYWORDS: Dict[str, TokenType] = {
    "problem": TokenType.PROBLEM,
    "e-dis": TokenType.PROBLEM,
    "e-diš": TokenType.PROBLEM,
    "procedure": TokenType.PROCEDURE,
    "dub-sar": TokenType.PROCEDURE,
    "recipe": TokenType.PROCEDURE,
    "result": TokenType.RESULT,
    "ka-dis": TokenType.RESULT,
    "ka-diš": TokenType.RESULT,
    "if": TokenType.IF,
    "e-a": TokenType.IF,
    "else": TokenType.ELSE,
    "nu-e-a": TokenType.ELSE,
    "repeat": TokenType.REPEAT,
    "for": TokenType.REPEAT,
    "gi": TokenType.REPEAT,
    "return": TokenType.RETURN,
    "ges": TokenType.RETURN,
    "ĝeš": TokenType.RETURN,
    "output": TokenType.OUTPUT,
    "print": TokenType.OUTPUT,
    "dis-a": TokenType.OUTPUT,
    "diš-a": TokenType.OUTPUT,
    "input": TokenType.INPUT,
    "a-dis": TokenType.INPUT,
    "a-diš": TokenType.INPUT,
    "to": TokenType.RANGE_SEP,
    "..": TokenType.RANGE_SEP,
    "iti": TokenType.RANGE_SEP,
    "not": TokenType.NOT,
    "nu": TokenType.NOT,
}

# Reverse mapping for canonical transliteration / cuneiformization
TOKEN_TO_CUNEIFORM: Dict[TokenType, str] = {
    TokenType.PROBLEM: "𒂊𒁹",
    TokenType.PROCEDURE: "𒁾𒊬",
    TokenType.RESULT: "𒅗𒁹",
    TokenType.IF: "𒂊𒀀",
    TokenType.ELSE: "𒉡𒂊𒀀",
    TokenType.REPEAT: "𒄀",
    TokenType.RETURN: "𒄑",
    TokenType.OUTPUT: "𒁹𒀀",
    TokenType.INPUT: "𒀀𒁹",
    TokenType.PLUS: "𒍣",
    TokenType.MINUS: "𒋫",
    TokenType.STAR: "𒊭",
    TokenType.SLASH: "𒉌",
    TokenType.NOT: "𒉡",
    TokenType.RANGE_SEP: "𒌗",
}

TOKEN_TO_SCHOLAR: Dict[TokenType, str] = {
    TokenType.PROBLEM: "PROBLEM",
    TokenType.PROCEDURE: "procedure",
    TokenType.RESULT: "RESULT",
    TokenType.IF: "if",
    TokenType.ELSE: "else",
    TokenType.REPEAT: "repeat",
    TokenType.RETURN: "return",
    TokenType.OUTPUT: "output",
    TokenType.INPUT: "input",
    TokenType.PLUS: "+",
    TokenType.MINUS: "-",
    TokenType.STAR: "*",
    TokenType.SLASH: "/",
    TokenType.MOD: "%",
    TokenType.POW: "**",
    TokenType.NOT: "not",
    TokenType.RANGE_SEP: "to",
}

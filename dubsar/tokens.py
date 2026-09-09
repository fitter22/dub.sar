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
    PROBLEM = auto()      # 𒂊𒁹 / PROBLEM / given
    GIVEN = PROBLEM
    RECIPE = auto()       # 𒁾𒊬 / RECIPE / procedure / dub-sar
    PROCEDURE = RECIPE
    RESULT = auto()       # 𒅗𒁹 / RESULT

    # Mathematical domains, selection & control flow
    CONSIDER = auto()     # 𒄀 / consider / repeat / for / gi
    REPEAT = CONSIDER
    FROM = auto()         # 𒋫 / from / ta
    THROUGH = auto()      # 𒌗 / through / to / .. / iti
    RANGE_SEP = THROUGH
    RETAIN = auto()       # 𒋼 / retain / keep / tu
    WHEN = auto()         # 𒂊𒀀 / when / if / e-a
    IF = WHEN
    ELSE = auto()         # 𒉡𒂊𒀀 / else / nu-e-a
    RETURN = auto()       # 𒄑 / return / ges / ĝeš
    INSCRIBE = auto()     # 𒁹𒀀 / inscribe / output / print / diš-a / dis-a
    OUTPUT = INSCRIBE
    ASK = auto()          # 𒀀𒁹 / ask / input / a-diš / a-dis
    INPUT = ASK

    # Comparison & Logic
    LESSER = auto()       # 𒌉 / lesser / tur / <
    GREATER = auto()      # 𒃲 / greater / gal / >
    EQUAL = auto()        # 𒊓 / equal / sa / sá / ==
    NOT_EQUAL = auto()    # 𒉡 / not-equal / !=
    THAN = auto()         # 𒋫 / than
    IS = auto()           # 𒈨 / is / me
    EMPTY = auto()        # 𒉡 / empty / none / nu
    OF = auto()           # 𒊭 / of / ša / sha
    TAKE = auto()         # 𒋗 / take / šu / shu
    DETERMINE = auto()    # 𒉆 / determine / nam
    APPLY = auto()        # apply

    # Assignment & Punctuation
    ASSIGN = auto()       # :=
    COLON = auto()        # :
    COMMA = auto()        # ,
    DOT = auto()          # .
    LPAREN = auto()       # (
    RPAREN = auto()       # )

    # Operators
    PLUS = auto()         # + / 𒍣 / zi / add
    MINUS = auto()        # - / 𒋫 / ta / sub / subtract
    STAR = auto()         # * / 𒊭 / ša / sha / mul / multiply
    SLASH = auto()        # / / 𒉌 / ni / div / divide
    MOD = auto()          # %
    POW = auto()          # **
    NOT = auto()          # 𒉡 / not / nu
    FLOOR = auto()        # гур / floor / gur
    CEIL = auto()         # 𒉏 / ceil / nim
    NEAREST = auto()      # 𒊑 / nearest / ri / round
    ABSOLUTE = auto()     # 𒋼 / absolute / abs / te

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


# Canonical Cuneiform vocabulary mappings (§4, §8, §60)
CUNEIFORM_KEYWORDS: Dict[str, TokenType] = {
    "𒂊𒁹": TokenType.PROBLEM,
    "𒁾𒊬": TokenType.RECIPE,
    "𒅗𒁹": TokenType.RESULT,
    "𒂊𒀀": TokenType.WHEN,
    "𒉡𒂊𒀀": TokenType.ELSE,
    "𒄀": TokenType.CONSIDER,
    "𒄑": TokenType.RETURN,
    "𒁹𒀀": TokenType.INSCRIBE,
    "𒀀𒁹": TokenType.ASK,
    "𒍣": TokenType.PLUS,
    "𒋫": TokenType.MINUS,
    "𒊭": TokenType.STAR,
    "𒉌": TokenType.SLASH,
    "𒉡": TokenType.EMPTY,
    "𒌗": TokenType.THROUGH,
    "𒋼": TokenType.RETAIN,
    "𒌉": TokenType.LESSER,
    "𒃲": TokenType.GREATER,
    "𒊓": TokenType.EQUAL,
    "𒈨": TokenType.IS,
    "𒋗": TokenType.TAKE,
    "𒉆": TokenType.DETERMINE,
    "гур": TokenType.FLOOR,
    "𒉏": TokenType.CEIL,
    "𒊑": TokenType.NEAREST,
}

# Scholar / Transliteration keyword mappings (§2.2, §4, §6, §60)
SCHOLAR_KEYWORDS: Dict[str, TokenType] = {
    "problem": TokenType.PROBLEM,
    "given": TokenType.PROBLEM,
    "e-dis": TokenType.PROBLEM,
    "e-diš": TokenType.PROBLEM,
    "recipe": TokenType.RECIPE,
    "procedure": TokenType.RECIPE,
    "dub-sar": TokenType.RECIPE,
    "result": TokenType.RESULT,
    "ka-dis": TokenType.RESULT,
    "ka-diš": TokenType.RESULT,
    "consider": TokenType.CONSIDER,
    "repeat": TokenType.CONSIDER,
    "for": TokenType.CONSIDER,
    "gi": TokenType.CONSIDER,
    "from": TokenType.FROM,
    "through": TokenType.THROUGH,
    "to": TokenType.THROUGH,
    "..": TokenType.THROUGH,
    "iti": TokenType.THROUGH,
    "retain": TokenType.RETAIN,
    "keep": TokenType.RETAIN,
    "tu": TokenType.RETAIN,
    "when": TokenType.WHEN,
    "if": TokenType.WHEN,
    "e-a": TokenType.WHEN,
    "else": TokenType.ELSE,
    "nu-e-a": TokenType.ELSE,
    "return": TokenType.RETURN,
    "ges": TokenType.RETURN,
    "ĝeš": TokenType.RETURN,
    "inscribe": TokenType.INSCRIBE,
    "output": TokenType.INSCRIBE,
    "print": TokenType.INSCRIBE,
    "dis-a": TokenType.INSCRIBE,
    "diš-a": TokenType.INSCRIBE,
    "ask": TokenType.ASK,
    "input": TokenType.ASK,
    "a-dis": TokenType.ASK,
    "a-diš": TokenType.ASK,
    "lesser": TokenType.LESSER,
    "tur": TokenType.LESSER,
    "greater": TokenType.GREATER,
    "gal": TokenType.GREATER,
    "equal": TokenType.EQUAL,
    "sa": TokenType.EQUAL,
    "sá": TokenType.EQUAL,
    "not-equal": TokenType.NOT_EQUAL,
    "than": TokenType.THAN,
    "is": TokenType.IS,
    "me": TokenType.IS,
    "empty": TokenType.EMPTY,
    "none": TokenType.EMPTY,
    "of": TokenType.OF,
    "take": TokenType.TAKE,
    "determine": TokenType.DETERMINE,
    "apply": TokenType.APPLY,
    "add": TokenType.PLUS,
    "zi": TokenType.PLUS,
    "subtract": TokenType.MINUS,
    "sub": TokenType.MINUS,
    "ta": TokenType.MINUS,
    "multiply": TokenType.STAR,
    "mul": TokenType.STAR,
    "sha": TokenType.STAR,
    "ša": TokenType.STAR,
    "divide": TokenType.SLASH,
    "div": TokenType.SLASH,
    "ni": TokenType.SLASH,
    "floor": TokenType.FLOOR,
    "gur": TokenType.FLOOR,
    "ceil": TokenType.CEIL,
    "nim": TokenType.CEIL,
    "nearest": TokenType.NEAREST,
    "round": TokenType.NEAREST,
    "ri": TokenType.NEAREST,
    "absolute": TokenType.ABSOLUTE,
    "abs": TokenType.ABSOLUTE,
    "te": TokenType.ABSOLUTE,
    "not": TokenType.NOT,
    "nu": TokenType.NOT,
}

# Reverse mapping for canonical transliteration / cuneiformization
TOKEN_TO_CUNEIFORM: Dict[TokenType, str] = {
    TokenType.PROBLEM: "𒂊𒁹",
    TokenType.RECIPE: "𒁾𒊬",
    TokenType.RESULT: "𒅗𒁹",
    TokenType.WHEN: "𒂊𒀀",
    TokenType.ELSE: "𒉡𒂊𒀀",
    TokenType.CONSIDER: "𒄀",
    TokenType.RETURN: "𒄑",
    TokenType.INSCRIBE: "𒁹𒀀",
    TokenType.ASK: "𒀀𒁹",
    TokenType.PLUS: "𒍣",
    TokenType.MINUS: "𒋫",
    TokenType.STAR: "𒊭",
    TokenType.SLASH: "𒉌",
    TokenType.NOT: "𒉡",
    TokenType.THROUGH: "𒌗",
    TokenType.RETAIN: "𒋼",
    TokenType.LESSER: "𒌉",
    TokenType.GREATER: "𒃲",
    TokenType.EQUAL: "𒊓",
    TokenType.IS: "𒈨",
    TokenType.EMPTY: "𒉡",
    TokenType.FLOOR: "гур",
    TokenType.CEIL: "𒉏",
    TokenType.NEAREST: "𒊑",
    TokenType.ABSOLUTE: "𒋼",
    TokenType.TAKE: "𒋗",
    TokenType.DETERMINE: "𒉆",
}

TOKEN_TO_SCHOLAR: Dict[TokenType, str] = {
    TokenType.PROBLEM: "problem",
    TokenType.RECIPE: "recipe",
    TokenType.RESULT: "result",
    TokenType.WHEN: "when",
    TokenType.ELSE: "else",
    TokenType.CONSIDER: "consider",
    TokenType.RETURN: "return",
    TokenType.INSCRIBE: "inscribe",
    TokenType.ASK: "ask",
    TokenType.PLUS: "add",
    TokenType.MINUS: "subtract",
    TokenType.STAR: "multiply",
    TokenType.SLASH: "divide",
    TokenType.MOD: "%",
    TokenType.POW: "**",
    TokenType.NOT: "not",
    TokenType.THROUGH: "through",
    TokenType.FROM: "from",
    TokenType.RETAIN: "retain",
    TokenType.LESSER: "lesser",
    TokenType.GREATER: "greater",
    TokenType.EQUAL: "equal",
    TokenType.NOT_EQUAL: "not-equal",
    TokenType.THAN: "than",
    TokenType.IS: "is",
    TokenType.EMPTY: "empty",
    TokenType.FLOOR: "floor",
    TokenType.CEIL: "ceil",
    TokenType.NEAREST: "nearest",
    TokenType.ABSOLUTE: "absolute",
    TokenType.OF: "of",
    TokenType.TAKE: "take",
    TokenType.DETERMINE: "determine",
    TokenType.APPLY: "apply",
}

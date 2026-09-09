"""DUB.SAR 1.0 — Source Normalizer and Transliteration Engine.

Implements Sections 2, 4, and 24:
- Translates Tablet mode (Cuneiform) -> Scholar mode (Latin transliteration)
- Translates Scholar mode -> Canonical Cuneiform Tablet mode
- Normalizes mixed-mode source code
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from dubsar.lexer import Lexer
from dubsar.numbers import format_cuneiform_digit
from dubsar.tokens import (
    CUNEIFORM_KEYWORDS,
    SCHOLAR_KEYWORDS,
    TOKEN_TO_CUNEIFORM,
    TOKEN_TO_SCHOLAR,
    Token,
    TokenType,
)

# Mapping table from cuneiform tokens to scholar text
CUNEIFORM_TO_SCHOLAR_MAP: List[Tuple[str, str]] = [
    ("𒉡𒂊𒀀", "else"),
    ("𒂊𒁹", "PROBLEM"),
    ("𒁾𒊬", "procedure"),
    ("𒅗𒁹", "RESULT"),
    ("𒂊𒀀", "if"),
    ("𒄀", "repeat"),
    ("𒄑", "return"),
    ("𒁹𒀀", "output"),
    ("𒀀𒁹", "input"),
    ("𒍣", "+"),
    ("𒋫", "-"),
    ("𒊭", "*"),
    ("𒉌", "/"),
    ("nu", "not"),
    ("𒉡", "not"),
    ("𒑰", "#"),
    ("𒌓", "day"),
    ("𒌗", "month"),
    ("𒈬", "year"),
]

# Mapping table from scholar keywords to canonical cuneiform
SCHOLAR_TO_CUNEIFORM_WORDS: Dict[str, str] = {
    "problem": "𒂊𒁹",
    "procedure": "𒁾𒊬",
    "dub-sar": "𒁾𒊬",
    "recipe": "𒁾𒊬",
    "result": "𒅗𒁹",
    "if": "𒂊𒀀",
    "e-a": "𒂊𒀀",
    "else": "𒉡𒂊𒀀",
    "nu-e-a": "𒉡𒂊𒀀",
    "repeat": "𒄀",
    "gi": "𒄀",
    "return": "𒄑",
    "ges": "𒄑",
    "ĝeš": "𒄑",
    "output": "𒁹𒀀",
    "print": "𒁹𒀀",
    "diš-a": "𒁹𒀀",
    "dis-a": "𒁹𒀀",
    "input": "𒀀𒁹",
    "a-diš": "𒀀𒁹",
    "a-dis": "𒀀𒁹",
    "to": "𒌗",
    "..": "𒌗",
    "day": "𒌓",
    "ud": "𒌓",
    "month": "𒌗",
    "iti": "𒌗",
    "year": "𒈬",
    "mu": "𒈬",
}


def transliterate(source: str) -> str:
    """Converts a tablet source (cuneiform/mixed) to clean Scholar mode transliteration."""
    lines = source.splitlines()
    new_lines = []

    for line in lines:
        new_line = line
        # Check comment
        comment = ""
        if "𒑰" in new_line:
            idx = new_line.index("𒑰")
            comment = "#" + new_line[idx + 1:]
            new_line = new_line[:idx]
        elif "#" in new_line:
            idx = new_line.index("#")
            comment = new_line[idx:]
            new_line = new_line[:idx]

        # Replace cuneiform signs (longest match first)
        for cun, sch in CUNEIFORM_TO_SCHOLAR_MAP:
            new_line = new_line.replace(cun, sch)

        if comment:
            new_line = new_line.rstrip() + "  " + comment if new_line.strip() else comment
        new_lines.append(new_line)

    return "\n".join(new_lines)


def cuneiformize(source: str) -> str:
    """Converts Scholar mode or mixed source to canonical Cuneiform Tablet mode."""
    lines = source.splitlines()
    new_lines = []

    for line in lines:
        new_line = line
        # Check comment
        comment = ""
        if "#" in new_line:
            idx = new_line.index("#")
            comment = "𒑰" + new_line[idx + 1:]
            new_line = new_line[:idx]
        elif "𒑰" in new_line:
            idx = new_line.index("𒑰")
            comment = new_line[idx:]
            new_line = new_line[:idx]

        # Word boundary replacement for Scholar keywords
        def replace_word(match: re.Match) -> str:
            w = match.group(0).lower()
            if w in SCHOLAR_TO_CUNEIFORM_WORDS:
                return SCHOLAR_TO_CUNEIFORM_WORDS[w]
            return match.group(0)

        # Pattern for words
        new_line = re.sub(r"\b[A-Za-z_-]+\b", replace_word, new_line)
        # Also replace .. with 𒌗
        new_line = new_line.replace("..", " 𒌗 ")

        if comment:
            new_line = new_line.rstrip() + "  " + comment if new_line.strip() else comment
        new_lines.append(new_line)

    return "\n".join(new_lines)

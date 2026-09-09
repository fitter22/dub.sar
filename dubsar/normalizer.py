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
    ("𒂊𒁹", "problem"),
    ("𒁾𒊬", "recipe"),
    ("𒅗𒁹", "result"),
    ("𒂊𒀀", "when"),
    ("𒄀", "consider"),
    ("𒄑", "return"),
    ("𒁹𒀀", "output"),
    ("𒀀𒁹", "ask"),
    ("𒌉", "lesser"),
    ("𒃲", "greater"),
    ("𒊓", "equal"),
    ("𒍣", "add"),
    ("𒊭", "multiply"),
    ("𒉌", "divide"),
    ("nu", "not"),
    ("𒉡", "empty"),
    ("𒄥", "floor"),
    ("𒉏", "ceil"),
    ("𒊑", "nearest"),
    ("𒈨", "is"),
    ("𒉆", "determine"),
    ("ナム", "determine"),
    ("𒀝", "apply"),
    ("𒆕", "apply"),
    ("𒂗", "through"),
    ("𒋗", "take"),
    ("𒑰", "#"),
    ("𒌓", "day"),
    ("𒌗", "month"),
    ("𒈬", "year"),
]

# Mapping table from scholar keywords to canonical cuneiform
SCHOLAR_TO_CUNEIFORM_WORDS: Dict[str, str] = {
    "problem": "𒂊𒁹",
    "given": "𒂊𒁹",
    "procedure": "𒁾𒊬",
    "dub-sar": "𒁾𒊬",
    "recipe": "𒁾𒊬",
    "result": "𒅗𒁹",
    "if": "𒂊𒀀",
    "when": "𒂊𒀀",
    "e-a": "𒂊𒀀",
    "else": "𒉡𒂊𒀀",
    "nu-e-a": "𒉡𒂊𒀀",
    "consider": "𒄀",
    "repeat": "𒄀",
    "gi": "𒄀",
    "retain": "𒋼",
    "from": "𒋫",
    "through": "𒂗",
    "to": "𒂗",
    "en": "𒂗",
    "lesser": "𒌉",
    "greater": "𒃲",
    "equal": "𒊓",
    "empty": "𒉡",
    "none": "𒉡",
    "floor": "𒄥",
    "ceil": "𒉏",
    "nearest": "𒊑",
    "absolute": "𒋼",
    "is": "𒈨",
    "determine": "𒉆",
    "nam": "𒉆",
    "apply": "𒀝",
    "ak": "𒀝",
    "return": "𒄑",
    "ges": "𒄑",
    "ĝeš": "𒄑",
    "output": "𒁹𒀀",
    "inscribe": "𒁹𒀀",
    "print": "𒁹𒀀",
    "diš-a": "𒁹𒀀",
    "dis-a": "𒁹𒀀",
    "ask": "𒀀𒁹",
    "input": "𒀀𒁹",
    "a-diš": "𒀀𒁹",
    "a-dis": "𒀀𒁹",
    "day": "𒌓",
    "ud": "𒌓",
    "month": "𒌗",
    "iti": "𒌗",
    "year": "𒈬",
    "mu": "𒈬",
    "multiply": "𒊭",
    "mul": "𒊭",
    "divide": "𒉌",
    "div": "𒉌",
    "add": "𒍣",
    "subtract": "𒋫",
    "sub": "𒋫",
    "of": "𒊭",
    "than": "𒋫",
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

        # Preserve string literals during replacement
        parts = re.split(r'(".*?")', new_line)
        for i in range(0, len(parts), 2):
            p = parts[i]
            # Contextual replacement for domain loops: 𒄀/consider ... 𒋫 ... 𒂗 ...
            p = re.sub(r'(\b(?:consider|𒄀)\s+[A-Za-z0-9_-]+\s+)𒋫\s+', r'\1from ', p)
            # Contextual replacement for retain: line starting with 𒋼 <word>
            p = re.sub(r'^(\s*)𒋼(\s+[A-Za-z0-9_-]+)', r'\1retain\2', p)
            # Contextual replacement for comparison: 𒌉/lesser 𒋫 -> lesser than
            p = re.sub(r'(\b(?:lesser|greater|𒌉|𒃲)\s+)𒋫(\s+)', r'\1than\2', p)
            # Contextual replacement for field access: <word> 𒊭 <word> -> <word> of <word>
            p = re.sub(r'([A-Za-z0-9_-]+)\s+𒊭\s+([A-Za-z0-9_-]+)', r'\1 of \2', p)
            # Postfix 𒋼 alone or after whitespace
            p = re.sub(r'(^|\s+)𒋼($|\s+)', r'\1absolute\2', p)
            # Postfix 𒋫 alone or after whitespace
            p = re.sub(r'(^|\s+)𒋫($|\s+)', r'\1subtract\2', p)
            # Replace cuneiform signs
            for cun, sch in CUNEIFORM_TO_SCHOLAR_MAP:
                p = p.replace(cun, sch)
            parts[i] = p
        new_line = "".join(parts)

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

        # Preserve string literals during replacement
        parts = re.split(r'(".*?")', new_line)
        for i in range(0, len(parts), 2):
            p = parts[i]
            def replace_word(match: re.Match) -> str:
                w = match.group(0).lower()
                if w in SCHOLAR_TO_CUNEIFORM_WORDS:
                    return SCHOLAR_TO_CUNEIFORM_WORDS[w]
                return match.group(0)

            # Pattern for words
            p = re.sub(r"\b[A-Za-z_-]+\b", replace_word, p)
            # Also replace .. with 𒂗
            p = p.replace("..", " 𒂗 ")
            parts[i] = p
        new_line = "".join(parts)

        if comment:
            new_line = new_line.rstrip() + "  " + comment if new_line.strip() else comment
        new_lines.append(new_line)

    return "\n".join(new_lines)

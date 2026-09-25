"""DUB.SAR 1.0 — Source Normalizer and Transliteration Engine.

Implements Sections 2, 4, and 24:
- Translates Tablet mode (Cuneiform) -> Scholar mode (Latin transliteration)
- Translates Scholar mode -> Canonical Cuneiform Tablet mode
- Normalizes mixed-mode source code
- Preserves arbitrary Unicode string literals as data without transliteration
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

STRING_PATTERN = re.compile(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')')
CUNEIFORM_WORD_PATTERN = re.compile(r"[\U00012000-\U0001246F\U00012472-\U0001254F]+")

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
    ("𒅆", "consult"),
    ("𒁾", "tablet"),
    ("𒆥", "working"),
    ("𒃻", "put"),
    ("𒈭", "append"),
    ("𒉻", "entry"),
    ("𒁶", "as"),
    ("𒀀", "into"),
    ("𒁀𒋛", "square-root"),
]

CUNEIFORM_TO_SCHOLAR_WORDS: Dict[str, str] = {
    cun: sch for cun, sch in CUNEIFORM_TO_SCHOLAR_MAP if cun != "𒑰"
}

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
    "consult": "𒅆",
    "tablet": "𒁾",
    "working": "𒆥",
    "put": "𒃻",
    "append": "𒈭",
    "entry": "𒉻",
    "as": "𒁶",
    "into": "𒀀",
    "take": "𒋗",
    "square-root": "𒁀𒋛",
    "sqrt": "𒁀𒋛",
}

# Canonical / symbolic identifier mappings for flagship examples and common programs
CANONICAL_TABLET_IDENTIFIERS: Dict[str, str] = {
    # Planetary leap
    "solar-year": "𒈬",
    "limit": "𒍠",
    "whole-days": "𒌓",
    "fraction": "𒁇",
    "best": "𒊕",
    "cycle": "𒁄",
    "leaps": "𒋛",
    "candidate-year": "𒈬𒁶",
    "error": "𒇲",
    "candidate": "𒊮",
    # Babylonian sqrt(2)
    "initial-estimate": "𒊕",
    "steps": "𒅎",
    "target-diagonal": "𒁇",
    "approx": "𒃷",
    "diagonal": "𒋛",
    "babylonian-sqrt": "𒅆𒁀",
    "start": "𒈠",
    "iterations": "𒅎",
    "two": "𒋰",
    "half": "𒈦",
    "step": "𒁄",
    "next-x": "𒈠𒁶",
    # Even distribution
    "y1": "𒈬𒁹",
    "y2": "𒈬𒈫",
    "y3": "𒈬𒐈",
    "y4": "𒈬𒐉",
    "leap-for-year": "𒋛𒈬",
    "prev-year": "𒈬𒈦",
    "cur-count": "𒅎",
    "prev-count": "𒅎𒈦",
    "is-leap": "𒋛𒀀",
    # Reciprocal lookup
    "reciprocals": "𒅎",
    "recip_8": "𒈦",
    "dividend": "𒊕",
    "quotient": "𒁇",
}

CANONICAL_SCHOLAR_IDENTIFIERS: Dict[str, str] = {
    v: k for k, v in CANONICAL_TABLET_IDENTIFIERS.items()
}


def _build_identifier_maps(
    identifier_map: Optional[Dict[str, str]],
    use_canonical: bool,
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Builds bidirectional (scholar_to_cuneiform, cuneiform_to_scholar) identifier maps."""
    s_to_c: Dict[str, str] = {}
    c_to_s: Dict[str, str] = {}

    if use_canonical:
        s_to_c.update(CANONICAL_TABLET_IDENTIFIERS)
        c_to_s.update(CANONICAL_SCHOLAR_IDENTIFIERS)

    if identifier_map:
        for k, v in identifier_map.items():
            # If key contains cuneiform signs, treat as cuneiform -> scholar
            if re.search(r"[\U00012000-\U0001254F]", k):
                c_to_s[k] = v
                s_to_c[v] = k
            else:
                s_to_c[k] = v
                c_to_s[v] = k

    return s_to_c, c_to_s


def transliterate(
    source: str,
    identifier_map: Optional[Dict[str, str]] = None,
    use_canonical_identifiers: bool = False,
) -> str:
    """Converts a tablet source (cuneiform/mixed) to clean Scholar mode transliteration.

    String literals are preserved verbatim because they represent data, not program syntax.
    """
    _, c_to_s = _build_identifier_maps(identifier_map, use_canonical_identifiers)
    lines = source.splitlines()
    new_lines = []

    for line in lines:
        parts = STRING_PATTERN.split(line)

        # Extract comments occurring outside string literals
        code_parts: List[str] = []
        comment = ""
        for i in range(0, len(parts), 2):
            p = parts[i]
            # Check for comment markers '𒑰' or '#'
            c_idx = -1
            for marker in ("𒑰", "#"):
                pos = p.find(marker)
                if pos != -1 and (c_idx == -1 or pos < c_idx):
                    c_idx = pos

            if c_idx != -1:
                code_parts.append(p[:c_idx])
                comment_tail = p[c_idx + 1 :]
                remaining_parts = "".join(parts[i + 1 :])
                comment = "#" + comment_tail + remaining_parts
                break
            else:
                code_parts.append(p)
                if i + 1 < len(parts):
                    code_parts.append(parts[i + 1])

        # Process code segments (even indices)
        res_parts: List[str] = []
        for idx, part in enumerate(code_parts):
            if idx % 2 == 1:
                # String literal: preserve data content untouched
                res_parts.append(part)
                continue

            p = part
            # Contextual replacement for domain loops: 𒄀/consider <ident> 𒋫 ... 𒂗 ...
            p = re.sub(r"(\b(?:consider|𒄀)\s+[\w-]+\s+)𒋫\s+", r"\1from ", p)
            # Contextual replacement for retain: line starting with 𒋼 <ident>
            p = re.sub(r"^(\s*)𒋼(\s+[\w-]+)", r"\1retain\2", p)
            # Contextual replacement for comparison: 𒌉/lesser 𒋫 -> lesser than
            p = re.sub(r"(\b(?:lesser|greater|𒌉|𒃲)\s+)𒋫(\s+)", r"\1than\2", p)
            # Contextual replacement for field access: <field> 𒊭 <record> -> <field> of <record>
            p = re.sub(r"([\w-]+)\s+𒊭\s+([\w-]+)", r"\1 of \2", p)
            # Postfix 𒋼 alone or after whitespace
            p = re.sub(r"(^|\s+)𒋼($|\s+)", r"\1absolute\2", p)
            # Postfix 𒋫 alone or after whitespace
            p = re.sub(r"(^|\s+)𒋫($|\s+)", r"\1subtract\2", p)

            # Whole-word cuneiform token and identifier replacement
            def replace_cun_word(m: re.Match) -> str:
                w = m.group(0)
                if w in c_to_s:
                    return c_to_s[w]
                if w in CUNEIFORM_TO_SCHOLAR_WORDS:
                    return CUNEIFORM_TO_SCHOLAR_WORDS[w]
                return w

            p = CUNEIFORM_WORD_PATTERN.sub(replace_cun_word, p)
            res_parts.append(p)

        new_line = "".join(res_parts)
        if comment:
            new_line = new_line.rstrip() + "  " + comment if new_line.strip() else comment
        new_lines.append(new_line)

    return "\n".join(new_lines)


def cuneiformize(
    source: str,
    identifier_map: Optional[Dict[str, str]] = None,
    use_canonical_identifiers: bool = False,
) -> str:
    """Converts Scholar mode or mixed source to canonical Cuneiform Tablet mode.

    String literals are preserved verbatim because they represent data, not program syntax.
    """
    s_to_c, _ = _build_identifier_maps(identifier_map, use_canonical_identifiers)
    lines = source.splitlines()
    new_lines = []

    for line in lines:
        parts = STRING_PATTERN.split(line)

        # Extract comments occurring outside string literals
        code_parts: List[str] = []
        comment = ""
        for i in range(0, len(parts), 2):
            p = parts[i]
            c_idx = -1
            for marker in ("#", "𒑰"):
                pos = p.find(marker)
                if pos != -1 and (c_idx == -1 or pos < c_idx):
                    c_idx = pos

            if c_idx != -1:
                code_parts.append(p[:c_idx])
                comment_tail = p[c_idx + 1 :]
                remaining_parts = "".join(parts[i + 1 :])
                comment = "𒑰" + comment_tail + remaining_parts
                break
            else:
                code_parts.append(p)
                if i + 1 < len(parts):
                    code_parts.append(parts[i + 1])

        # Process code segments (even indices)
        res_parts: List[str] = []
        for idx, part in enumerate(code_parts):
            if idx % 2 == 1:
                # String literal: preserve data content untouched
                res_parts.append(part)
                continue

            p = part

            def replace_word(match: re.Match) -> str:
                orig = match.group(0)
                w = orig.lower()
                if orig in s_to_c:
                    return s_to_c[orig]
                if w in s_to_c:
                    return s_to_c[w]
                if w in SCHOLAR_TO_CUNEIFORM_WORDS:
                    return SCHOLAR_TO_CUNEIFORM_WORDS[w]
                return orig

            p = re.sub(r"\b[A-Za-z0-9_-]+\b", replace_word, p)
            # Replace range syntax .. with 𒂗
            p = p.replace("..", " 𒂗 ")
            res_parts.append(p)

        new_line = "".join(res_parts)
        if comment:
            new_line = new_line.rstrip() + "  " + comment if new_line.strip() else comment
        new_lines.append(new_line)

    return "\n".join(new_lines)

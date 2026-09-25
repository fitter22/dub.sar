#!/usr/bin/env python3
"""DUB.SAR Repository Invariant Check: Verify zero emojis in repository.

Excludes git history, caches, and binary files.
Distinguishes legitimate ancient cuneiform unicode characters from modern emojis.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# Match Unicode emoji blocks while preserving cuneiform (U+12000..U+1254F)
EMOJI_PATTERN = re.compile(
    "["
    "\u2600-\u26FF"          # Miscellaneous Symbols
    "\u2700-\u27BF"          # Dingbats
    "\U0001F600-\U0001F64F"  # Emoticons
    "\U0001F300-\U0001F5FF"  # Miscellaneous Symbols and Pictographs
    "\U0001F680-\U0001F6FF"  # Transport and Map Symbols
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U0001F1E6-\U0001F1FF"  # Enclosed Alphanumeric Supplement / Flags
    "]",
    flags=re.UNICODE,
)

IGNORED_DIRS = {".git", ".ruff_cache", "__pycache__", ".pytest_cache", "build", "dist", "site"}
IGNORED_EXTENSIONS = {".pyc", ".db", ".png", ".jpg", ".jpeg", ".ico", ".wasm", ".o", ".a"}


def check_file(path: Path) -> list[tuple[int, str]]:
    findings = []
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError):
        return findings

    for line_no, line in enumerate(content.splitlines(), start=1):
        for match in EMOJI_PATTERN.finditer(line):
            findings.append((line_no, match.group(0)))
    return findings


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    findings_count = 0

    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            p = Path(root) / f
            if p.suffix in IGNORED_EXTENSIONS:
                continue
            matches = check_file(p)
            for line_no, char in matches:
                findings_count += 1
                rel_path = p.relative_to(repo_root)
                code_point = f"U+{ord(char):04X}"
                print(f"[ERROR] Disallowed emoji {code_point} found in {rel_path}:{line_no}")

    if findings_count > 0:
        print(f"FAILED: Found {findings_count} emoji violation(s).")
        return 1

    print("SUCCESS: Zero emojis found across repository.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""DUB.SAR Repository Invariant Check: Verify zero emojis in repository.

Excludes git history directories, caches, and binary files.
Distinguishes legitimate ancient cuneiform Unicode characters from modern emojis.
Optionally verifies recent git commit messages.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# Match Unicode emoji blocks while strictly preserving cuneiform (U+12000..U+1254F)
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
    """Checks a single file for disallowed emojis, returning line numbers and matched characters."""
    findings = []
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError):
        return findings

    for line_no, line in enumerate(content.splitlines(), start=1):
        for match in EMOJI_PATTERN.finditer(line):
            findings.append((line_no, match.group(0)))
    return findings


def check_git_commits(repo_root: Path, max_count: int = 50) -> list[str]:
    """Scans recent git commit messages for disallowed emojis."""
    findings = []
    try:
        proc = subprocess.run(
            ["git", "log", f"-n{max_count}", "--format=%H %s%n%b"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            for line in proc.stdout.splitlines():
                for match in EMOJI_PATTERN.finditer(line):
                    char = match.group(0)
                    code_point = f"U+{ord(char):04X}"
                    findings.append(f"[ERROR] Disallowed emoji {code_point} in commit message: {line.strip()[:60]}")
    except Exception:
        pass
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify zero emojis in repository and git history.")
    parser.add_argument("--skip-commits", action="store_true", help="Skip scanning git commit history")
    parser.add_argument("--path", type=str, default=None, help="Root path to scan (defaults to repository root)")
    args = parser.parse_args()

    repo_root = Path(args.path).resolve() if args.path else Path(__file__).resolve().parent.parent
    findings_count = 0

    # 1. Scan files in repository
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            p = Path(root) / f
            if p.suffix in IGNORED_EXTENSIONS:
                continue
            matches = check_file(p)
            for line_no, char in matches:
                findings_count += 1
                try:
                    rel_path = p.relative_to(repo_root)
                except ValueError:
                    rel_path = p
                code_point = f"U+{ord(char):04X}"
                print(f"[ERROR] Disallowed emoji {code_point} found in {rel_path}:{line_no}")

    # 2. Scan git commit messages if requested
    if not args.skip_commits:
        commit_findings = check_git_commits(repo_root)
        for cf in commit_findings:
            findings_count += 1
            print(cf)

    if findings_count > 0:
        print(f"FAILED: Found {findings_count} emoji violation(s).")
        return 1

    print("SUCCESS: Zero emojis found across repository.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

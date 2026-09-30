"""Tests verifying documentation links, example references, UTF-8 integrity, and compiler conformance."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from dubsar.lexer import Lexer
from dubsar.native.compiler import NativeCompiler
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer
from dubsar.wasm import WasmCompiler

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"


def _slugify(text: str) -> str:
    """Generates an anchor slug following Python-Markdown rules."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text


def _extract_anchors(file_path: Path) -> set[str]:
    """Extracts heading anchor slugs and explicit HTML IDs from a Markdown file."""
    anchors: set[str] = set()
    text = file_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("#"):
            h_text = line.lstrip("#").strip()
            # Remove inline markdown links
            h_text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", h_text)
            # Remove inline code formatting
            h_text = re.sub(r"`([^`]+)`", r"\1", h_text)
            anchors.add(_slugify(h_text))
        for m in re.finditer(r"id=[\"\']([a-zA-Z0-9_\-]+)[\"\']", line):
            anchors.add(m.group(1))
    return anchors


class TestDocsIntegrity(unittest.TestCase):
    """Verifies that documentation links, referenced examples, and encodings remain sound."""

    def test_internal_markdown_links_and_anchors(self) -> None:
        """Every relative Markdown link and anchor in docs/ must point to a valid target."""
        link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
        md_files = sorted(DOCS_DIR.glob("**/*.md")) + [REPO_ROOT / "README.md"]
        broken_links: list[str] = []

        for md_path in md_files:
            if not md_path.exists():
                continue
            content = md_path.read_text(encoding="utf-8")
            for text_snippet, target in link_pattern.findall(content):
                # Skip external links
                if target.startswith(("http://", "https://", "mailto:", "ftp://")):
                    continue

                parts = target.split("#", 1)
                file_part = parts[0]
                anchor_part = parts[1] if len(parts) > 1 else None

                target_file = (md_path.parent / file_part).resolve() if file_part else md_path
                if not target_file.exists():
                    broken_links.append(f"{md_path.relative_to(REPO_ROOT)}: '{target}' (file not found)")
                    continue

                if anchor_part and target_file.suffix == ".md":
                    anchors = _extract_anchors(target_file)
                    if anchor_part not in anchors:
                        broken_links.append(
                            f"{md_path.relative_to(REPO_ROOT)}: '{target}' (anchor #{anchor_part} not found in {target_file.name})"
                        )

        self.assertEqual(
            broken_links,
            [],
            f"Found {len(broken_links)} broken internal documentation links:\n" + "\n".join(broken_links),
        )

    def test_referenced_example_files_exist(self) -> None:
        """All examples/<file>.dub references in documentation must exist on disk."""
        ref_pattern = re.compile(r"examples/([a-zA-Z0-9_\-]+\.dub)")
        md_files = sorted(DOCS_DIR.glob("**/*.md")) + [REPO_ROOT / "README.md"]
        missing_refs: list[str] = []

        for md_path in md_files:
            if not md_path.exists():
                continue
            content = md_path.read_text(encoding="utf-8")
            for filename in ref_pattern.findall(content):
                expected_path = REPO_ROOT / "examples" / filename
                if not expected_path.exists():
                    missing_refs.append(f"{md_path.relative_to(REPO_ROOT)} references non-existent examples/{filename}")

        self.assertEqual(
            missing_refs,
            [],
            f"Found {len(missing_refs)} references to non-existent example files:\n" + "\n".join(missing_refs),
        )

    def test_utf8_and_cuneiform_codepoint_validity(self) -> None:
        """All documentation and source files must be valid UTF-8 with authentic cuneiform codepoints."""
        extensions = {".md", ".dub", ".py", ".c", ".h", ".yml", ".yaml"}
        encoding_errors: list[str] = []

        for path in sorted(REPO_ROOT.rglob("*")):
            if path.is_dir() or path.suffix not in extensions:
                continue
            if ".git" in path.parts:
                continue

            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                encoding_errors.append(f"{path.relative_to(REPO_ROOT)}: UTF-8 decode error: {exc}")
                continue

            if "\ufffd" in content:
                encoding_errors.append(
                    f"{path.relative_to(REPO_ROOT)}: contains Unicode replacement character U+FFFD"
                )

            # Check that cuneiform characters belong to valid Unicode cuneiform blocks:
            # U+12000 - U+123FF: Cuneiform
            # U+12400 - U+1247F: Cuneiform Numbers and Punctuation
            # U+12480 - U+1254F: Early Dynastic Cuneiform
            for line_idx, line in enumerate(content.splitlines(), 1):
                for ch in line:
                    cp = ord(ch)
                    if 0x12000 <= cp <= 0x12FFF:
                        if not (
                            (0x12000 <= cp <= 0x123FF)
                            or (0x12400 <= cp <= 0x1247F)
                            or (0x12480 <= cp <= 0x1254F)
                        ):
                            encoding_errors.append(
                                f"{path.relative_to(REPO_ROOT)}:{line_idx}: invalid cuneiform codepoint U+{cp:04X}"
                            )

        self.assertEqual(
            encoding_errors,
            [],
            f"Found {len(encoding_errors)} encoding issues:\n" + "\n".join(encoding_errors),
        )

    def test_tutorial_examples_against_native_compiler(self) -> None:
        """Verifies that representative tutorial examples compile and execute cleanly with NativeCompiler."""
        test_cases = [
            (
                "learn-first-tablet-pythagoras",
                """
problem
    width : 3 meter
    height : 4 meter
    w_sq : width width multiply
    h_sq : height height multiply
    hyp_sq : w_sq h_sq add
    hyp : hyp_sq square-root
result
    hyp
""",
                ["5"],
            ),
            (
                "learn-exact-arithmetic-addition",
                """
problem
    a : 0;30
    b : 0;20
    s : a + b
    p : 5 * 5
result
    output s
    output p
""",
                ["0;50", "25"],
            ),
            (
                "learn-bounded-search-sum",
                """
problem
    total : 0
    consider i from 1 through 10:
        total : total + i
result
    total
""",
                ["55"],
            ),
            (
                "learn-selection-retain",
                """
problem
    best : empty
    consider x from 1 through 10:
        sq : x * x
        retain x when sq <= 50
result
    best
""",
                ["7"],
            ),
        ]

        nc = NativeCompiler()
        for name, code, expected in test_cases:
            with self.subTest(example=name):
                ast = Parser(Lexer(code).tokenize()).parse()
                SemanticAnalyzer().analyze(ast)
                ret, stdout, stderr = nc.run(ast)
                self.assertEqual(ret, 0, f"Native execution failed for {name}:\n{stderr}")
                self.assertEqual(stdout, expected, f"Native output mismatch for {name}")

    def test_tutorial_examples_against_wasm_compiler(self) -> None:
        """Verifies that representative tutorial examples compile to valid WebAssembly Text (.wat)."""
        test_cases = [
            """
problem
    width : 3 meter
    height : 4 meter
    w_sq : width width multiply
    h_sq : height height multiply
    hyp_sq : w_sq h_sq add
    hyp : hyp_sq square-root
result
    hyp
""",
            """
problem
    total : 0
    consider i from 1 through 10:
        total : total + i
result
    total
""",
            """
problem
    best : empty
    consider x from 1 through 10:
        sq : x * x
        retain x when sq <= 50
result
    best
""",
        ]

        wc = WasmCompiler()
        for idx, code in enumerate(test_cases, 1):
            with self.subTest(case=idx):
                ast = Parser(Lexer(code).tokenize()).parse()
                SemanticAnalyzer().analyze(ast)
                wat = wc.compile(ast)
                self.assertIn("(module", wat, "Compiled WAT must contain a top-level (module) declaration")
                self.assertIn('(func (export "run")', wat, "Compiled WAT must export a run function")


if __name__ == "__main__":
    unittest.main()

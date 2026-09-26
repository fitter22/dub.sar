"""Tests verifying executable DUB.SAR code blocks in documentation."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer
from dubsar.vm import VirtualMachine

EXPECTED_OUTPUTS: dict[tuple[str, int], list[str]] = {
    ("docs/learn/first-tablet.md", 1): ["5 length"],
    ("docs/learn/first-tablet.md", 2): ["5 length"],
    ("docs/index.md", 1): ["5 length"],
    ("docs/index.md", 2): ["5 length"],
    ("docs/learn/quantities.md", 1): ["12", "0;45", "1;30", "0;20"],
    ("docs/learn/quantities.md", 2): ["5 time"],
    ("docs/learn/quantities.md", 3): ["5 time"],
    ("docs/learn/exact-arithmetic.md", 1): ["0;50", "25"],
    ("docs/learn/units.md", 1): ["2;5 nindan"],
    ("docs/learn/pipelines.md", 1): ["5 length"],
    ("docs/learn/pipelines.md", 2): ["5 length"],
    ("docs/learn/selection.md", 1): ["12 length^2"],
    ("docs/learn/selection.md", 2): ["25"],
    ("docs/learn/search.md", 1): ["55"],
    ("docs/learn/search.md", 2): ["55"],
    ("docs/learn/sequences.md", 1): ["3", "12", "18"],
    ("docs/learn/sequences.md", 2): ["3", "12", "18"],
    ("docs/learn/sequences.md", 3): ["20"],
    ("docs/learn/sequences.md", 4): ["20"],
    ("docs/learn/archive.md", 1): ["0;15"],
    ("docs/learn/archive.md", 2): ["0;15"],
    ("docs/learn/archive.md", 3): ["42"],
    ("docs/learn/archive.md", 4): ["42"],
    ("docs/learn/complete-example.md", 1): ["128", "31", "0;0,0,2,42"],
    ("docs/learn/complete-example.md", 2): ["128", "31", "0;0,0,2,42"],
    ("docs/guide/calculations.md", 1): ["35"],
    ("docs/guide/determinations.md", 1): ["360 length^2"],
    ("docs/guide/domains-and-selection.md", 1): ["5050"],
    ("docs/guide/domains-and-selection.md", 2): ["7"],
    ("docs/guide/source-modes.md", 1): ["1 day"],
    ("docs/guide/source-modes.md", 2): ["1 day"],
    ("docs/guide/units.md", 1): ["24 hour", "120 mina"],
}


class TestDocsExamples(unittest.TestCase):
    """Verifies that all standalone tablet examples in docs/ parse and execute cleanly."""

    tablets: list[tuple[Path, int, str]] = []

    @classmethod
    def setUpClass(cls) -> None:
        repo_root = Path(__file__).resolve().parent.parent
        docs_dir = repo_root / "docs"
        md_files = list(docs_dir.glob("**/*.md"))
        cls.tablets = []

        seen_files = set()
        for fpath in sorted(md_files):
            if fpath in seen_files or not fpath.exists():
                continue
            seen_files.add(fpath)
            text = fpath.read_text(encoding="utf-8")
            blocks = re.findall(r"```dubsar\n(.*?)```", text, re.DOTALL)
            for idx, code in enumerate(blocks, 1):
                stripped = code.strip()
                if ("problem" in stripped or "𒂊𒁹" in stripped) and ("result" in stripped or "𒅗𒁹" in stripped):
                    cls.tablets.append((fpath.relative_to(repo_root), idx, stripped))

    def test_found_tablets(self) -> None:
        """Ensures documentation contains executable tablet examples."""
        self.assertGreaterEqual(len(self.tablets), 25, "Expected at least 25 standalone tablet blocks in docs")

    def test_documentation_tablets_execute(self) -> None:
        """Tokenizes, parses, semantically analyzes, and executes all documentation tablets."""
        for rel_path, idx, code in self.tablets:
            with self.subTest(file=str(rel_path), block=idx):
                tokens = Lexer(code, source_file=str(rel_path)).tokenize()
                ast = Parser(tokens, source_file=str(rel_path)).parse()

                SemanticAnalyzer(source_file=str(rel_path)).analyze(ast)

                out_interp: list[str] = []
                interp = Interpreter(
                    input_fn=lambda _: "1",
                    output_fn=out_interp.append,
                    source_file=str(rel_path),
                )
                interp.run(ast)

                compiled = Compiler().compile(ast)
                out_vm: list[str] = []
                vm = VirtualMachine(
                    input_fn=lambda _: "1",
                    output_fn=out_vm.append,
                )
                vm.execute(compiled)

                self.assertEqual(
                    out_interp,
                    out_vm,
                    f"Output divergence between Interpreter and VM in {rel_path} block #{idx}: {out_interp} vs {out_vm}",
                )

                key = (str(rel_path), idx)
                if key in EXPECTED_OUTPUTS:
                    self.assertEqual(
                        out_interp,
                        EXPECTED_OUTPUTS[key],
                        f"Expected output mismatch in {rel_path} block #{idx}: got {out_interp}, expected {EXPECTED_OUTPUTS[key]}",
                    )


if __name__ == "__main__":
    unittest.main()

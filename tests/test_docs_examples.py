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

EXPECTED_OUTPUTS: dict[str | tuple[str, int], list[str]] = {
    # Stable test IDs for documentation examples
    "home-first-tablet-scholar": ["5 length"],
    "home-first-tablet-cuneiform": ["5 length"],
    "learn-first-tablet-scholar": ["5 length"],
    "learn-first-tablet-cuneiform": ["5 length"],
    "learn-quantities-literals": ["12", "0;45", "1;30", "0;20"],
    "learn-quantities-metrological": ["5 time"],
    "learn-quantities-mixed": ["5 time"],
    "learn-exact-arithmetic-runnable": ["0;50", "25"],
    "learn-units-dimensional": ["2;5 nindan"],
    "learn-pipelines-scholar": ["5 length"],
    "learn-pipelines-cuneiform": ["5 length"],
    "learn-search-scholar": ["55"],
    "learn-search-cuneiform": ["55"],
    "learn-selection-records": ["12 length^2"],
    "learn-selection-retain": ["25"],
    "learn-sequences-working-scholar": ["3", "12", "18"],
    "learn-sequences-working-mixed": ["3", "12", "18"],
    "learn-sequences-indexing-scholar": ["20"],
    "learn-sequences-indexing-mixed": ["20"],
    "learn-archive-reciprocals-scholar": ["0;15"],
    "learn-archive-reciprocals-mixed": ["0;15"],
    "learn-archive-working-scholar": ["42"],
    "learn-archive-working-cuneiform": ["42"],
    "learn-complete-example-scholar": ["128", "31", "0;0,0,2,42"],
    "learn-complete-example-cuneiform": ["128", "31", "0;0,0,2,42"],

    # Guide fallbacks keyed by (filename, block_idx)
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

    tablets: list[tuple[Path, int, str, str | None]] = []

    @classmethod
    def setUpClass(cls) -> None:
        repo_root = Path(__file__).resolve().parent.parent
        docs_dir = repo_root / "docs"
        md_files = list(docs_dir.glob("**/*.md"))
        cls.tablets = []

        seen_files = set()
        pattern = re.compile(
            r"(?:<!--\s*test-id:\s*(?P<html_id>[a-zA-Z0-9_\-/]+)\s*-->\s*)?```dubsar\n(?P<code>.*?)```",
            re.DOTALL,
        )
        for fpath in sorted(md_files):
            if fpath in seen_files or not fpath.exists():
                continue
            seen_files.add(fpath)
            text = fpath.read_text(encoding="utf-8")
            for idx, m in enumerate(pattern.finditer(text), 1):
                code = m.group("code")
                stripped = code.strip()
                if ("problem" in stripped or "𒂊𒁹" in stripped) and ("result" in stripped or "𒅗𒁹" in stripped):
                    tablet_id = m.group("html_id")
                    if not tablet_id:
                        first_line = stripped.split("\n", 1)[0].strip()
                        id_m = re.match(r"^(?:#|𒑰)\s*test-id:\s*([a-zA-Z0-9_\-/]+)", first_line)
                        if id_m:
                            tablet_id = id_m.group(1)
                    cls.tablets.append((fpath.relative_to(repo_root), idx, stripped, tablet_id))

    def test_found_tablets(self) -> None:
        """Ensures documentation contains executable tablet examples."""
        self.assertGreaterEqual(len(self.tablets), 25, "Expected at least 25 standalone tablet blocks in docs")

    def test_documentation_tablets_execute(self) -> None:
        """Tokenizes, parses, semantically analyzes, and executes all documentation tablets."""
        for rel_path, idx, code, tablet_id in self.tablets:
            with self.subTest(file=str(rel_path), block=idx, id=tablet_id):
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

                expected = None
                if tablet_id and tablet_id in EXPECTED_OUTPUTS:
                    expected = EXPECTED_OUTPUTS[tablet_id]
                elif (str(rel_path), idx) in EXPECTED_OUTPUTS:
                    expected = EXPECTED_OUTPUTS[(str(rel_path), idx)]

                if expected is not None:
                    self.assertEqual(
                        out_interp,
                        expected,
                        f"Expected output mismatch in {rel_path} block #{idx} (id: {tablet_id}): got {out_interp}, expected {expected}",
                    )


if __name__ == "__main__":
    unittest.main()

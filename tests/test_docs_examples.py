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
                self.assertIsNotNone(out_interp)

                compiled = Compiler().compile(ast)
                out_vm: list[str] = []
                vm = VirtualMachine(
                    input_fn=lambda _: "1",
                    output_fn=out_vm.append,
                )
                vm.execute(compiled)
                self.assertIsNotNone(out_vm)


if __name__ == "__main__":
    unittest.main()

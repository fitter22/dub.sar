"""Tests verifying the execution and conformance of all catalog examples."""

from __future__ import annotations

import unittest
from pathlib import Path

from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer
from dubsar.vm import VirtualMachine

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


def parse_example_header(path: Path) -> dict:
    """Extracts metadata and expected output lines from an example tablet header."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    meta: dict = {
        "title": None,
        "difficulty": None,
        "concept": None,
        "mode": None,
        "purpose": "",
        "expected_output": [],
    }
    purpose_lines: list[str] = []
    in_expected = False
    in_purpose = False

    for line in lines:
        raw = line.strip()
        if not (raw.startswith("#") or raw.startswith("𒑰")):
            if raw == "" and (in_expected or in_purpose):
                in_expected = False
                in_purpose = False
                continue
            if not raw:
                continue
            break

        comment = raw.lstrip("# 𒑰\t").strip()
        if "Example:" in comment:
            meta["title"] = comment.split("Example:", 1)[1].strip()
            in_expected = in_purpose = False
        elif comment.startswith("Difficulty:"):
            meta["difficulty"] = comment.split(":", 1)[1].strip()
            in_expected = in_purpose = False
        elif comment.startswith("Concept:"):
            meta["concept"] = comment.split(":", 1)[1].strip()
            in_expected = in_purpose = False
        elif comment.startswith("Mode:"):
            meta["mode"] = comment.split(":", 1)[1].strip()
            in_expected = in_purpose = False
        elif comment.startswith("Purpose:"):
            in_purpose = True
            in_expected = False
        elif comment.startswith("Expected Output:"):
            in_expected = True
            in_purpose = False
        elif in_purpose:
            if comment:
                purpose_lines.append(comment)
        elif in_expected:
            if comment:
                meta["expected_output"].append(comment)

    meta["purpose"] = " ".join(purpose_lines)
    return meta


class TestExamplesCatalog(unittest.TestCase):
    """Verifies that all catalog examples adhere to standards and execute cleanly."""

    def setUp(self) -> None:
        self.example_paths = sorted(EXAMPLES_DIR.glob("*.dub"))

    def test_example_file_count_and_pairing(self) -> None:
        """Every example must exist in both Scholar and Tablet/Mixed modes."""
        self.assertGreaterEqual(
            len(self.example_paths),
            20,
            "Expected a substantial catalog of example tablets",
        )

        scholar_bases = {
            p.stem[:-8] for p in self.example_paths if p.stem.endswith("_scholar")
        }
        paired_bases = {
            p.stem for p in self.example_paths if not p.stem.endswith("_scholar")
        }

        self.assertEqual(
            scholar_bases,
            paired_bases,
            "Every example must exist in both Scholar (*_scholar.dub) and Tablet/Mixed (*.dub) modes",
        )

    def test_example_headers_complete(self) -> None:
        """All examples must contain valid header metadata adhering to specification."""
        valid_difficulties = {
            "Beginner",
            "Intermediate",
            "Advanced",
            "Mastery",
            "Exemplar",
        }
        pure_cuneiform_tablets = {
            "babylonian_sqrt2.dub",
            "even_distribution.dub",
            "planetary_leap.dub",
            "reciprocal_lookup.dub",
        }

        for path in self.example_paths:
            with self.subTest(file=path.name):
                meta = parse_example_header(path)
                self.assertTrue(
                    meta["title"],
                    f"{path.name} is missing Title in header",
                )
                self.assertIn(
                    meta["difficulty"],
                    valid_difficulties,
                    f"{path.name} has invalid difficulty {meta['difficulty']}",
                )
                self.assertTrue(
                    meta["concept"],
                    f"{path.name} is missing Concept in header",
                )
                self.assertTrue(
                    meta["purpose"],
                    f"{path.name} is missing Purpose in header",
                )
                self.assertTrue(
                    len(meta["expected_output"]) > 0,
                    f"{path.name} is missing Expected Output in header",
                )

                # Validate Mode matches file type and content
                if path.name.endswith("_scholar.dub"):
                    self.assertEqual(
                        meta["mode"],
                        "Scholar (Latin transliteration)",
                        f"{path.name} should declare Scholar mode",
                    )
                elif path.name in pure_cuneiform_tablets:
                    self.assertEqual(
                        meta["mode"],
                        "Tablet (Canonical Cuneiform)",
                        f"{path.name} should declare Tablet (Canonical Cuneiform) mode",
                    )
                else:
                    self.assertEqual(
                        meta["mode"],
                        "Mixed (Cuneiform syntax with Latin identifiers)",
                        f"{path.name} should declare Mixed mode",
                    )

    def test_examples_execution_and_output_parity(self) -> None:
        """All examples must execute identically on both Interpreter and VM matching expected output."""
        for path in self.example_paths:
            with self.subTest(file=path.name):
                meta = parse_example_header(path)
                expected = meta["expected_output"]

                # Handle stdin for planetary_leap
                input_str = "365;14,31,55" if "planetary_leap" in path.name else ""

                interp = Interpreter(output_fn=lambda _: None, input_fn=lambda _: input_str)
                vm = VirtualMachine(output_fn=lambda _: None, input_fn=lambda _: input_str)

                # Precondition archive for ea_nasir_revision
                if "ea_nasir_revision" in path.name:
                    base_name = (
                        "ea_nasir_scholar.dub"
                        if "scholar" in path.name
                        else "ea_nasir.dub"
                    )
                    base_path = EXAMPLES_DIR / base_name
                    base_ast = Parser(Lexer(base_path.read_text(encoding="utf-8")).tokenize()).parse()
                    interp.run(base_ast)
                    interp.outputs.clear()

                    base_chunk = Compiler().compile(base_ast)
                    vm.execute(base_chunk)

                tokens = Lexer(path.read_text(encoding="utf-8")).tokenize()
                ast = Parser(tokens).parse()
                SemanticAnalyzer().analyze(ast)

                out_interp = interp.run(ast)
                chunk = Compiler().compile(ast)
                out_vm = vm.execute(chunk)

                self.assertEqual(
                    out_interp,
                    expected,
                    f"Interpreter output mismatch for {path.name}",
                )
                self.assertEqual(
                    out_vm,
                    expected,
                    f"VM output mismatch for {path.name}",
                )
                self.assertEqual(
                    out_interp,
                    out_vm,
                    f"Parity mismatch between Interpreter and VM for {path.name}",
                )


if __name__ == "__main__":
    unittest.main()

"""Tests for the dubsar Command Line Interface."""

import tempfile
import unittest
from pathlib import Path

from dubsar.cli import main


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dub_file = Path(self.temp_dir.name) / "test.dub"
        self.dub_file.write_text("""PROBLEM
    a : 40
    b : 2
    c := a + b
RESULT
    output "answer:"
    output c
""", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_cli_check(self):
        code = main(["check", str(self.dub_file)])
        self.assertEqual(code, 0)

    def test_cli_run_vm(self):
        code = main(["run", str(self.dub_file), "--backend=vm"])
        self.assertEqual(code, 0)

    def test_cli_run_ast(self):
        code = main(["run", str(self.dub_file), "--backend=ast"])
        self.assertEqual(code, 0)

    def test_cli_compile_bytecode(self):
        code = main(["compile", str(self.dub_file), "--target=bytecode"])
        self.assertEqual(code, 0)

    def test_cli_compile_wasm(self):
        code = main(["compile", str(self.dub_file), "--target=wasm"])
        self.assertEqual(code, 0)

    def test_cli_compile_json(self):
        code = main(["compile", str(self.dub_file), "--target=json"])
        self.assertEqual(code, 0)

    def test_cli_transliterate(self):
        code = main(["transliterate", str(self.dub_file)])
        self.assertEqual(code, 0)

    def test_cli_cuneiform(self):
        code = main(["cuneiform", str(self.dub_file)])
        self.assertEqual(code, 0)

    def test_cli_render(self):
        out_svg = Path(self.temp_dir.name) / "test.svg"
        code = main(["render", str(self.dub_file), "--style=svg", "-o", str(out_svg)])
        self.assertEqual(code, 0)
        self.assertTrue(out_svg.exists())


if __name__ == "__main__":
    unittest.main()

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

    def test_cli_format(self):
        out_fmt = Path(self.temp_dir.name) / "formatted.dub"
        code = main(["format", str(self.dub_file), "--mode=scholar", "-o", str(out_fmt)])
        self.assertEqual(code, 0)
        self.assertTrue(out_fmt.exists())
        content = out_fmt.read_text(encoding="utf-8")
        self.assertIn("PROBLEM", content)
        self.assertIn("a : 40", content)

    def test_cli_error_diagnostic(self):
        bad_file = Path(self.temp_dir.name) / "bad.dub"
        bad_file.write_text("PROBLEM\n    x := 1 day + 2 year\nRESULT\n    output x\n", encoding="utf-8")
        code = main(["check", str(bad_file)])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()

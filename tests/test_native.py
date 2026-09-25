"""DUB.SAR 1.0 — Native Compiler Test Suite (Stage 4).

Tests C99 generation, LLVM IR emission, native compilation, toolchain driver,
CLI integration, exact rational preservation, geometric mathematics, tablet model,
and Fourier transforms.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from dubsar.lexer import Lexer
from dubsar.native.compiler import NativeCompiler
from dubsar.parser import Parser


class TestNativeCompilerToolchain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.has_cc = shutil.which("clang") or shutil.which("gcc") or shutil.which("cc")
        if not cls.has_cc:
            raise unittest.SkipTest("No host C compiler (clang/gcc/cc) available.")
        cls.compiler = NativeCompiler()

    def _parse(self, source: str):
        tokens = Lexer(source).tokenize()
        return Parser(tokens).parse()

    def test_c_code_generation(self):
        source = """problem:
    a : 10
    b : 20
    c := a + b
result:
    c
"""
        prog = self._parse(source)
        c_code = self.compiler.generate_c(prog)
        self.assertIn('#include "dubsar_runtime.h"', c_code)
        self.assertIn("void dubsar_program_run(void)", c_code)
        self.assertIn("dubsar_val_add", c_code)
        self.assertIn("dubsar_print_val", c_code)

    def test_llvm_ir_generation(self):
        if not shutil.which("clang"):
            self.skipTest("Generating LLVM IR requires clang.")
        source = """problem:
    x : 42
result:
    x
"""
        prog = self._parse(source)
        llvm_ir = self.compiler.generate_llvm(prog)
        self.assertIn("target triple", llvm_ir)
        self.assertIn("@dubsar_program_run", llvm_ir)

    def test_shared_library_generation(self):
        source = """problem:
    x : 100
result:
    x
"""
        prog = self._parse(source)
        with tempfile.TemporaryDirectory(prefix="dubsar_shlib_") as tmpdir:
            ext = ".dylib" if sys.platform == "darwin" else ".so"
            out_file = Path(tmpdir) / f"libtablet{ext}"
            compiled_path = self.compiler.compile(prog, output_path=out_file, target="shared")
            self.assertTrue(compiled_path.exists())
            self.assertGreater(compiled_path.stat().st_size, 0)


class TestNativeExecution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.has_cc = shutil.which("clang") or shutil.which("gcc") or shutil.which("cc")
        if not cls.has_cc:
            raise unittest.SkipTest("No host C compiler available.")
        cls.compiler = NativeCompiler()

    def _run_source(self, source: str, input_preset: str = None):
        tokens = Lexer(source).tokenize()
        prog = Parser(tokens).parse()
        code, out_lines, stderr = self.compiler.run(prog, input_preset=input_preset)
        self.assertEqual(code, 0, f"Native run failed with code {code}:\n{stderr}")
        return out_lines

    def test_arithmetic_and_builtins(self):
        source = """problem:
    a : 15
    b : 4
    sum_val := a + b
    sub_val := a - b
    mul_val := a * b
    div_val := a / b
    mod_val := a % b
    flr : 7 2 divide floor
    cil : 7 2 divide ceil
    nst : 7 2 divide nearest
    ab : -5 absolute
result:
    sum_val
    sub_val
    mul_val
    div_val
    mod_val
    flr
    cil
    nst
    ab
"""
        out = self._run_source(source)
        self.assertEqual(out[0], "19")
        self.assertEqual(out[1], "11")
        self.assertEqual(out[2], "60")
        self.assertEqual(out[3], "3;45")
        self.assertEqual(out[4], "3")
        self.assertEqual(out[5], "3")
        self.assertEqual(out[6], "4")
        self.assertEqual(out[7], "4")
        self.assertEqual(out[8], "5")

    def test_procedures_and_recursion(self):
        source = """problem:
    ans := factorial(5)
procedure factorial(n):
    if n <= 1:
        return 1
    sub_n := n - 1
    sub_res := factorial(sub_n)
    return n * sub_res
result:
    ans
"""
        out = self._run_source(source)
        self.assertEqual(out, ["120"])

    def test_loops_and_retain(self):
        source = """problem:
    best : empty
    consider i from 1 through 5:
        c : i * i
        retain c when c is greater than best
result:
    best
"""
        out = self._run_source(source)
        self.assertEqual(out, ["25"])

    def test_determinations_and_fields(self):
        source = """problem:
    n : 33
    d : 8
    candidate : n, d
    num : candidate.n
    den : candidate.d
result:
    num
    den
"""
        out = self._run_source(source)
        self.assertEqual(out, ["33", "8"])

    def test_tablets_and_take(self):
        source = """problem:
    working seq of length 0
    append 10 to seq
    append 20 to seq
    append 30 to seq
    append 40 to seq
    sz : length of seq
    fst : first from seq
    lst : last from seq
result:
    sz
    fst
    lst
"""
        out = self._run_source(source)
        self.assertEqual(out, ["4", "10", "40"])

    def test_tablet_archive_lookups(self):
        source = """problem:
    tri : take "3-4-5" from "right-triangles"
    diag : tri.diagonal
    ramp : take "standard-ramp" from "inclinations"
    fd : ramp.feed
result:
    diag
    fd
"""
        out = self._run_source(source)
        self.assertEqual(out, ["5", "3"])

    def test_geometric_triangles_and_validation(self):
        source = """problem:
    tri : 5 12 right-triangle
    valid : tri validate-triangle
    diag : tri.diagonal
    inc : tri.inclination
    fd : tri.feed
    area : tri.area
result:
    valid
    diag
    inc
    fd
    area
"""
        out = self._run_source(source)
        self.assertEqual(out, ["1", "13", "2;24", "0;25", "30"])

    def test_geometric_inclinations_turns_and_directions(self):
        source = """problem:
    slope : 1 2 inclination
    inc : slope.inclination
    fd : slope.feed
    base_dir : quarter-turn direction
    rotated_dir : base_dir eighth-turn rotate
    force : 10 meter quarter-turn rotate
result:
    inc
    fd
    base_dir
    rotated_dir
    force
"""
        out = self._run_source(source)
        self.assertEqual(out, [
            "0;30",
            "2",
            "direction(quarter-turn)",
            "direction(0;22,30-turn)",
            "10 meter along direction(quarter-turn)",
        ])

    def test_fourier_dft_and_fft(self):
        source = """problem:
    working sig of length 0
    sig 1 append
    sig 1 append
    sig 1 append
    sig 1 append
    spectrum_dft : sig dft
    first_dft : spectrum_dft 0 take
    mag_dft : first_dft.magnitude

    spectrum_fft : sig fft
    first_fft : spectrum_fft 0 take
    mag_fft : first_fft.magnitude
result:
    mag_dft
    mag_fft
"""
        out = self._run_source(source)
        self.assertEqual(out, ["4", "4"])

    def test_exact_rational_preservation(self):
        source = """problem
    solar-year : ask "solar year in days"
    limit : 200
    whole-days : solar-year floor
    fraction : solar-year whole-days subtract
    best : empty
    consider cycle from 1 through limit:
        leaps : cycle fraction multiply nearest
        error : whole-days leaps cycle divide add solar-year subtract absolute
        candidate : cycle, leaps, error
        retain candidate when error of candidate is lesser than error of best
result
    best.cycle
"""
        out = self._run_source(source, input_preset="365.2422")
        self.assertEqual(out, ["128"])


class TestNativeCLI(unittest.TestCase):
    def test_cli_run_backend_native(self):
        cmd = [
            sys.executable,
            "-m",
            "dubsar",
            "run",
            "examples/geometry_triangle_scholar.dub",
            "--backend=native",
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"CLI run failed:\n{res.stderr}")
        lines = [line for line in res.stdout.splitlines() if line]
        self.assertEqual(lines, ["1", "13", "2;24", "0;25", "30", "1"])

    def test_cli_compile_native_and_execute(self):
        with tempfile.TemporaryDirectory(prefix="dubsar_cli_") as tmpdir:
            bin_path = Path(tmpdir) / "geo_tri_bin"
            comp_cmd = [
                sys.executable,
                "-m",
                "dubsar",
                "compile",
                "examples/geometry_triangle_scholar.dub",
                "--target=native",
                "-o",
                str(bin_path),
            ]
            comp_res = subprocess.run(comp_cmd, capture_output=True, text=True)
            self.assertEqual(comp_res.returncode, 0, f"CLI compile failed:\n{comp_res.stderr}")
            self.assertTrue(bin_path.exists())

            run_res = subprocess.run([str(bin_path)], capture_output=True, text=True)
            self.assertEqual(run_res.returncode, 0)
            lines = [line for line in run_res.stdout.splitlines() if line]
            self.assertEqual(lines, ["1", "13", "2;24", "0;25", "30", "1"])

    def test_cli_compile_c(self):
        with tempfile.TemporaryDirectory(prefix="dubsar_cli_") as tmpdir:
            c_path = Path(tmpdir) / "output.c"
            cmd = [
                sys.executable,
                "-m",
                "dubsar",
                "compile",
                "examples/geometry_triangle_scholar.dub",
                "--target=c",
                "-o",
                str(c_path),
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)
            self.assertTrue(c_path.exists())
            content = c_path.read_text(encoding="utf-8")
            self.assertIn("#include \"dubsar_runtime.h\"", content)


if __name__ == "__main__":
    unittest.main()

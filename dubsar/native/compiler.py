"""DUB.SAR 1.0 — Native Compiler & Toolchain Driver (Stage 4).

Drives host C compiler (clang / gcc) to build native executables, shared libraries,
textual LLVM IR, or C source code.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

from dubsar.ast import Program
from dubsar.errors import DubSarError
from dubsar.native.codegen import NativeCodeGen, compile_to_c
from dubsar.semantic_ir import SemanticProgram


class NativeCompilerError(DubSarError):
    """Raised when native compilation or linking fails."""
    pass


class NativeCompiler:
    """Orchestrates native code generation, compilation, and execution."""

    def __init__(self, cc: Optional[str] = None) -> None:
        self.cc = cc or self._detect_cc()
        self.runtime_dir = Path(__file__).parent / "runtime"
        self.runtime_c = self.runtime_dir / "dubsar_runtime.c"
        self.runtime_h = self.runtime_dir / "dubsar_runtime.h"

    def _detect_cc(self) -> str:
        """Finds host C compiler (clang preferred, fallback to gcc or cc)."""
        for candidate in ("clang", "gcc", "cc"):
            path = shutil.which(candidate)
            if path:
                return candidate
        raise NativeCompilerError(
            "No host C compiler found. Please install clang or gcc to use the native compiler backend."
        )

    def generate_c(self, program: Program | SemanticProgram) -> str:
        """Generates standalone C99 source code."""
        return compile_to_c(program)

    def generate_llvm(self, program: Program | SemanticProgram) -> str:
        """Generates textual LLVM IR (.ll) using host clang."""
        if "clang" not in self.cc and not shutil.which("clang"):
            raise NativeCompilerError("Generating LLVM IR requires clang.")
        clang_bin = shutil.which("clang") or "clang"

        c_code = self.generate_c(program)
        with tempfile.TemporaryDirectory(prefix="dubsar_llvm_") as tmpdir:
            c_file = Path(tmpdir) / "program.c"
            c_file.write_text(c_code, encoding="utf-8")
            ll_file = Path(tmpdir) / "program.ll"

            cmd = [
                clang_bin,
                "-S",
                "-emit-llvm",
                "-O3",
                f"-I{self.runtime_dir}",
                str(c_file),
                "-o",
                str(ll_file),
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                raise NativeCompilerError(f"LLVM IR generation failed:\n{res.stderr}")

            return ll_file.read_text(encoding="utf-8")

    def compile(
        self,
        program: Program | SemanticProgram,
        output_path: Path | str,
        target: str = "native",
        opt_level: str = "-O3",
    ) -> Path:
        """Compiles a DUB.SAR program to the specified target."""
        out_path = Path(output_path).resolve()
        target = target.lower()

        if target == "c":
            c_code = self.generate_c(program)
            out_path.write_text(c_code, encoding="utf-8")
            return out_path

        if target in ("llvm", "ll"):
            ll_code = self.generate_llvm(program)
            out_path.write_text(ll_code, encoding="utf-8")
            return out_path

        c_code = self.generate_c(program)
        with tempfile.TemporaryDirectory(prefix="dubsar_compile_") as tmpdir:
            src_c = Path(tmpdir) / "tablet.c"
            src_c.write_text(c_code, encoding="utf-8")

            if target in ("shared", "dylib", "so"):
                cmd = [
                    self.cc,
                    opt_level,
                    "-shared",
                    "-fPIC",
                    f"-I{self.runtime_dir}",
                    str(self.runtime_c),
                    str(src_c),
                    "-lm",
                    "-o",
                    str(out_path),
                ]
            else:  # native executable
                cmd = [
                    self.cc,
                    opt_level,
                    f"-I{self.runtime_dir}",
                    str(self.runtime_c),
                    str(src_c),
                    "-lm",
                    "-o",
                    str(out_path),
                ]

            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                raise NativeCompilerError(f"Native compilation failed:\n{res.stderr}")

        return out_path

    def run(
        self,
        program: Program | SemanticProgram,
        input_preset: Optional[str] = None,
    ) -> Tuple[int, List[str], str]:
        """Compiles the tablet to a temporary native binary and executes it."""
        with tempfile.TemporaryDirectory(prefix="dubsar_run_") as tmpdir:
            bin_path = Path(tmpdir) / "tablet_native"
            self.compile(program, output_path=bin_path, target="native")

            cmd = [str(bin_path)]
            if input_preset is not None:
                cmd.append(f"--input={input_preset}")

            res = subprocess.run(cmd, capture_output=True, text=True)
            stdout_lines = [line for line in res.stdout.splitlines() if line]
            return res.returncode, stdout_lines, res.stderr

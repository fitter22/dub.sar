#!/usr/bin/env python3
"""Prepare browser assets for the DUB.SAR website.

Copies the example catalog, builds a wheel of this repository, and emits a
sample WebAssembly module from the language's WAT backend.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLES_DIR = REPO_ROOT / "examples"
PUBLIC_DIR = REPO_ROOT / "website" / "public"
RUNTIME_DIR = PUBLIC_DIR / "runtime"
RUNNER_SRC = REPO_ROOT / "website" / "runtime" / "runner.py"

SAMPLE_SOURCE = """problem
    width : 3 meter
    height : 4 meter
    w_sq : width width multiply
    h_sq : height height multiply
    hyp_sq : w_sq h_sq add
    hyp : hyp_sq square-root
result
    hyp
"""


def _header_text(line: str) -> str | None:
    stripped = line.strip()
    if stripped.startswith("#"):
        return stripped[1:].strip()
    if stripped.startswith("𒑰"):
        return stripped[len("𒑰") :].strip()
    return None


def parse_example(path: Path) -> dict[str, str]:
    """Read catalog metadata and source from one example tablet."""
    source = path.read_text(encoding="utf-8")
    title = path.stem.replace("_", " ")
    difficulty = "unspecified"
    mode = "scholar"
    concept = ""
    purpose_lines: list[str] = []
    capturing_purpose = False

    for raw_line in source.splitlines():
        text = _header_text(raw_line)
        if text is None:
            if raw_line.strip() == "" and (title or purpose_lines or concept):
                continue
            break
        if not text:
            continue
        lower = text.lower()
        if "example:" in lower:
            title = text.split(":", 1)[1].strip()
            capturing_purpose = False
            continue
        if lower.startswith("expected"):
            capturing_purpose = False
            continue
        if ":" in text:
            key, value = text.split(":", 1)
            key = key.strip().lower()
            if key in {"difficulty", "mode", "concept", "purpose"}:
                value = value.strip()
                capturing_purpose = key == "purpose"
                if key == "difficulty":
                    difficulty = value.lower()
                elif key == "mode":
                    mode = _normalize_mode(value)
                elif key == "concept":
                    concept = value
                elif value:
                    purpose_lines.append(value)
                continue
        if capturing_purpose:
            purpose_lines.append(text)

    return {
        "id": path.stem,
        "title": title,
        "difficulty": difficulty,
        "mode": mode,
        "concept": concept,
        "purpose": " ".join(purpose_lines),
        "source": source,
    }


def _normalize_mode(value: str) -> str:
    text = value.lower()
    if "mixed" in text:
        return "mixed"
    if "tablet" in text:
        return "tablet"
    if "scholar" in text:
        return "scholar"
    return "scholar"


def build_catalog(examples_dir: Path) -> list[dict[str, str]]:
    """Build catalog entries for every tablet in the examples directory."""
    paths = sorted(examples_dir.glob("*.dub"))
    return [parse_example(path) for path in paths]


def _build_wheel(dest: Path) -> str:
    dest.mkdir(parents=True, exist_ok=True)
    for old in dest.glob("dubsar-*.whl"):
        old.unlink()
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-deps",
            "--no-build-isolation",
            "-w",
            str(dest),
            str(REPO_ROOT),
        ],
        cwd=REPO_ROOT,
    )
    wheels = sorted(dest.glob("dubsar-*.whl"))
    if len(wheels) != 1:
        raise SystemExit(f"Expected one dubsar wheel in {dest}, found {wheels}")
    return wheels[0].name


def _write_sample_wasm(dest: Path) -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from dubsar.lexer import Lexer
    from dubsar.parser import Parser
    from dubsar.wasm import compile_to_wat

    program = Parser(Lexer(SAMPLE_SOURCE).tokenize()).parse()
    wat_path = dest / "sample.wat"
    wat_path.write_text(compile_to_wat(program), encoding="utf-8")
    wat2wasm = shutil.which("wat2wasm")
    wasm_path = dest / "sample.wasm"
    if wasm_path.exists():
        wasm_path.unlink()
    if wat2wasm is None:
        print("wat2wasm not found; sample.wat was written and sample.wasm was skipped")
        return
    subprocess.check_call([wat2wasm, str(wat_path), "-o", str(wasm_path)])


def prepare() -> None:
    """Write catalog.json, the interpreter wheel, and the sample WASM module."""
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    if RUNTIME_DIR.exists():
        shutil.rmtree(RUNTIME_DIR)
    RUNTIME_DIR.mkdir(parents=True)
    catalog = build_catalog(EXAMPLES_DIR)
    (PUBLIC_DIR / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    shutil.copyfile(RUNNER_SRC, RUNTIME_DIR / "runner.py")
    wheel_name = _build_wheel(RUNTIME_DIR)
    _write_sample_wasm(RUNTIME_DIR)
    version = wheel_name.split("-")[1]
    manifest = {
        "version": version,
        "wheel": wheel_name,
        "runner": "runner.py",
        "sampleWat": "sample.wat",
        "sampleWasm": "sample.wasm" if (RUNTIME_DIR / "sample.wasm").exists() else None,
    }
    (RUNTIME_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Prepared {len(catalog)} examples and {wheel_name}")


if __name__ == "__main__":
    prepare()

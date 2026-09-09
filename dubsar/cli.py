"""DUB.SAR 1.0 — Command Line Interface (CLI).

Implements Section 24, CR-027, CR-028, CR-040, CR-041:
  dubsar run tablet.dub [--backend=vm|ast] [--format=canonical|sexagesimal|decimal] [--mode=auto|tablet|scholar]
  dubsar check tablet.dub [--mode=auto|tablet|scholar]
  dubsar compile tablet.dub [--target=bytecode|wasm|wat|ir|json]
  dubsar format tablet.dub [--mode=auto|tablet|scholar] [--inplace]
  dubsar transliterate tablet.dub
  dubsar cuneiform tablet.dub
  dubsar render tablet.dub --style=tablet|svg|text
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List, Optional

from dubsar.diagnostics import format_diagnostic
from dubsar.errors import DubSarError
from dubsar.formatter import detect_source_mode, format_source
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.normalizer import cuneiformize, transliterate
from dubsar.parser import Parser
from dubsar.renderer import render_svg, render_terminal_tablet
from dubsar.semantic import SemanticAnalyzer
from dubsar.wasm import compile_to_wat


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dubsar",
        description="DUB.SAR 1.0 — Executable Mesopotamian Mathematical Tablet Language",
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-command to run")

    # run
    run_p = subparsers.add_parser("run", help="Execute a DUB.SAR tablet")
    run_p.add_argument("file", type=str, help="Path to .dub source file")
    run_p.add_argument(
        "--backend",
        choices=["vm", "ast"],
        default="vm",
        help="Execution engine: stack VM (default) or AST interpreter",
    )
    run_p.add_argument("--input", type=str, default=None, help="Preset input value for the tablet")
    run_p.add_argument(
        "--format",
        choices=["canonical", "sexagesimal", "decimal"],
        default="canonical",
        help="Number presentation formatting",
    )
    run_p.add_argument(
        "--mode",
        choices=["auto", "tablet", "scholar", "mixed"],
        default="auto",
        help="Source language mode filter / detection",
    )

    # check
    check_p = subparsers.add_parser("check", help="Parse and semantically validate a tablet")
    check_p.add_argument("file", type=str, help="Path to .dub source file")
    check_p.add_argument(
        "--mode",
        choices=["auto", "tablet", "scholar", "mixed"],
        default="auto",
        help="Source language mode filter / detection",
    )

    # compile
    comp_p = subparsers.add_parser("compile", help="Compile a tablet to bytecode, WASM, or IR")
    comp_p.add_argument("file", type=str, help="Path to .dub source file")
    comp_p.add_argument(
        "--target",
        choices=["bytecode", "wasm", "wat", "ir", "json"],
        default="bytecode",
        help="Compilation target format",
    )
    comp_p.add_argument(
        "--mode",
        choices=["auto", "tablet", "scholar", "mixed"],
        default="auto",
        help="Source language mode filter / detection",
    )
    comp_p.add_argument("-o", "--output", type=str, default=None, help="Output destination file")

    # format
    fmt_p = subparsers.add_parser("format", help="Format and canonicalize tablet source code")
    fmt_p.add_argument("file", type=str, help="Path to .dub source file")
    fmt_p.add_argument(
        "--mode",
        choices=["auto", "tablet", "scholar"],
        default="auto",
        help="Canonical target style (tablet cuneiform, scholar Latin, or auto)",
    )
    fmt_p.add_argument("-i", "--inplace", action="store_true", help="Format file in place")
    fmt_p.add_argument("-o", "--output", type=str, default=None, help="Output destination file")

    # transliterate
    trans_p = subparsers.add_parser("transliterate", help="Convert Cuneiform/Tablet source to Scholar mode")
    trans_p.add_argument("file", type=str, help="Path to .dub source file")
    trans_p.add_argument("-o", "--output", type=str, default=None, help="Output destination file")

    # cuneiform
    cun_p = subparsers.add_parser("cuneiform", help="Convert Scholar mode source to canonical Cuneiform")
    cun_p.add_argument("file", type=str, help="Path to .dub source file")
    cun_p.add_argument("-o", "--output", type=str, default=None, help="Output destination file")

    # render
    rend_p = subparsers.add_parser("render", help="Render tablet source as clay artwork or terminal display")
    rend_p.add_argument("file", type=str, help="Path to .dub source file")
    rend_p.add_argument(
        "--style",
        choices=["tablet", "svg", "text"],
        default="tablet",
        help="Rendering presentation style: clay tablet SVG or terminal box text",
    )
    rend_p.add_argument(
        "--strip-comments",
        action="store_true",
        help="Omit comment lines ('#' and '𒑰') from the rendered tablet artwork",
    )
    rend_p.add_argument("-o", "--output", type=str, default=None, help="Output destination file")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return 1

    source: str = ""
    try:
        source = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        return 1

    detected_mode = detect_source_mode(source)

    try:
        if args.command == "run":
            tokens = Lexer(source, source_file=str(file_path)).tokenize()
            program = Parser(tokens, source_file=str(file_path)).parse()

            input_val = args.input
            if input_val is not None:
                in_fn = lambda prompt: input_val
            else:
                in_fn = input

            if args.backend == "vm":
                from dubsar.vm import VirtualMachine
                SemanticAnalyzer(source_file=str(file_path)).analyze(program)
                compiler = Compiler()
                compiled = compiler.compile(program)
                vm = VirtualMachine(input_fn=in_fn, output_fn=print, format_mode=args.format)
                vm.execute(compiled)
            else:
                interp = Interpreter(input_fn=in_fn, output_fn=print, source_file=str(file_path), format_mode=args.format)
                interp.run(program)
            return 0

        elif args.command == "check":
            tokens = Lexer(source, source_file=str(file_path)).tokenize()
            program = Parser(tokens, source_file=str(file_path)).parse()
            SemanticAnalyzer(source_file=str(file_path)).analyze(program)
            print(f"✓ Tablet '{file_path.name}' parsed and verified successfully (Mode: {detected_mode}).")
            return 0

        elif args.command == "compile":
            tokens = Lexer(source, source_file=str(file_path)).tokenize()
            program = Parser(tokens, source_file=str(file_path)).parse()
            SemanticAnalyzer(source_file=str(file_path)).analyze(program)

            if args.target in ("bytecode", "ir"):
                compiler = Compiler()
                compiled = compiler.compile(program)
                out_str = compiled.disassemble()
            elif args.target in ("wasm", "wat"):
                out_str = compile_to_wat(program)
            elif args.target == "json":
                def to_dict(obj: Any) -> Any:
                    if hasattr(obj, "__dict__"):
                        return {k: to_dict(v) for k, v in obj.__dict__.items()}
                    if isinstance(obj, list):
                        return [to_dict(x) for x in obj]
                    return str(obj)
                out_str = json.dumps(to_dict(program), indent=2, ensure_ascii=False)
            else:
                print(f"Unsupported target: {args.target}", file=sys.stderr)
                return 1

            if args.output:
                Path(args.output).write_text(out_str, encoding="utf-8")
                print(f"Compiled output written to: {args.output}")
            else:
                print(out_str)
            return 0

        elif args.command == "format":
            formatted = format_source(source, mode=args.mode)
            if args.inplace:
                file_path.write_text(formatted, encoding="utf-8")
                print(f"Formatted {file_path}")
            elif args.output:
                Path(args.output).write_text(formatted, encoding="utf-8")
                print(f"Formatted output written to: {args.output}")
            else:
                print(formatted)
            return 0

        elif args.command == "transliterate":
            result = transliterate(source)
            if args.output:
                Path(args.output).write_text(result, encoding="utf-8")
                print(f"Transliterated output written to: {args.output}")
            else:
                print(result)
            return 0

        elif args.command == "cuneiform":
            result = cuneiformize(source)
            if args.output:
                Path(args.output).write_text(result, encoding="utf-8")
                print(f"Cuneiform output written to: {args.output}")
            else:
                print(result)
            return 0

        elif args.command == "render":
            if args.style in ("tablet", "svg"):
                rendered = render_svg(
                    source,
                    title=f"TABLET: {file_path.stem.upper()}",
                    strip_comments=args.strip_comments,
                )
                out_dest = args.output if args.output else f"{file_path.stem}_tablet.svg"
                Path(out_dest).write_text(rendered, encoding="utf-8")
                print(f"Clay tablet SVG artwork rendered to: {out_dest}")
            else:
                rendered = render_terminal_tablet(
                    source,
                    title=f"TABLET: {file_path.stem.upper()}",
                    strip_comments=args.strip_comments,
                )
                if args.output:
                    Path(args.output).write_text(rendered, encoding="utf-8")
                    print(f"Text tablet rendered to: {args.output}")
                else:
                    print(rendered)
            return 0

    except DubSarError as err:
        diag = format_diagnostic(err, source_text=source, source_file=str(file_path))
        print(diag, file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())

"""DUB.SAR 1.0 — Command Line Interface (CLI).

Implements Section 24:
  dubsar run tablet.dub
  dubsar check tablet.dub
  dubsar compile tablet.dub --target=bytecode
  dubsar compile tablet.dub --target=wasm
  dubsar transliterate tablet.dub
  dubsar cuneiform tablet.dub
  dubsar render tablet.dub --style=tablet
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from dubsar.errors import DubSarError
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.normalizer import cuneiformize, transliterate
from dubsar.parser import Parser
from dubsar.renderer import render_svg, render_terminal_tablet
from dubsar.semantic import SemanticAnalyzer
from dubsar.vm import VirtualMachine
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

    # check
    check_p = subparsers.add_parser("check", help="Parse and semantically validate a tablet")
    check_p.add_argument("file", type=str, help="Path to .dub source file")

    # compile
    comp_p = subparsers.add_parser("compile", help="Compile a tablet to bytecode, WASM, or IR")
    comp_p.add_argument("file", type=str, help="Path to .dub source file")
    comp_p.add_argument(
        "--target",
        choices=["bytecode", "wasm", "wat", "ir", "json"],
        default="bytecode",
        help="Compilation target format",
    )
    comp_p.add_argument("-o", "--output", type=str, default=None, help="Output destination file")

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
    rend_p.add_argument("-o", "--output", type=str, default=None, help="Output destination file")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return 1

    try:
        source = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        return 1

    try:
        if args.command == "run":
            tokens = Lexer(source, source_file=str(file_path)).tokenize()
            program = Parser(tokens, source_file=str(file_path)).parse()

            # Set up input function
            input_val = args.input
            if input_val is not None:
                in_fn = lambda prompt: input_val
            else:
                in_fn = input

            if args.backend == "vm":
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
            print(f"✓ Tablet '{file_path.name}' parsed and verified successfully.")
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
                rendered = render_svg(source, title=f"TABLET: {file_path.stem.upper()}")
                out_dest = args.output if args.output else f"{file_path.stem}_tablet.svg"
                Path(out_dest).write_text(rendered, encoding="utf-8")
                print(f"Clay tablet SVG artwork rendered to: {out_dest}")
            else:
                rendered = render_terminal_tablet(source, title=f"TABLET: {file_path.stem.upper()}")
                if args.output:
                    Path(args.output).write_text(rendered, encoding="utf-8")
                    print(f"Text tablet rendered to: {args.output}")
                else:
                    print(rendered)
            return 0

    except DubSarError as err:
        print(f"DUB.SAR Error: {err}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())

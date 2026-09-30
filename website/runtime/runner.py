"""Browser entry point. Pyodide loads this file and calls execute()."""

from __future__ import annotations

import json
import traceback

from dubsar import __version__
from dubsar.diagnostics import format_diagnostic
from dubsar.errors import DubSarError, DubSarInputError
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.vm import VirtualMachine


def execute(source_text: str, backend_name: str, stdin_text: str) -> str:
    """Run one tablet and return a JSON object describing the outcome."""
    answers = iter(stdin_text.splitlines())

    def input_fn(_prompt: str) -> str:
        try:
            return next(answers)
        except StopIteration as exc:
            raise DubSarInputError(
                "This tablet asks for input. Put one answer on each line of the input box."
            ) from exc

    try:
        program = Parser(Lexer(source_text).tokenize()).parse()
        if backend_name == "vm":
            machine = VirtualMachine(input_fn=input_fn, output_fn=lambda _text: None)
            output = machine.execute(Compiler().compile(program))
        else:
            interpreter = Interpreter(input_fn=input_fn, output_fn=lambda _text: None)
            output = interpreter.run(program)
        payload = {
            "ok": True,
            "output": list(output),
            "version": __version__,
        }
    except DubSarError as exc:
        payload = {
            "ok": False,
            "diagnostic": format_diagnostic(exc, source_text),
            "version": __version__,
            "line": exc.line,
            "col": exc.col,
            "errorType": exc.__class__.__name__,
        }
    except Exception:
        payload = {
            "ok": False,
            "diagnostic": traceback.format_exc(),
            "version": __version__,
            "errorType": "InternalError",
        }
    return json.dumps(payload)

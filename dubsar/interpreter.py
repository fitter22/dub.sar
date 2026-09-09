"""DUB.SAR 1.0 — Reference Interpreter (Stage 1).

Implements Section 20 (Program Execution), Section 13 (Procedures),
Section 11 (Conditions), Section 12 (Repetitions), and Section 17 (I/O):
- Exact rational evaluation with first-class units
- Lexical environment stack with procedure local frames
- Tablet execution order: procedures -> problem -> result
- Pluggable I/O for interactive terminal, files, or programmatic capture
"""

from __future__ import annotations

import sys
from typing import Any, Callable, Dict, List, Optional, TextIO, Tuple, Union

from dubsar.ast import (
    Assignment,
    BinaryOp,
    CallExpr,
    Conditional,
    Declaration,
    Expression,
    ExpressionStatement,
    Identifier,
    InputExpr,
    NumberLiteral,
    OutputStatement,
    ProblemSection,
    Procedure,
    Program,
    Repetition,
    ResultSection,
    ReturnStatement,
    Statement,
    StringLiteral,
    TupleExpr,
    UnaryOp,
)
from dubsar.builtins import BUILTINS
from dubsar.errors import (
    DubSarDivisionByZero,
    DubSarInputError,
    DubSarNameError,
    DubSarRangeError,
    DubSarReturnError,
    DubSarUnitError,
)
from dubsar.numbers import Rational, parse_number
from dubsar.semantic import SemanticAnalyzer
from dubsar.units import (
    DIMENSIONLESS,
    Quantity,
    Unit,
    lookup_unit,
    to_quantity,
)


class ReturnSignal(Exception):
    """Internal control-flow signal for procedure return."""

    def __init__(self, values: List[Any]) -> None:
        self.values = values


class Environment:
    """Environment mapping variable names to values."""

    def __init__(self, parent: Optional[Environment] = None, name: str = "tablet") -> None:
        self.parent = parent
        self.name = name
        self.bindings: Dict[str, Any] = {}

    def get(self, name: str) -> Any:
        if name in self.bindings:
            return self.bindings[name]
        if self.parent:
            return self.parent.get(name)
        raise DubSarNameError(f"Undefined quantity or variable: '{name}'")

    def set(self, name: str, value: Any) -> None:
        # If already bound in current environment, update it
        self.bindings[name] = value

    def update(self, name: str, value: Any) -> None:
        if name in self.bindings:
            self.bindings[name] = value
        elif self.parent and self.parent.has(name):
            self.parent.update(name, value)
        else:
            self.bindings[name] = value

    def has(self, name: str) -> bool:
        if name in self.bindings:
            return True
        if self.parent:
            return self.parent.has(name)
        return False


class Interpreter:
    """Tree-walking reference interpreter for DUB.SAR 1.0 tablets."""

    def __init__(
        self,
        input_fn: Optional[Callable[[str], str]] = None,
        output_fn: Optional[Callable[[str], None]] = None,
        source_file: Optional[str] = None,
        format_mode: str = "canonical",
    ) -> None:
        self.source_file = source_file
        self.format_mode = format_mode
        self.input_fn = input_fn if input_fn is not None else input
        self.output_fn = output_fn if output_fn is not None else print
        self.outputs: List[str] = []
        self.procedures: Dict[str, Procedure] = {}
        self.global_env = Environment(name="tablet")
        self.current_env = self.global_env

    def run(self, program: Program) -> List[str]:
        """Executes a DUB.SAR tablet per Section 20."""
        # 1. Initialize standard library
        # 2. Semantic validation pass
        analyzer = SemanticAnalyzer(source_file=self.source_file)
        analyzer.analyze(program)

        # 3. Register all procedures
        for proc in program.procedures:
            self.procedures[proc.name] = proc

        # 4. Execute problem section in source order
        self.current_env = self.global_env
        for stmt in program.problem.body:
            self._exec_statement(stmt)

        # 5. Execute result section
        for stmt in program.result.body:
            self._exec_statement(stmt)

        # 6. Terminate with final observable output
        return self.outputs

    def _write_output(self, text: str) -> None:
        self.outputs.append(text)
        self.output_fn(text)

    # ==========================================================================
    # Statement execution
    # ==========================================================================

    def _exec_statement(self, stmt: Statement) -> None:
        if isinstance(stmt, Declaration):
            val = self._eval_expression(stmt.value)
            # If explicit unit is provided on declaration
            if stmt.unit is not None:
                u = lookup_unit(stmt.unit)
                if isinstance(val, Quantity):
                    val = Quantity(val.value, u)
                else:
                    val = Quantity(val, u)
            elif not isinstance(val, (Quantity, str)):
                val = Quantity(val, DIMENSIONLESS)
            self.current_env.set(stmt.name, val)

        elif isinstance(stmt, Assignment):
            val = self._eval_expression(stmt.value)
            if len(stmt.targets) == 1:
                target = stmt.targets[0]
                # If RHS is a 1-element tuple, unwrap it
                if isinstance(val, (list, tuple)) and len(val) == 1:
                    val = val[0]
                self.current_env.update(target, val)
            else:
                # Tuple unpacking
                if not isinstance(val, (list, tuple)):
                    raise DubSarReturnError(
                        f"Expected {len(stmt.targets)} values to unpack, got single value",
                        line=stmt.line,
                        col=stmt.col,
                        source_file=self.source_file,
                    )
                if len(val) != len(stmt.targets):
                    raise DubSarReturnError(
                        f"Target unpack count mismatch: expected {len(stmt.targets)} values, got {len(val)}",
                        line=stmt.line,
                        col=stmt.col,
                        source_file=self.source_file,
                    )
                for target, item in zip(stmt.targets, val):
                    self.current_env.update(target, item)

        elif isinstance(stmt, Conditional):
            cond_val = self._eval_expression(stmt.condition)
            # Control flow truthiness
            is_true = bool(cond_val)
            if is_true:
                for s in stmt.body:
                    self._exec_statement(s)
            elif stmt.alternative:
                for s in stmt.alternative:
                    self._exec_statement(s)

        elif isinstance(stmt, Repetition):
            # Evaluate bounds
            if stmt.start is not None:
                start_q = to_quantity(self._eval_expression(stmt.start))
                if not start_q.value.is_integer:
                    raise DubSarRangeError(
                        f"Repetition range start must be an integer, got {start_q.value}",
                        line=stmt.line,
                        col=stmt.col,
                        source_file=self.source_file,
                    )
                start_val = int(start_q.value.numerator)
            else:
                start_val = 1

            end_q = to_quantity(self._eval_expression(stmt.end))
            if not end_q.value.is_integer:
                raise DubSarRangeError(
                    f"Repetition range upper bound must be an integer, got {end_q.value}",
                    line=stmt.line,
                    col=stmt.col,
                    source_file=self.source_file,
                )
            end_val = int(end_q.value.numerator)

            if end_val < 0:
                raise DubSarRangeError(
                    f"Repetition upper bound cannot be negative: {end_val}",
                    line=stmt.line,
                    col=stmt.col,
                    source_file=self.source_file,
                )

            # Execute bounded repetition (inclusive of upper bound per §12)
            loop_env = Environment(parent=self.current_env, name="repetition")
            old_env = self.current_env
            self.current_env = loop_env

            try:
                for idx in range(start_val, end_val + 1):
                    self.current_env.set(stmt.target, Quantity(idx, DIMENSIONLESS))
                    for s in stmt.body:
                        self._exec_statement(s)
            finally:
                self.current_env = old_env

        elif isinstance(stmt, ReturnStatement):
            evaled_values = [self._eval_expression(v) for v in stmt.values]
            raise ReturnSignal(evaled_values)

        elif isinstance(stmt, OutputStatement):
            val = self._eval_expression(stmt.value)
            if isinstance(val, str):
                out_str = val
            elif isinstance(val, Quantity):
                out_str = val.format(format_mode=self.format_mode)
            elif isinstance(val, Rational):
                out_str = val.format_canonical()
            else:
                out_str = str(val)
            self._write_output(out_str)

        elif isinstance(stmt, ExpressionStatement):
            self._eval_expression(stmt.expr)

    # ==========================================================================
    # Expression evaluation
    # ==========================================================================

    def _eval_expression(self, expr: Expression) -> Any:
        if isinstance(expr, NumberLiteral):
            u = lookup_unit(expr.unit) if expr.unit else DIMENSIONLESS
            return Quantity(expr.value, u)

        elif isinstance(expr, StringLiteral):
            return expr.value

        elif isinstance(expr, InputExpr):
            prompt = expr.prompt
            raw_input = self.input_fn(prompt).strip()
            try:
                # Check if input string has trailing unit (e.g. "365.2422 𒌓" or "365.2422 day")
                parts = raw_input.split()
                if len(parts) >= 2:
                    num_part = parts[0]
                    unit_part = " ".join(parts[1:])
                    rat = parse_number(num_part)
                    u = lookup_unit(unit_part)
                    return Quantity(rat, u)
                
                # Single part: check if prompt specifies unit (e.g. "in days", "in 𒌓")
                rat = parse_number(raw_input)
                unit_to_use = DIMENSIONLESS
                prompt_lower = prompt.lower()
                if "in days" in prompt_lower or "in day" in prompt_lower or "in 𒌓" in prompt:
                    unit_to_use = lookup_unit("day")
                elif "in hours" in prompt_lower or "in hour" in prompt_lower:
                    unit_to_use = lookup_unit("hour")
                elif "in minutes" in prompt_lower or "in minute" in prompt_lower:
                    unit_to_use = lookup_unit("minute")
                elif "in seconds" in prompt_lower or "in second" in prompt_lower:
                    unit_to_use = lookup_unit("second")
                elif "in months" in prompt_lower or "in month" in prompt_lower or "in 𒌗" in prompt:
                    unit_to_use = lookup_unit("month")
                elif "in years" in prompt_lower or "in year" in prompt_lower or "in 𒈬" in prompt:
                    unit_to_use = lookup_unit("year")

                return Quantity(rat, unit_to_use)
            except Exception as e:
                raise DubSarInputError(
                    f"Invalid numeric input '{raw_input}': {e}",
                    line=expr.line,
                    col=expr.col,
                    source_file=self.source_file,
                )

        elif isinstance(expr, Identifier):
            # Check variable bindings
            if self.current_env.has(expr.name):
                return self.current_env.get(expr.name)
            if expr.name in UNIT_TABLE:
                return Quantity(1, UNIT_TABLE[expr.name])
            raise DubSarNameError(
                f"Undefined quantity or variable: '{expr.name}'",
                line=expr.line,
                col=expr.col,
                source_file=self.source_file,
            )

        elif isinstance(expr, CallExpr):
            return self._eval_call(expr)

        elif isinstance(expr, UnaryOp):
            operand_val = self._eval_expression(expr.operand)
            if expr.op in ("-", "ta", "𒋫"):
                return -to_quantity(operand_val)
            elif expr.op in ("not", "nu", "𒉡"):
                return not bool(operand_val)
            raise DubSarSyntaxError(f"Unknown unary operator: {expr.op}", line=expr.line, col=expr.col)

        elif isinstance(expr, BinaryOp):
            left_val = self._eval_expression(expr.left)
            right_val = self._eval_expression(expr.right)
            return self._eval_binary(expr.op, left_val, right_val, expr.line, expr.col)

        elif isinstance(expr, TupleExpr):
            return [self._eval_expression(e) for e in expr.elements]

        raise DubSarSyntaxError(f"Cannot evaluate expression: {expr}", line=expr.line, col=expr.col)

    def _eval_call(self, call: CallExpr) -> Any:
        # Check builtins first
        if call.callee in BUILTINS:
            func = BUILTINS[call.callee]
            evaled_args = [self._eval_expression(a) for a in call.arguments]
            try:
                return func(*evaled_args)
            except (DubSarUnitError, DubSarDivisionByZero):
                raise
            except Exception as e:
                raise DubSarUnitError(
                    f"Error in builtin '{call.callee}': {e}",
                    line=call.line,
                    col=call.col,
                    source_file=self.source_file,
                )

        # Check declared procedures
        if call.callee in self.procedures:
            proc = self.procedures[call.callee]
            if len(call.arguments) != len(proc.parameters):
                raise DubSarReturnError(
                    f"Procedure '{proc.name}' takes {len(proc.parameters)} arguments, got {len(call.arguments)}",
                    line=call.line,
                    col=call.col,
                    source_file=self.source_file,
                )

            # Evaluate argument expressions in current scope
            evaled_args = [self._eval_expression(a) for a in call.arguments]

            # Bind to new procedure environment
            proc_env = Environment(parent=self.global_env, name=f"proc:{proc.name}")
            for param_name, arg_val in zip(proc.parameters, evaled_args):
                proc_env.set(param_name, arg_val)

            old_env = self.current_env
            self.current_env = proc_env

            try:
                for stmt in proc.body:
                    self._exec_statement(stmt)
                # If execution falls through without returning
                raise DubSarReturnError(
                    f"Procedure '{proc.name}' reached end without returning a result",
                    line=proc.line,
                    col=proc.col,
                    source_file=self.source_file,
                )
            except ReturnSignal as ret:
                ret_vals = ret.values
                if len(ret_vals) == 1:
                    return ret_vals[0]
                return ret_vals
            finally:
                self.current_env = old_env

        raise DubSarNameError(
            f"Call to undefined procedure: '{call.callee}'",
            line=call.line,
            col=call.col,
            source_file=self.source_file,
        )

    def _eval_binary(self, op: str, left: Any, right: Any, line: int, col: int) -> Any:
        # Comparison operators
        if op in ("==", "!=", "<", "<=", ">", ">="):
            ql = to_quantity(left)
            qr = to_quantity(right)
            if op == "==":
                return ql == qr
            elif op == "!=":
                return ql != qr
            elif op == "<":
                return ql < qr
            elif op == "<=":
                return ql <= qr
            elif op == ">":
                return ql > qr
            elif op == ">=":
                return ql >= qr

        # Arithmetic operators
        ql = to_quantity(left)
        qr = to_quantity(right)

        if op in ("+", "zi", "add", "𒍣"):
            return ql + qr
        elif op in ("-", "ta", "sub", "𒋫"):
            return ql - qr
        elif op in ("*", "ša", "sha", "mul", "𒊭"):
            return ql * qr
        elif op in ("/", "ni", "div", "𒉌"):
            return ql / qr
        elif op == "%":
            return ql % qr
        elif op == "**":
            if not qr.value.is_integer:
                raise DubSarUnitError(
                    f"Power exponent must be an integer, got {qr.value}",
                    line=line,
                    col=col,
                    source_file=self.source_file,
                )
            return ql ** int(qr.value.numerator)

        raise DubSarSyntaxError(f"Unknown binary operator: {op}", line=line, col=col)

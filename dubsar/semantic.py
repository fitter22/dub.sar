"""DUB.SAR 1.0 — Semantic Analysis and Validation.

Implements Sections 5, 18, and 19:
- Lexical static scope analysis
- Procedure registration and parameter validation
- Name resolution (raising DubSarNameError for undefined identifiers)
- Range validation (raising DubSarRangeError for invalid repetition bounds)
- Return validation in procedures
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set

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
from dubsar.errors import DubSarNameError, DubSarRangeError, DubSarReturnError, DubSarSyntaxError
from dubsar.units import UNIT_TABLE


class Scope:
    """Lexical scope holding established names."""

    def __init__(self, parent: Optional[Scope] = None, name: str = "tablet") -> None:
        self.parent = parent
        self.name = name
        self.symbols: Set[str] = set()

    def define(self, name: str) -> None:
        self.symbols.add(name)

    def is_defined(self, name: str) -> bool:
        if name in self.symbols:
            return True
        if self.parent:
            return self.parent.is_defined(name)
        return False


class SemanticAnalyzer:
    """Validates tablet structure, scopes, and name bindings."""

    def __init__(self, source_file: Optional[str] = None) -> None:
        self.source_file = source_file
        self.procedures: Dict[str, Procedure] = {}
        self.global_scope = Scope(name="tablet")
        self.current_scope = self.global_scope
        self.in_procedure = False
        self.current_proc_name: Optional[str] = None

    def analyze(self, program: Program) -> None:
        """Runs the full semantic validation pass on a tablet."""
        # 1. Register all procedures first (§5, §20)
        for proc in program.procedures:
            if proc.name in self.procedures:
                raise DubSarSyntaxError(
                    f"Duplicate procedure declaration: '{proc.name}'",
                    line=proc.line,
                    col=proc.col,
                    source_file=self.source_file,
                )
            if proc.name in BUILTINS:
                raise DubSarSyntaxError(
                    f"Cannot redefine built-in mathematical procedure: '{proc.name}'",
                    line=proc.line,
                    col=proc.col,
                    source_file=self.source_file,
                )
            self.procedures[proc.name] = proc

        # 2. Validate procedures bodies
        for proc in program.procedures:
            self._analyze_procedure(proc)

        # 3. Validate problem section
        self.current_scope = self.global_scope
        self.in_procedure = False
        for stmt in program.problem.body:
            self._analyze_statement(stmt)

        # 4. Validate result section (shares tablet scope with problem section)
        for stmt in program.result.body:
            self._analyze_statement(stmt)

    def _analyze_procedure(self, proc: Procedure) -> None:
        # Check parameter uniqueness
        seen_params: Set[str] = set()
        for p in proc.parameters:
            if p in seen_params:
                raise DubSarSyntaxError(
                    f"Duplicate parameter '{p}' in procedure '{proc.name}'",
                    line=proc.line,
                    col=proc.col,
                    source_file=self.source_file,
                )
            seen_params.add(p)

        # Create procedure local scope (parameters shadow outer scopes, §18)
        proc_scope = Scope(parent=self.global_scope, name=f"proc:{proc.name}")
        for p in proc.parameters:
            proc_scope.define(p)

        old_scope = self.current_scope
        old_proc = self.current_proc_name
        self.current_scope = proc_scope
        self.in_procedure = True
        self.current_proc_name = proc.name

        try:
            has_return = False
            for stmt in proc.body:
                if self._statement_has_return(stmt):
                    has_return = True
                self._analyze_statement(stmt)

            if not has_return:
                raise DubSarReturnError(
                    f"Procedure '{proc.name}' does not contain any return ('𒄑' / 'return') statement",
                    line=proc.line,
                    col=proc.col,
                    source_file=self.source_file,
                )
        finally:
            self.current_scope = old_scope
            self.in_procedure = False
            self.current_proc_name = old_proc

    def _statement_has_return(self, stmt: Statement) -> bool:
        if isinstance(stmt, ReturnStatement):
            return True
        if isinstance(stmt, Conditional):
            in_body = any(self._statement_has_return(s) for s in stmt.body)
            in_alt = (
                any(self._statement_has_return(s) for s in stmt.alternative)
                if stmt.alternative
                else False
            )
            return in_body or in_alt
        if isinstance(stmt, Repetition):
            return any(self._statement_has_return(s) for s in stmt.body)
        return False

    def _analyze_statement(self, stmt: Statement) -> None:
        if isinstance(stmt, Declaration):
            self._analyze_expression(stmt.value)
            self.current_scope.define(stmt.name)

        elif isinstance(stmt, Assignment):
            self._analyze_expression(stmt.value)
            for target in stmt.targets:
                self.current_scope.define(target)

        elif isinstance(stmt, Conditional):
            self._analyze_expression(stmt.condition)
            for s in stmt.body:
                self._analyze_statement(s)
            if stmt.alternative:
                for s in stmt.alternative:
                    self._analyze_statement(s)

        elif isinstance(stmt, Repetition):
            # Section 12: Range checking
            if stmt.start:
                self._analyze_expression(stmt.start)
            self._analyze_expression(stmt.end)

            # Check statically negative bound if literal or negative unary literal
            if isinstance(stmt.end, NumberLiteral) and stmt.end.value < 0:
                raise DubSarRangeError(
                    f"Repetition upper bound cannot be negative: {stmt.end.value}",
                    line=stmt.line,
                    col=stmt.col,
                    source_file=self.source_file,
                )
            if isinstance(stmt.end, UnaryOp) and stmt.end.op in ("-", "ta", "𒋫") and isinstance(stmt.end.operand, NumberLiteral):
                raise DubSarRangeError(
                    f"Repetition upper bound cannot be negative: -{stmt.end.operand.value}",
                    line=stmt.line,
                    col=stmt.col,
                    source_file=self.source_file,
                )

            # Target loop variable is defined in loop scope
            loop_scope = Scope(parent=self.current_scope, name="repetition")
            loop_scope.define(stmt.target)
            old_scope = self.current_scope
            self.current_scope = loop_scope
            try:
                for s in stmt.body:
                    self._analyze_statement(s)
            finally:
                self.current_scope = old_scope

        elif isinstance(stmt, ReturnStatement):
            if not self.in_procedure:
                raise DubSarSyntaxError(
                    "Return statement ('𒄑' / 'return') cannot be used outside a procedure",
                    line=stmt.line,
                    col=stmt.col,
                    source_file=self.source_file,
                )
            for v in stmt.values:
                self._analyze_expression(v)

        elif isinstance(stmt, OutputStatement):
            self._analyze_expression(stmt.value)

        elif isinstance(stmt, ExpressionStatement):
            self._analyze_expression(stmt.expr)

    def _analyze_expression(self, expr: Expression) -> None:
        if isinstance(expr, NumberLiteral):
            return

        elif isinstance(expr, StringLiteral):
            return

        elif isinstance(expr, InputExpr):
            return

        elif isinstance(expr, Identifier):
            # Check if defined in scope or known unit/builtin
            if not self.current_scope.is_defined(expr.name):
                # Is it a unit name or builtin?
                if expr.name not in BUILTINS and expr.name not in UNIT_TABLE:
                    raise DubSarNameError(
                        f"Undefined quantity or variable: '{expr.name}'",
                        line=expr.line,
                        col=expr.col,
                        source_file=self.source_file,
                    )

        elif isinstance(expr, CallExpr):
            # Check if procedure or builtin exists
            if expr.callee not in self.procedures and expr.callee not in BUILTINS:
                raise DubSarNameError(
                    f"Call to undefined procedure: '{expr.callee}'",
                    line=expr.line,
                    col=expr.col,
                    source_file=self.source_file,
                )
            for arg in expr.arguments:
                self._analyze_expression(arg)

        elif isinstance(expr, UnaryOp):
            self._analyze_expression(expr.operand)

        elif isinstance(expr, BinaryOp):
            self._analyze_expression(expr.left)
            self._analyze_expression(expr.right)

        elif isinstance(expr, TupleExpr):
            for e in expr.elements:
                self._analyze_expression(e)

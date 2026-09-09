"""DUB.SAR 1.0 — Semantic Analysis and Validation.

Implements Sections 5, 18, 19, 20:
- Lexical static scope analysis
- Static compile-time unit type inference and dimensional checking (CR-003)
- Procedure registration, parameter validation, and call arity checking (CR-020, CR-021)
- Definite return path and return arity consistency verification (CR-022)
- Name resolution (raising DubSarNameError for undefined identifiers)
- Range validation (raising DubSarRangeError for invalid repetition bounds)
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set

from dubsar.ast import (
    Assignment,
    BinaryOp,
    CallExpr,
    ApplyRecipe,
    CompareExpr,
    Conditional,
    Declaration,
    Determination,
    DomainRepetition,
    EmptyLiteral,
    Expression,
    ExpressionStatement,
    FieldAccess,
    Identifier,
    InputExpr,
    IsExpr,
    NumberLiteral,
    OutputStatement,
    PostfixExpr,
    ProblemSection,
    Procedure,
    Program,
    Recipe,
    Repetition,
    ResultSection,
    RetainStatement,
    ReturnStatement,
    Statement,
    StringLiteral,
    TupleExpr,
    UnaryOp,
    ConsultTablet,
    CreateWorkingTablet,
    CopyTablet,
    DeriveTablet,
    InscribeTablet,
    PutEntry,
    ReplaceEntry,
    RemoveEntry,
    TakeEntry,
    SeekEntry,
    TabletHistory,
)
from dubsar.builtins import BUILTINS
from dubsar.errors import (
    DubSarNameError,
    DubSarRangeError,
    DubSarReturnError,
    DubSarSyntaxError,
    DubSarTypeError,
    DubSarUnitError,
)
from dubsar.units import DIMENSIONLESS, UNIT_TABLE, Unit, lookup_unit


class Scope:
    """Lexical scope holding established names and static unit types."""

    def __init__(self, parent: Optional[Scope] = None, name: str = "tablet") -> None:
        self.parent = parent
        self.name = name
        self.symbols: Dict[str, Optional[Unit]] = {}

    def define(self, name: str, unit: Optional[Unit] = None) -> None:
        self.symbols[name] = unit

    def is_defined(self, name: str) -> bool:
        if name in self.symbols:
            return True
        if self.parent:
            return self.parent.is_defined(name)
        return False

    def get_unit(self, name: str) -> Optional[Unit]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.get_unit(name)
        return None


class SemanticAnalyzer:
    """Validates tablet structure, scopes, name bindings, and dimensional types."""

    def __init__(self, source_file: Optional[str] = None) -> None:
        self.source_file = source_file
        self.procedures: Dict[str, Procedure] = {}
        self.procedure_return_arities: Dict[str, int] = {}
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
            proc_scope.define(p, None)

        old_scope = self.current_scope
        old_proc = self.current_proc_name
        self.current_scope = proc_scope
        self.in_procedure = True
        self.current_proc_name = proc.name

        try:
            return_arities: List[int] = []
            has_return = False
            for stmt in proc.body:
                self._collect_return_arities(stmt, return_arities)
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

            # Check return arity consistency
            if return_arities:
                first_arity = return_arities[0]
                for arity in return_arities[1:]:
                    if arity != first_arity:
                        raise DubSarReturnError(
                            f"Procedure '{proc.name}' has inconsistent return arities: {first_arity} vs {arity}",
                            line=proc.line,
                            col=proc.col,
                            source_file=self.source_file,
                        )
                self.procedure_return_arities[proc.name] = first_arity
        finally:
            self.current_scope = old_scope
            self.in_procedure = False
            self.current_proc_name = old_proc

    def _collect_return_arities(self, stmt: Statement, arities: List[int]) -> None:
        if isinstance(stmt, ReturnStatement):
            arities.append(len(stmt.values))
        elif isinstance(stmt, Conditional):
            for s in stmt.body:
                self._collect_return_arities(s, arities)
            if stmt.alternative:
                for s in stmt.alternative:
                    self._collect_return_arities(s, arities)
        elif isinstance(stmt, Repetition):
            for s in stmt.body:
                self._collect_return_arities(s, arities)

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
            val_u = self._analyze_expression(stmt.value)
            declared_u = lookup_unit(stmt.unit) if stmt.unit else None
            if declared_u and val_u and not declared_u.is_compatible_with(val_u):
                raise DubSarUnitError(
                    f"Declared unit '{declared_u}' is incompatible with value unit '{val_u}'",
                    line=stmt.line,
                    col=stmt.col,
                    source_file=self.source_file,
                )
            unit = declared_u or val_u
            self.current_scope.define(stmt.name, unit)

        elif isinstance(stmt, Assignment):
            val_u = self._analyze_expression(stmt.value)
            if len(stmt.targets) == 1:
                self.current_scope.define(stmt.targets[0], val_u)
            else:
                for target in stmt.targets:
                    self.current_scope.define(target, None)

        elif isinstance(stmt, Conditional):
            self._analyze_expression(stmt.condition)
            for s in stmt.body:
                self._analyze_statement(s)
            if stmt.alternative:
                for s in stmt.alternative:
                    self._analyze_statement(s)

        elif isinstance(stmt, Repetition):
            if stmt.start:
                self._analyze_expression(stmt.start)
            self._analyze_expression(stmt.end)

            # Check statically negative bound
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

            loop_scope = Scope(parent=self.current_scope, name="repetition")
            loop_scope.define(stmt.target, DIMENSIONLESS)
            old_scope = self.current_scope
            self.current_scope = loop_scope
            try:
                for s in stmt.body:
                    self._analyze_statement(s)
            finally:
                self.current_scope = old_scope

        elif isinstance(stmt, DomainRepetition):
            self._analyze_expression(stmt.start)
            self._analyze_expression(stmt.end)
            loop_scope = Scope(parent=self.current_scope, name="domain")
            loop_scope.define(stmt.target, DIMENSIONLESS)
            old_scope = self.current_scope
            self.current_scope = loop_scope
            try:
                for s in stmt.body:
                    self._analyze_statement(s)
            finally:
                self.current_scope = old_scope

        elif isinstance(stmt, Determination):
            for f in stmt.fields:
                if not self.current_scope.is_defined(f):
                    raise DubSarNameError(
                        f"Field '{f}' in determination '{stmt.name}' is not established",
                        line=stmt.line,
                        col=stmt.col,
                        source_file=self.source_file,
                    )
            self.current_scope.define(stmt.name, None)

        elif isinstance(stmt, RetainStatement):
            if not self.current_scope.is_defined(stmt.candidate):
                raise DubSarNameError(
                    f"Candidate '{stmt.candidate}' in retain statement is not established",
                    line=stmt.line,
                    col=stmt.col,
                    source_file=self.source_file,
                )
            self._analyze_expression(stmt.condition)
            self.current_scope.define(stmt.target, None)

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

        elif isinstance(stmt, ConsultTablet):
            self._analyze_expression(stmt.tablet_name)
            if stmt.version:
                self._analyze_expression(stmt.version)
            if stmt.alias:
                self.current_scope.define(stmt.alias, None)
            elif isinstance(stmt.tablet_name, StringLiteral):
                self.current_scope.define(stmt.tablet_name.value, None)
            elif isinstance(stmt.tablet_name, Identifier):
                self.current_scope.define(stmt.tablet_name.name, None)

        elif isinstance(stmt, CreateWorkingTablet):
            self.current_scope.define(stmt.name, None)

        elif isinstance(stmt, CopyTablet):
            if stmt.source:
                self._analyze_expression(stmt.source)
            if stmt.version:
                self._analyze_expression(stmt.version)
            self.current_scope.define(stmt.target, None)

        elif isinstance(stmt, DeriveTablet):
            if stmt.source:
                self._analyze_expression(stmt.source)
            if stmt.version:
                self._analyze_expression(stmt.version)
            self.current_scope.define(stmt.target, None)

        elif isinstance(stmt, InscribeTablet):
            if not self.current_scope.is_defined(stmt.working_name):
                raise DubSarNameError(
                    f"Working tablet '{stmt.working_name}' is not established",
                    line=stmt.line,
                    col=stmt.col,
                    source_file=self.source_file,
                )
            self._analyze_expression(stmt.target_name)

        elif isinstance(stmt, PutEntry):
            if not self.current_scope.is_defined(stmt.working_name):
                raise DubSarNameError(
                    f"Working tablet '{stmt.working_name}' is not established",
                    line=stmt.line,
                    col=stmt.col,
                    source_file=self.source_file,
                )
            self._analyze_expression(stmt.value)
            self._analyze_expression(stmt.key)

        elif isinstance(stmt, ReplaceEntry):
            if not self.current_scope.is_defined(stmt.working_name):
                raise DubSarNameError(
                    f"Working tablet '{stmt.working_name}' is not established",
                    line=stmt.line,
                    col=stmt.col,
                    source_file=self.source_file,
                )
            self._analyze_expression(stmt.key)
            self._analyze_expression(stmt.value)

        elif isinstance(stmt, RemoveEntry):
            if not self.current_scope.is_defined(stmt.working_name):
                raise DubSarNameError(
                    f"Working tablet '{stmt.working_name}' is not established",
                    line=stmt.line,
                    col=stmt.col,
                    source_file=self.source_file,
                )
            self._analyze_expression(stmt.key)

    def _analyze_expression(self, expr: Expression) -> Optional[Unit]:
        """Analyzes an expression and returns its statically inferred unit if known."""
        if isinstance(expr, NumberLiteral):
            if expr.unit:
                return lookup_unit(expr.unit)
            return DIMENSIONLESS

        elif isinstance(expr, StringLiteral):
            return None

        elif isinstance(expr, InputExpr):
            return None

        elif isinstance(expr, Identifier):
            if self.current_scope.is_defined(expr.name):
                return self.current_scope.get_unit(expr.name)

            if expr.name in UNIT_TABLE:
                return lookup_unit(expr.name)

            if expr.name not in BUILTINS:
                raise DubSarNameError(
                    f"Undefined quantity or variable: '{expr.name}'",
                    line=expr.line,
                    col=expr.col,
                    source_file=self.source_file,
                )
            return None

        elif isinstance(expr, CallExpr):
            if expr.callee not in self.procedures and expr.callee not in BUILTINS:
                raise DubSarNameError(
                    f"Call to undefined procedure: '{expr.callee}'",
                    line=expr.line,
                    col=expr.col,
                    source_file=self.source_file,
                )

            # Check procedure call argument count
            if expr.callee in self.procedures:
                proc = self.procedures[expr.callee]
                if len(expr.arguments) != len(proc.parameters):
                    raise DubSarSyntaxError(
                        f"Procedure '{expr.callee}' expects {len(proc.parameters)} arguments, got {len(expr.arguments)}",
                        line=expr.line,
                        col=expr.col,
                        source_file=self.source_file,
                    )

            arg_units = [self._analyze_expression(arg) for arg in expr.arguments]

            if expr.callee in ("abs", "floor", "ceil"):
                return arg_units[0] if arg_units else None

            if expr.callee == "nearest":
                # Returns dimensionless count per Section 14.1
                return DIMENSIONLESS

            if expr.callee in ("min", "max"):
                if len(arg_units) >= 2 and arg_units[0] is not None and arg_units[1] is not None:
                    if not arg_units[0].is_compatible_with(arg_units[1]):
                        raise DubSarUnitError(
                            f"Cannot compute {expr.callee} of incompatible units: '{arg_units[0]}' and '{arg_units[1]}'",
                            line=expr.line,
                            col=expr.col,
                            source_file=self.source_file,
                        )
                return arg_units[0] if arg_units else None

            if expr.callee in ("gcd", "lcm"):
                return DIMENSIONLESS

            if expr.callee == "convert":
                if len(expr.arguments) >= 2:
                    val_u = arg_units[0]
                    target_arg = expr.arguments[1]
                    if isinstance(target_arg, Identifier):
                        target_u = lookup_unit(target_arg.name)
                        if val_u is not None and not val_u.is_compatible_with(target_u):
                            raise DubSarUnitError(
                                f"Cannot convert between incompatible dimensions: '{val_u}' to '{target_u}'",
                                line=expr.line,
                                col=expr.col,
                                source_file=self.source_file,
                            )
                        return target_u
                return None

            return None

        elif isinstance(expr, UnaryOp):
            u = self._analyze_expression(expr.operand)
            if expr.op in ("not", "nu", "𒉡"):
                return DIMENSIONLESS
            return u

        elif isinstance(expr, BinaryOp):
            left_u = self._analyze_expression(expr.left)
            right_u = self._analyze_expression(expr.right)

            if expr.op in ("+", "-", "zi", "ta", "𒍣", "𒋫"):
                if left_u is not None and right_u is not None:
                    if not left_u.is_compatible_with(right_u):
                        raise DubSarUnitError(
                            f"Cannot perform '{expr.op}' between incompatible units: '{left_u}' and '{right_u}'",
                            line=expr.line,
                            col=expr.col,
                            source_file=self.source_file,
                        )
                    return left_u
                return left_u or right_u

            elif expr.op in ("*", "ša", "sha", "𒊭"):
                if left_u is not None and right_u is not None:
                    return left_u * right_u
                return None

            elif expr.op in ("/", "ni", "𒉌"):
                if left_u is not None and right_u is not None:
                    return left_u / right_u
                return None

            elif expr.op == "%":
                if left_u is not None and right_u is not None:
                    if not left_u.is_compatible_with(right_u):
                        raise DubSarUnitError(
                            f"Cannot perform modulo between incompatible units: '{left_u}' and '{right_u}'",
                            line=expr.line,
                            col=expr.col,
                            source_file=self.source_file,
                        )
                    return left_u
                return left_u or right_u

            elif expr.op in ("==", "!=", "<", "<=", ">", ">="):
                if left_u is not None and right_u is not None:
                    if not left_u.is_compatible_with(right_u):
                        raise DubSarUnitError(
                            f"Cannot compare incompatible units: '{left_u}' and '{right_u}'",
                            line=expr.line,
                            col=expr.col,
                            source_file=self.source_file,
                        )
                return DIMENSIONLESS

            elif expr.op == "**":
                return left_u

            return None

        elif isinstance(expr, TupleExpr):
            for e in expr.elements:
                self._analyze_expression(e)
            return None

        elif isinstance(expr, EmptyLiteral):
            return None

        elif isinstance(expr, FieldAccess):
            self._analyze_expression(expr.record)
            return None

        elif isinstance(expr, PostfixExpr):
            unit_stack: List[Optional[Unit]] = []
            for step in expr.steps:
                if isinstance(step, Expression):
                    u = self._analyze_expression(step)
                    unit_stack.append(u)
                elif isinstance(step, ApplyRecipe):
                    if step.recipe not in self.procedures and step.recipe not in BUILTINS:
                        raise DubSarNameError(
                            f"Undefined recipe: '{step.recipe}'",
                            line=step.line,
                            col=step.col,
                            source_file=self.source_file,
                        )
                    if step.recipe in self.procedures:
                        argc = len(self.procedures[step.recipe].parameters)
                    elif step.recipe in BUILTINS:
                        import inspect
                        argc = len(inspect.signature(BUILTINS[step.recipe]).parameters)
                    else:
                        argc = 0
                    for _ in range(min(argc, len(unit_stack))):
                        unit_stack.pop()
                    unit_stack.append(None)
                elif isinstance(step, str):
                    if step in ("+", "-", "zi", "ta", "𒍣", "𒋫", "add", "subtract"):
                        right_u = unit_stack.pop() if unit_stack else None
                        left_u = unit_stack.pop() if unit_stack else None
                        if left_u is not None and right_u is not None:
                            if not left_u.is_compatible_with(right_u):
                                raise DubSarUnitError(
                                    f"Cannot perform '{step}' between incompatible units: '{left_u}' and '{right_u}'",
                                    line=expr.line,
                                    col=expr.col,
                                    source_file=self.source_file,
                                )
                            unit_stack.append(left_u)
                        else:
                            unit_stack.append(left_u or right_u)
                    elif step in ("*", "ša", "sha", "𒊭", "multiply"):
                        right_u = unit_stack.pop() if unit_stack else None
                        left_u = unit_stack.pop() if unit_stack else None
                        if left_u is not None and right_u is not None:
                            unit_stack.append(left_u * right_u)
                        else:
                            unit_stack.append(None)
                    elif step in ("/", "ni", "𒉌", "divide"):
                        right_u = unit_stack.pop() if unit_stack else None
                        left_u = unit_stack.pop() if unit_stack else None
                        if left_u is not None and right_u is not None:
                            unit_stack.append(left_u / right_u)
                        else:
                            unit_stack.append(None)
                    elif step in ("floor", "ceil", "nearest", "absolute", "abs", "gur", "nim", "ri", "te", "𒄥", "𒉏", "𒊑", "𒋼"):
                        pass
                    elif step == "take":
                        unit_stack.pop() if unit_stack else None
                        unit_stack.pop() if unit_stack else None
                        unit_stack.append(None)
                    elif step in ("<", "<=", ">", ">=", "==", "!=", "lesser", "greater", "equal", "not-equal"):
                        right_u = unit_stack.pop() if unit_stack else None
                        left_u = unit_stack.pop() if unit_stack else None
                        if left_u is not None and right_u is not None and not left_u.is_compatible_with(right_u):
                            raise DubSarUnitError(
                                f"Cannot compare incompatible units: '{left_u}' and '{right_u}'",
                                line=expr.line,
                                col=expr.col,
                                source_file=self.source_file,
                            )
                        unit_stack.append(DIMENSIONLESS)
            return unit_stack[-1] if unit_stack else None

        elif isinstance(expr, CompareExpr):
            self._analyze_expression(expr.left)
            if expr.right:
                self._analyze_expression(expr.right)
            return DIMENSIONLESS

        elif isinstance(expr, IsExpr):
            self._analyze_expression(expr.target)
            return DIMENSIONLESS

        elif isinstance(expr, TakeEntry):
            self._analyze_expression(expr.tablet)
            self._analyze_expression(expr.key)
            return None

        elif isinstance(expr, SeekEntry):
            self._analyze_expression(expr.tablet)
            self._analyze_expression(expr.target)
            return None

        elif isinstance(expr, TabletHistory):
            self._analyze_expression(expr.tablet)
            return None

        return None


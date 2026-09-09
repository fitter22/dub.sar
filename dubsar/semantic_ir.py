"""DUB.SAR 1.0 — High-Level Mathematical Semantic IR.

Implements CR-011 and CR-024:
- Explicit semantic intermediate representation based on mathematical verbs:
    ESTABLISH, TAKE, ADD, SUBTRACT, MULTIPLY, DIVIDE, COMPARE, REPEAT, DETERMINE, INSCRIBE
- Bridges typed Mathematical AST and Stack-based Machine IR
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional, Union

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
    Procedure,
    Program,
    Repetition,
    ReturnStatement,
    Statement,
    StringLiteral,
    TupleExpr,
    UnaryOp,
)
from dubsar.numbers import Rational


# ==============================================================================
# Semantic Verb Expressions
# ==============================================================================

@dataclass
class VerbExpr:
    """Base class for expressions within the semantic IR."""
    line: int = 0
    col: int = 0


@dataclass
class TakeLiteral(VerbExpr):
    """TAKE literal number quantity: value [unit]."""
    value: Rational = field(default_factory=lambda: Rational(0))
    unit: Optional[str] = None


@dataclass
class TakeText(VerbExpr):
    """TAKE text literal."""
    value: str = ""


@dataclass
class TakeQuantity(VerbExpr):
    """TAKE established quantity by name."""
    name: str = ""


@dataclass
class ReceiveInput(VerbExpr):
    """RECEIVE input quantity from user/environment."""
    prompt: str = ""


@dataclass
class ApplyMathVerb(VerbExpr):
    """Apply a core mathematical verb: ADD, SUBTRACT, MULTIPLY, DIVIDE, etc."""
    verb: str = ""  # 'ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', 'MODULO', 'POWER', 'NEGATE', 'NOT', 'COMPARE', 'INVOKE'
    operands: List[VerbExpr] = field(default_factory=list)
    relation: Optional[str] = None  # for COMPARE: '==', '<', etc.
    callee: Optional[str] = None    # for INVOKE: procedure or builtin name


@dataclass
class TuplePack(VerbExpr):
    """Pack ordered tuple of values."""
    elements: List[VerbExpr] = field(default_factory=list)


# ==============================================================================
# Semantic Mathematical Verbs (Prescriptions / Statements)
# ==============================================================================

@dataclass
class SemanticVerb:
    """Base class for all mathematical verbs."""
    line: int = 0
    col: int = 0


@dataclass
class EstablishVerb(SemanticVerb):
    """ESTABLISH: Initial establishment of a named quantity: name : value [unit]."""
    name: str = ""
    value: VerbExpr = field(default_factory=VerbExpr)
    unit: Optional[str] = None


@dataclass
class AssignVerb(SemanticVerb):
    """ASSIGN: Calculation and binding of derived quantities: targets := value."""
    targets: List[str] = field(default_factory=list)
    value: VerbExpr = field(default_factory=VerbExpr)


@dataclass
class DetermineVerb(SemanticVerb):
    """DETERMINE: Conditional branch governed by a mathematical predicate."""
    condition: VerbExpr = field(default_factory=VerbExpr)
    body: List[SemanticVerb] = field(default_factory=list)
    alternative: Optional[List[SemanticVerb]] = None


@dataclass
class RepeatVerb(SemanticVerb):
    """REPEAT: Bounded mathematical repetition over a finite range."""
    target: str = ""
    start: Optional[VerbExpr] = None
    end: VerbExpr = field(default_factory=VerbExpr)
    body: List[SemanticVerb] = field(default_factory=list)


@dataclass
class ConcludeVerb(SemanticVerb):
    """CONCLUDE: Produce final result(s) from a mathematical recipe."""
    values: List[VerbExpr] = field(default_factory=list)


@dataclass
class InscribeVerb(SemanticVerb):
    """INSCRIBE: Output/inscribe a calculated result onto the tablet."""
    value: VerbExpr = field(default_factory=VerbExpr)


@dataclass
class DiscardVerb(SemanticVerb):
    """Evaluate expression verb for side-effects (e.g. standalone invocation)."""
    expr: VerbExpr = field(default_factory=VerbExpr)


# ==============================================================================
# Procedures and Program Structure
# ==============================================================================

@dataclass
class ProcedureRecipe:
    """A reusable mathematical procedure recipe."""
    name: str = ""
    parameters: List[str] = field(default_factory=list)
    body: List[SemanticVerb] = field(default_factory=list)
    line: int = 0
    col: int = 0


@dataclass
class SemanticProgram:
    """Complete semantic IR representation of a DUB.SAR tablet."""
    problem_verbs: List[SemanticVerb] = field(default_factory=list)
    procedures: List[ProcedureRecipe] = field(default_factory=list)
    result_verbs: List[SemanticVerb] = field(default_factory=list)
    line: int = 0
    col: int = 0


# ==============================================================================
# AST -> Semantic IR Lowering
# ==============================================================================

def lower_expression_to_sem_ir(expr: Expression) -> VerbExpr:
    """Lowers an AST expression into a Semantic IR VerbExpr."""
    if isinstance(expr, NumberLiteral):
        return TakeLiteral(value=expr.value, unit=expr.unit, line=expr.line, col=expr.col)
    elif isinstance(expr, StringLiteral):
        return TakeText(value=expr.value, line=expr.line, col=expr.col)
    elif isinstance(expr, Identifier):
        return TakeQuantity(name=expr.name, line=expr.line, col=expr.col)
    elif isinstance(expr, InputExpr):
        return ReceiveInput(prompt=expr.prompt, line=expr.line, col=expr.col)
    elif isinstance(expr, UnaryOp):
        operand_ir = lower_expression_to_sem_ir(expr.operand)
        if expr.op in ("not", "nu", "𒉡"):
            return ApplyMathVerb(verb="NOT", operands=[operand_ir], line=expr.line, col=expr.col)
        else:
            return ApplyMathVerb(verb="NEGATE", operands=[operand_ir], line=expr.line, col=expr.col)
    elif isinstance(expr, BinaryOp):
        left_ir = lower_expression_to_sem_ir(expr.left)
        right_ir = lower_expression_to_sem_ir(expr.right)
        op_map = {
            "+": "ADD", "zi": "ADD", "𒍣": "ADD",
            "-": "SUBTRACT", "ta": "SUBTRACT", "𒋫": "SUBTRACT",
            "*": "MULTIPLY", "ša": "MULTIPLY", "sha": "MULTIPLY", "𒊭": "MULTIPLY",
            "/": "DIVIDE", "ni": "DIVIDE", "𒉌": "DIVIDE",
            "%": "MODULO",
            "**": "POWER",
        }
        if expr.op in op_map:
            return ApplyMathVerb(verb=op_map[expr.op], operands=[left_ir, right_ir], line=expr.line, col=expr.col)
        elif expr.op in ("==", "!=", "<", "<=", ">", ">="):
            return ApplyMathVerb(
                verb="COMPARE",
                operands=[left_ir, right_ir],
                relation=expr.op,
                line=expr.line,
                col=expr.col,
            )
        else:
            return ApplyMathVerb(verb=expr.op.upper(), operands=[left_ir, right_ir], line=expr.line, col=expr.col)
    elif isinstance(expr, CallExpr):
        arg_irs = [lower_expression_to_sem_ir(a) for a in expr.arguments]
        return ApplyMathVerb(verb="INVOKE", operands=arg_irs, callee=expr.callee, line=expr.line, col=expr.col)
    elif isinstance(expr, TupleExpr):
        el_irs = [lower_expression_to_sem_ir(e) for e in expr.elements]
        return TuplePack(elements=el_irs, line=expr.line, col=expr.col)
    return VerbExpr(line=expr.line, col=expr.col)


def lower_statement_to_sem_ir(stmt: Statement) -> SemanticVerb:
    """Lowers an AST statement into a Semantic IR verb."""
    if isinstance(stmt, Declaration):
        return EstablishVerb(
            name=stmt.name,
            value=lower_expression_to_sem_ir(stmt.value),
            unit=stmt.unit,
            line=stmt.line,
            col=stmt.col,
        )
    elif isinstance(stmt, Assignment):
        return AssignVerb(
            targets=list(stmt.targets),
            value=lower_expression_to_sem_ir(stmt.value),
            line=stmt.line,
            col=stmt.col,
        )
    elif isinstance(stmt, Conditional):
        return DetermineVerb(
            condition=lower_expression_to_sem_ir(stmt.condition),
            body=[lower_statement_to_sem_ir(s) for s in stmt.body],
            alternative=[lower_statement_to_sem_ir(s) for s in stmt.alternative] if stmt.alternative else None,
            line=stmt.line,
            col=stmt.col,
        )
    elif isinstance(stmt, Repetition):
        return RepeatVerb(
            target=stmt.target,
            start=lower_expression_to_sem_ir(stmt.start) if stmt.start else None,
            end=lower_expression_to_sem_ir(stmt.end),
            body=[lower_statement_to_sem_ir(s) for s in stmt.body],
            line=stmt.line,
            col=stmt.col,
        )
    elif isinstance(stmt, ReturnStatement):
        return ConcludeVerb(
            values=[lower_expression_to_sem_ir(v) for v in stmt.values],
            line=stmt.line,
            col=stmt.col,
        )
    elif isinstance(stmt, OutputStatement):
        return InscribeVerb(
            value=lower_expression_to_sem_ir(stmt.value),
            line=stmt.line,
            col=stmt.col,
        )
    elif isinstance(stmt, ExpressionStatement):
        return DiscardVerb(
            expr=lower_expression_to_sem_ir(stmt.expr),
            line=stmt.line,
            col=stmt.col,
        )
    return SemanticVerb(line=stmt.line, col=stmt.col)


def ast_to_semantic_ir(program: Program) -> SemanticProgram:
    """Translates the complete AST Program into DUB.SAR Semantic IR."""
    procedures = [
        ProcedureRecipe(
            name=p.name,
            parameters=list(p.parameters),
            body=[lower_statement_to_sem_ir(s) for s in p.body],
            line=p.line,
            col=p.col,
        )
        for p in program.procedures
    ]
    problem_verbs = [lower_statement_to_sem_ir(s) for s in program.problem.body]
    result_verbs = [lower_statement_to_sem_ir(s) for s in program.result.body]

    return SemanticProgram(
        problem_verbs=problem_verbs,
        procedures=procedures,
        result_verbs=result_verbs,
        line=program.line,
        col=program.col,
    )

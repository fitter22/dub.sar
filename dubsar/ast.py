"""DUB.SAR 1.0 — Abstract Syntax Tree (AST).

Implements Section 5 and Section 6:
- Tablet model: Problem section, Procedures, Result section
- Prescriptions: Declarations, Assignments (including tuple unpack), Conditionals, Repetitions
- Mathematical expressions with exact numbers, units, and operators
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

from dubsar.numbers import Rational


@dataclass
class ASTNode:
    """Base class for all AST nodes with source coordinates."""
    line: int = 0
    col: int = 0


# ==============================================================================
# Expressions
# ==============================================================================

@dataclass
class Expression(ASTNode):
    """Base class for expressions."""
    pass


@dataclass
class NumberLiteral(Expression):
    """A numeric literal (integer, sexagesimal, decimal, cuneiform), with optional unit."""
    value: Rational = field(default_factory=lambda: Rational(0))
    unit: Optional[str] = None


@dataclass
class StringLiteral(Expression):
    """A string literal."""
    value: str = ""


@dataclass
class Identifier(Expression):
    """A named reference (quantity or variable)."""
    name: str = ""


@dataclass
class InputExpr(Expression):
    """An input prescription: a-diš(prompt) / 𒀀𒁹(prompt)."""
    prompt: str = ""


@dataclass
class CallExpr(Expression):
    """A procedure call: name(arg1, arg2, ...)."""
    callee: str = ""
    arguments: List[Expression] = field(default_factory=list)


@dataclass
class UnaryOp(Expression):
    """Unary operation: - /  nu (negation / not)."""
    op: str = ""
    operand: Expression = field(default_factory=Expression)


@dataclass
class BinaryOp(Expression):
    """Binary mathematical prescription: left op right."""
    left: Expression = field(default_factory=Expression)
    op: str = ""
    right: Expression = field(default_factory=Expression)


@dataclass
class TupleExpr(Expression):
    """A tuple of expressions (e.g. multi-value returns)."""
    elements: List[Expression] = field(default_factory=list)


@dataclass
class EmptyLiteral(Expression):
    """An empty determination literal: empty / none / nu / 𒉡."""
    value: str = "empty"


@dataclass
class FieldAccess(Expression):
    """Record / determination field access: record.field or field of record."""
    record: Expression = field(default_factory=Expression)
    field: str = ""


@dataclass
class PostfixExpr(Expression):
    """A postfix calculation sequence composed of operands and operators."""
    steps: List[Any] = field(default_factory=list)


@dataclass
class CompareExpr(Expression):
    """Mathematical comparison: left is relation [than right] (e.g. error is lesser than best.error)."""
    left: Expression = field(default_factory=Expression)
    relation: str = "lesser"
    right: Optional[Expression] = None


@dataclass
class IsExpr(Expression):
    """State / emptiness predicate: target is predicate (e.g. best is empty)."""
    target: Expression = field(default_factory=Expression)
    predicate: str = "empty"


# ==============================================================================
# Statements / Prescriptions
# ==============================================================================

@dataclass
class Statement(ASTNode):
    """Base class for statements."""
    pass


@dataclass
class Declaration(Statement):
    """Quantity establishment: name : expr [unit]."""
    name: str = ""
    value: Expression = field(default_factory=Expression)
    unit: Optional[str] = None


@dataclass
class Assignment(Statement):
    """Quantity assignment: target := expr or t1, t2 := expr1, expr2 / call."""
    targets: List[str] = field(default_factory=list)
    value: Expression = field(default_factory=Expression)


@dataclass
class Conditional(Statement):
    """Conditional branch: e-a / if cond : body [ nu-e-a / else : alternative ]."""
    condition: Expression = field(default_factory=Expression)
    body: List[Statement] = field(default_factory=list)
    alternative: Optional[List[Statement]] = None


@dataclass
class Repetition(Statement):
    """Bounded repetition: gi / repeat id [start iti] end : body."""
    target: str = ""
    start: Optional[Expression] = None
    end: Expression = field(default_factory=Expression)
    body: List[Statement] = field(default_factory=list)


@dataclass
class ReturnStatement(Statement):
    """Procedure return: ges / return expr1, expr2, ..."""
    values: List[Expression] = field(default_factory=list)


@dataclass
class OutputStatement(Statement):
    """Output statement: diš-a / output expr."""
    value: Expression = field(default_factory=Expression)


@dataclass
class ExpressionStatement(Statement):
    """Expression evaluated for side effects (e.g. call)."""
    expr: Expression = field(default_factory=Expression)


@dataclass
class Determination(Statement):
    """Determination record declaration: name : field1, field2, ..."""
    name: str = ""
    fields: List[str] = field(default_factory=list)
    field_values: Optional[Dict[str, Expression]] = None


@dataclass
class RetainStatement(Statement):
    """Atomic determination selection: retain candidate when condition."""
    candidate: str = ""
    condition: Expression = field(default_factory=Expression)
    target: str = "best"
    comparator: Optional[str] = None


@dataclass
class DomainRepetition(Repetition):
    """Finite mathematical search domain: consider target from start through end: body."""
    pass


@dataclass
class Recipe(Statement):
    """Mathematical procedure recipe: recipe name param1 param2: body."""
    name: str = ""
    parameters: List[str] = field(default_factory=list)
    body: List[Statement] = field(default_factory=list)


# ==============================================================================
# Tablet Structure
# ==============================================================================

@dataclass
class ProblemSection(ASTNode):
    """Problem section: e-diš / 𒂊𒁹 block."""
    body: List[Statement] = field(default_factory=list)


@dataclass
class ResultSection(ASTNode):
    """Result section: ka-diš / 𒅗𒁹 block."""
    body: List[Statement] = field(default_factory=list)


@dataclass
class Procedure(ASTNode):
    """Procedure declaration: dub-sar / 𒁾𒊬 name(params): block."""
    name: str = ""
    parameters: List[str] = field(default_factory=list)
    body: List[Statement] = field(default_factory=list)


@dataclass
class Program(ASTNode):
    """A complete DUB.SAR tablet: Problem + Procedures + Result."""
    problem: ProblemSection = field(default_factory=ProblemSection)
    procedures: List[Procedure] = field(default_factory=list)
    result: ResultSection = field(default_factory=ResultSection)

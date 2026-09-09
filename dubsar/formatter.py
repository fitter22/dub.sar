"""DUB.SAR 1.0 — Canonical Source Formatter and Source Mode Detection.

Implements CR-040 and CR-041:
- Canonicalizes indentation, spacing, keywords, and numeric representations
- Supports formatting in Tablet, Scholar, or preserved mode
- Automatic detection of source mode (tablet, scholar, mixed)
"""

from __future__ import annotations

import re
from typing import List, Optional

from dubsar.ast import (
    ApplyRecipe,
    Assignment,
    BinaryOp,
    CallExpr,
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
)
from dubsar.lexer import Lexer
from dubsar.parser import Parser


def detect_source_mode(source: str) -> str:
    """Detects whether source is Tablet (cuneiform), Scholar (Latin), or Mixed.

    Returns: 'tablet', 'scholar', or 'mixed'.
    """
    has_cuneiform = bool(re.search(r"[\U00012000-\U0001247F\U00012480-\U0001254F]", source))
    scholar_keywords = re.search(r"\b(PROBLEM|RESULT|procedure|repeat|output|input|return)\b", source, re.IGNORECASE)

    if has_cuneiform and scholar_keywords:
        return "mixed"
    elif has_cuneiform:
        return "tablet"
    return "scholar"


class Formatter:
    """Formats a DUB.SAR AST into canonical source representation."""

    def __init__(self, mode: str = "tablet") -> None:
        self.mode = mode.lower()

    def format(self, program: Program) -> str:
        lines: List[str] = []

        is_tablet = self.mode == "tablet"

        # 1. Problem Section
        prob_kw = "𒂊𒁹" if is_tablet else "PROBLEM"
        lines.append(prob_kw)
        for stmt in program.problem.body:
            lines.append(self._format_statement(stmt, indent=4, is_tablet=is_tablet))

        # 2. Procedures
        for proc in program.procedures:
            lines.append("")
            proc_kw = "𒁾𒊬" if is_tablet else "recipe"
            params_str = " ".join(proc.parameters)
            lines.append(f"{proc_kw} {proc.name} {params_str}:")
            for stmt in proc.body:
                lines.append(self._format_statement(stmt, indent=4, is_tablet=is_tablet))

        # 3. Result Section
        lines.append("")
        res_kw = "𒅗𒁹" if is_tablet else "result"
        lines.append(res_kw)
        for stmt in program.result.body:
            lines.append(self._format_statement(stmt, indent=4, is_tablet=is_tablet))

        lines.append("")
        return "\n".join(lines)

    def _format_statement(self, stmt: Statement, indent: int = 4, is_tablet: bool = True) -> str:
        pad = " " * indent

        if isinstance(stmt, Declaration):
            if isinstance(stmt.value, PostfixExpr) and len(stmt.value.steps) > 1:
                step_lines = [f"{pad}{stmt.name} :"]
                for step in stmt.value.steps:
                    if isinstance(step, str):
                        if is_tablet:
                            tablet_ops = {
                                "floor": "𒄥", "ceil": "𒉏", "nearest": "𒊑",
                                "absolute": "𒋼", "add": "𒍣", "subtract": "𒋫",
                                "multiply": "𒊭", "divide": "𒉌", "lesser": "𒌉",
                                "greater": "𒃲", "equal": "𒊓",
                            }
                            s_str = tablet_ops.get(step.lower(), step)
                        else:
                            s_str = step
                    elif isinstance(step, Expression):
                        s_str = self._format_expression(step, is_tablet)
                    else:
                        s_str = str(step)
                    step_lines.append(f"{pad}    {s_str}")
                return "\n".join(step_lines)
            val_str = self._format_expression(stmt.value, is_tablet)
            unit_str = f" {stmt.unit}" if stmt.unit else ""
            return f"{pad}{stmt.name} : {val_str}{unit_str}"

        elif isinstance(stmt, Assignment):
            val_str = self._format_expression(stmt.value, is_tablet)
            targets_str = ", ".join(stmt.targets)
            return f"{pad}{targets_str} := {val_str}"

        elif isinstance(stmt, Conditional):
            if_kw = "𒂊𒀀" if is_tablet else "when"
            cond_str = self._format_expression(stmt.condition, is_tablet)
            res = [f"{pad}{if_kw} {cond_str}:"]
            for s in stmt.body:
                res.append(self._format_statement(s, indent + 4, is_tablet))
            if stmt.alternative:
                else_kw = "𒉡𒂊𒀀" if is_tablet else "else"
                res.append(f"{pad}{else_kw}:")
                for s in stmt.alternative:
                    res.append(self._format_statement(s, indent + 4, is_tablet))
            return "\n".join(res)

        elif isinstance(stmt, Determination):
            det_lines = [f"{pad}{stmt.name} :"]
            for f in stmt.fields:
                det_lines.append(f"{pad}    {f}")
            return "\n".join(det_lines)

        elif isinstance(stmt, RetainStatement):
            ret_kw = "𒋼" if is_tablet else "retain"
            when_kw = "𒂊𒀀" if is_tablet else "when"
            cond_str = self._format_expression(stmt.condition, is_tablet)
            return f"{pad}{ret_kw} {stmt.candidate}\n{pad}    {when_kw} {cond_str}"

        elif isinstance(stmt, DomainRepetition):
            rep_kw = "𒄀" if is_tablet else "consider"
            from_kw = "𒋫 " if is_tablet else "from "
            to_kw = "𒂗" if is_tablet else "through"
            start_str = f"{from_kw}{self._format_expression(stmt.start, is_tablet)} {to_kw} " if stmt.start else ""
            end_str = self._format_expression(stmt.end, is_tablet)
            res = [f"{pad}{rep_kw} {stmt.target} {start_str}{end_str}:"]
            for s in stmt.body:
                res.append(self._format_statement(s, indent + 4, is_tablet))
            return "\n".join(res)

        elif isinstance(stmt, Repetition):
            rep_kw = "𒄀" if is_tablet else "repeat"
            to_kw = "𒂗" if is_tablet else "through"
            start_str = f"{self._format_expression(stmt.start, is_tablet)} {to_kw} " if stmt.start else ""
            end_str = self._format_expression(stmt.end, is_tablet)
            res = [f"{pad}{rep_kw} {stmt.target} {start_str}{end_str}:"]
            for s in stmt.body:
                res.append(self._format_statement(s, indent + 4, is_tablet))
            return "\n".join(res)

        elif isinstance(stmt, ReturnStatement):
            ret_kw = "𒉆" if is_tablet else "determine"
            vals_str = ", ".join(self._format_expression(v, is_tablet) for v in stmt.values)
            return f"{pad}{ret_kw} {vals_str}" if vals_str else f"{pad}{ret_kw}"

        elif isinstance(stmt, OutputStatement):
            out_kw = "𒁹𒀀" if is_tablet else "output"
            val_str = self._format_expression(stmt.value, is_tablet)
            return f"{pad}{out_kw} {val_str}"

        elif isinstance(stmt, ExpressionStatement):
            return f"{pad}{self._format_expression(stmt.expr, is_tablet)}"

        return ""

    def _format_expression(self, expr: Expression, is_tablet: bool = True) -> str:
        if isinstance(expr, NumberLiteral):
            val_str = expr.value.format_canonical()
            if expr.unit:
                u_str = " 𒌓" if is_tablet and expr.unit in ("day", "ud", "𒌓") else f" {expr.unit}"
                return f"{val_str}{u_str}"
            return val_str

        elif isinstance(expr, EmptyLiteral):
            return "𒉡" if is_tablet else "empty"

        elif isinstance(expr, FieldAccess):
            rec_str = self._format_expression(expr.record, is_tablet)
            return f"{rec_str}.{expr.field}"

        elif isinstance(expr, PostfixExpr):
            parts = []
            for step in expr.steps:
                if isinstance(step, str):
                    if is_tablet:
                        tablet_ops = {
                            "floor": "𒄥", "ceil": "𒉏", "nearest": "𒊑",
                            "absolute": "𒋼", "add": "𒍣", "subtract": "𒋫",
                            "multiply": "𒊭", "divide": "𒉌", "lesser": "𒌉",
                            "greater": "𒃲", "equal": "𒊓",
                        }
                        parts.append(tablet_ops.get(step.lower(), step))
                    else:
                        parts.append(step)
                elif isinstance(step, Expression):
                    parts.append(self._format_expression(step, is_tablet))
                else:
                    parts.append(str(step))
            return " ".join(parts)

        elif isinstance(expr, CompareExpr):
            left_str = self._format_expression(expr.left, is_tablet)
            right_str = self._format_expression(expr.right, is_tablet) if expr.right else ""
            rel = getattr(expr, "relation", getattr(expr, "op", "lesser"))
            if is_tablet:
                cmp_kw = {"lesser": "𒌉", "greater": "𒃲", "equal": "𒊓", "not-equal": "nu-sa"}.get(rel, rel)
                return f"{left_str} {cmp_kw} {right_str}"
            else:
                return f"{left_str} is {rel} than {right_str}"

        elif isinstance(expr, IsExpr):
            target_str = self._format_expression(expr.target, is_tablet)
            if is_tablet:
                pred_kw = "𒉡" if expr.predicate == "empty" else "la-nu"
                return f"{target_str} e {pred_kw}"
            else:
                return f"{target_str} is {expr.predicate}"

        elif isinstance(expr, StringLiteral):
            return f'"{expr.value}"'

        elif isinstance(expr, Identifier):
            return expr.name

        elif isinstance(expr, InputExpr):
            in_kw = "𒀀𒁹" if is_tablet else "ask"
            return f'{in_kw} "{expr.prompt}"'

        elif isinstance(expr, CallExpr):
            args_str = ", ".join(self._format_expression(a, is_tablet) for a in expr.arguments)
            return f"{expr.callee}({args_str})"

        elif isinstance(expr, ApplyRecipe):
            ak_kw = "𒀝" if is_tablet else "apply"
            return f"{ak_kw} {expr.recipe}"

        elif isinstance(expr, UnaryOp):
            if expr.op in ("not", "nu", "𒉡"):
                op_str = "𒉡 " if is_tablet else "not "
            else:
                op_str = "-"
            return f"{op_str}{self._format_expression(expr.operand, is_tablet)}"

        elif isinstance(expr, BinaryOp):
            left_str = self._format_expression(expr.left, is_tablet)
            right_str = self._format_expression(expr.right, is_tablet)
            op_str = expr.op
            if is_tablet:
                tablet_ops = {"<": "𒌉", ">": "𒃲", "==": "𒊓"}
                op_str = tablet_ops.get(expr.op, expr.op)
            return f"{left_str} {op_str} {right_str}"

        elif isinstance(expr, TupleExpr):
            return ", ".join(self._format_expression(e, is_tablet) for e in expr.elements)

        return ""


def format_source(source: str, mode: Optional[str] = None) -> str:
    """Formats DUB.SAR source code into canonical layout."""
    if mode is None or mode == "auto":
        mode = detect_source_mode(source)

    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()
    formatter = Formatter(mode=mode)
    return formatter.format(program)

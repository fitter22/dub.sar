"""DUB.SAR 1.0 — Stack-Oriented Intermediate Representation (IR).

Implements Section 21 and Section 22:
- Stack-oriented bytecode instructions
- Semantic IR lowering from AST to bytecode
- Constant table, variable symbols, and label resolution
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union

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
from dubsar.numbers import Rational
from dubsar.units import DIMENSIONLESS, Quantity, Unit, lookup_unit


class OpCode(Enum):
    CONST = auto()          # Push constant value onto stack
    LOAD = auto()           # Load variable onto stack
    STORE = auto()          # Store top of stack into variable
    UNPACK = auto()         # Unpack tuple from stack into multiple variables
    ADD = auto()            # Pop b, a; push a + b
    SUB = auto()            # Pop b, a; push a - b
    MUL = auto()            # Pop b, a; push a * b
    DIV = auto()            # Pop b, a; push a / b
    REM = auto()            # Pop b, a; push a % b
    POW_INT = auto()        # Pop b, a; push a ** b
    CMP = auto()            # Pop b, a; push a cmp b (arg: '==', '<', etc.)
    NOT = auto()            # Pop a; push not a
    NEG = auto()            # Pop a; push -a
    JUMP = auto()           # Unconditional jump (arg: instruction index)
    JUMP_IF_FALSE = auto()  # Jump if top of stack is false
    POP = auto()            # Discard top of stack
    CALL = auto()           # Call procedure / builtin (arg: (name, argc))
    RETURN = auto()         # Return from procedure (arg: count)
    FLOOR = auto()          # Pop a; push floor(a)
    CEIL = auto()           # Pop a; push ceil(a)
    NEAREST = auto()        # Pop a; push nearest(a)
    ABS = auto()            # Pop a; push abs(a)
    INPUT = auto()          # Pop prompt; push input quantity
    OUTPUT = auto()         # Pop a; output it
    HALT = auto()           # End execution


@dataclass
class Instruction:
    """A single bytecode instruction."""
    op: OpCode
    arg: Any = None
    line: int = 0

    def __repr__(self) -> str:
        if self.arg is not None:
            return f"{self.op.name:<14} {self.arg!r}"
        return self.op.name


@dataclass
class BytecodeChunk:
    """A sequence of bytecode instructions for a tablet section or procedure."""
    name: str
    parameters: List[str] = field(default_factory=list)
    instructions: List[Instruction] = field(default_factory=list)

    def emit(self, op: OpCode, arg: Any = None, line: int = 0) -> int:
        idx = len(self.instructions)
        self.instructions.append(Instruction(op, arg, line))
        return idx

    def disassemble(self) -> str:
        lines = [f"=== {self.name} ==="]
        if self.parameters:
            lines.append(f"  params: {', '.join(self.parameters)}")
        for idx, instr in enumerate(self.instructions):
            lines.append(f"  {idx:04d}: {instr}")
        return "\n".join(lines)


@dataclass
class CompiledTablet:
    """A fully compiled DUB.SAR program containing main chunk and procedures."""
    main_chunk: BytecodeChunk
    procedures: Dict[str, BytecodeChunk] = field(default_factory=dict)

    def disassemble(self) -> str:
        chunks = [self.main_chunk.disassemble()]
        for proc in self.procedures.values():
            chunks.append(proc.disassemble())
        return "\n\n".join(chunks)


class Compiler:
    """Compiles DUB.SAR AST to stack-oriented IR bytecode."""

    def __init__(self) -> None:
        self.current_chunk: Optional[BytecodeChunk] = None

    def compile(self, program: Program) -> CompiledTablet:
        # 1. Compile procedures
        procedures: Dict[str, BytecodeChunk] = {}
        for proc in program.procedures:
            proc_chunk = BytecodeChunk(name=f"proc:{proc.name}", parameters=proc.parameters)
            self.current_chunk = proc_chunk
            for stmt in proc.body:
                self._compile_statement(stmt)
            # Default return if needed
            if not proc_chunk.instructions or proc_chunk.instructions[-1].op != OpCode.RETURN:
                proc_chunk.emit(OpCode.CONST, Quantity(0, DIMENSIONLESS), proc.line)
                proc_chunk.emit(OpCode.RETURN, 1, proc.line)
            procedures[proc.name] = proc_chunk

        # 2. Compile main chunk (problem section followed by result section)
        main_chunk = BytecodeChunk(name="main")
        self.current_chunk = main_chunk

        for stmt in program.problem.body:
            self._compile_statement(stmt)

        for stmt in program.result.body:
            self._compile_statement(stmt)

        main_chunk.emit(OpCode.HALT, None, program.line)

        return CompiledTablet(main_chunk=main_chunk, procedures=procedures)

    def _compile_statement(self, stmt: Statement) -> None:
        assert self.current_chunk is not None
        chunk = self.current_chunk

        if isinstance(stmt, Declaration):
            self._compile_expression(stmt.value)
            if stmt.unit is not None:
                # Multiply by unit or wrap with unit
                u = lookup_unit(stmt.unit)
                chunk.emit(OpCode.CONST, Quantity(1, u), stmt.line)
                chunk.emit(OpCode.MUL, None, stmt.line)
            chunk.emit(OpCode.STORE, stmt.name, stmt.line)

        elif isinstance(stmt, Assignment):
            self._compile_expression(stmt.value)
            if len(stmt.targets) == 1:
                chunk.emit(OpCode.STORE, stmt.targets[0], stmt.line)
            else:
                chunk.emit(OpCode.UNPACK, stmt.targets, stmt.line)

        elif isinstance(stmt, Conditional):
            self._compile_expression(stmt.condition)
            # Emit jump if false with placeholder
            jump_false_idx = chunk.emit(OpCode.JUMP_IF_FALSE, None, stmt.line)

            # Compile true block
            for s in stmt.body:
                self._compile_statement(s)

            if stmt.alternative:
                # Jump over alternative from end of true block
                jump_end_idx = chunk.emit(OpCode.JUMP, None, stmt.line)
                # Patch jump_false to point to start of alternative
                chunk.instructions[jump_false_idx].arg = len(chunk.instructions)
                for s in stmt.alternative:
                    self._compile_statement(s)
                # Patch jump_end to point past alternative
                chunk.instructions[jump_end_idx].arg = len(chunk.instructions)
            else:
                chunk.instructions[jump_false_idx].arg = len(chunk.instructions)

        elif isinstance(stmt, Repetition):
            # Evaluate start
            if stmt.start is not None:
                self._compile_expression(stmt.start)
            else:
                chunk.emit(OpCode.CONST, Quantity(1, DIMENSIONLESS), stmt.line)

            # Store in loop variable
            chunk.emit(OpCode.STORE, stmt.target, stmt.line)

            # Loop start label
            loop_start = len(chunk.instructions)

            # Condition check: loop_var <= end
            chunk.emit(OpCode.LOAD, stmt.target, stmt.line)
            self._compile_expression(stmt.end)
            chunk.emit(OpCode.CMP, "<=", stmt.line)

            jump_exit_idx = chunk.emit(OpCode.JUMP_IF_FALSE, None, stmt.line)

            # Loop body
            for s in stmt.body:
                self._compile_statement(s)

            # Increment loop variable: loop_var := loop_var + 1
            chunk.emit(OpCode.LOAD, stmt.target, stmt.line)
            chunk.emit(OpCode.CONST, Quantity(1, DIMENSIONLESS), stmt.line)
            chunk.emit(OpCode.ADD, None, stmt.line)
            chunk.emit(OpCode.STORE, stmt.target, stmt.line)

            # Jump back to start
            chunk.emit(OpCode.JUMP, loop_start, stmt.line)

            # Patch exit jump
            chunk.instructions[jump_exit_idx].arg = len(chunk.instructions)

        elif isinstance(stmt, ReturnStatement):
            for val in stmt.values:
                self._compile_expression(val)
            chunk.emit(OpCode.RETURN, len(stmt.values), stmt.line)

        elif isinstance(stmt, OutputStatement):
            self._compile_expression(stmt.value)
            chunk.emit(OpCode.OUTPUT, None, stmt.line)

        elif isinstance(stmt, ExpressionStatement):
            self._compile_expression(stmt.expr)
            chunk.emit(OpCode.POP, None, stmt.line)

    def _compile_expression(self, expr: Expression) -> None:
        assert self.current_chunk is not None
        chunk = self.current_chunk

        if isinstance(expr, NumberLiteral):
            u = lookup_unit(expr.unit) if expr.unit else DIMENSIONLESS
            chunk.emit(OpCode.CONST, Quantity(expr.value, u), expr.line)

        elif isinstance(expr, StringLiteral):
            chunk.emit(OpCode.CONST, expr.value, expr.line)

        elif isinstance(expr, InputExpr):
            chunk.emit(OpCode.CONST, expr.prompt, expr.line)
            chunk.emit(OpCode.INPUT, None, expr.line)

        elif isinstance(expr, Identifier):
            chunk.emit(OpCode.LOAD, expr.name, expr.line)

        elif isinstance(expr, CallExpr):
            # Special bytecode opcodes for math builtins
            if expr.callee == "floor" and len(expr.arguments) == 1:
                self._compile_expression(expr.arguments[0])
                chunk.emit(OpCode.FLOOR, None, expr.line)
            elif expr.callee == "ceil" and len(expr.arguments) == 1:
                self._compile_expression(expr.arguments[0])
                chunk.emit(OpCode.CEIL, None, expr.line)
            elif expr.callee == "nearest" and len(expr.arguments) == 1:
                self._compile_expression(expr.arguments[0])
                chunk.emit(OpCode.NEAREST, None, expr.line)
            elif expr.callee == "abs" and len(expr.arguments) == 1:
                self._compile_expression(expr.arguments[0])
                chunk.emit(OpCode.ABS, None, expr.line)
            else:
                for arg in expr.arguments:
                    self._compile_expression(arg)
                chunk.emit(OpCode.CALL, (expr.callee, len(expr.arguments)), expr.line)

        elif isinstance(expr, UnaryOp):
            self._compile_expression(expr.operand)
            if expr.op in ("-", "ta", "𒋫"):
                chunk.emit(OpCode.NEG, None, expr.line)
            elif expr.op in ("not", "nu", "𒉡"):
                chunk.emit(OpCode.NOT, None, expr.line)

        elif isinstance(expr, BinaryOp):
            self._compile_expression(expr.left)
            self._compile_expression(expr.right)
            if expr.op in ("+", "zi", "add", "𒍣"):
                chunk.emit(OpCode.ADD, None, expr.line)
            elif expr.op in ("-", "ta", "sub", "𒋫"):
                chunk.emit(OpCode.SUB, None, expr.line)
            elif expr.op in ("*", "ša", "sha", "mul", "𒊭"):
                chunk.emit(OpCode.MUL, None, expr.line)
            elif expr.op in ("/", "ni", "div", "𒉌"):
                chunk.emit(OpCode.DIV, None, expr.line)
            elif expr.op == "%":
                chunk.emit(OpCode.REM, None, expr.line)
            elif expr.op == "**":
                chunk.emit(OpCode.POW_INT, None, expr.line)
            elif expr.op in ("==", "!=", "<", "<=", ">", ">="):
                chunk.emit(OpCode.CMP, expr.op, expr.line)

        elif isinstance(expr, TupleExpr):
            for e in expr.elements:
                self._compile_expression(e)

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
    EMPTY = auto()          # Push empty determination onto stack
    DETERMINE = auto()      # Create determination record: arg = (name, fields)
    FIELD_GET = auto()      # Pop record; push field value: arg = field_name
    RETAIN = auto()         # Pop condition; retain candidate into target if condition is True: arg = (candidate, target)
    CONSULT = auto()        # Consult persistent tablet: arg=(has_version, alias)
    WORKING_CREATE = auto() # Create working tablet: arg=(name, shape)
    TABLET_COPY = auto()    # Copy tablet: arg=(target, has_source, has_version)
    TABLET_DERIVE = auto()  # Derive tablet: arg=(target, has_source, has_version)
    TABLET_INSCRIBE = auto()# Inscribe working tablet: arg=working_name
    WORKING_PUT = auto()    # Put into working tablet: arg=working_name
    WORKING_REPLACE = auto()# Replace in working tablet: arg=working_name
    WORKING_REMOVE = auto() # Remove from working tablet: arg=working_name
    ENTRY_TAKE = auto()     # Pop key, tablet; push entry value
    ENTRY_SEEK = auto()     # Pop target, tablet; push nearest entry value
    TABLET_HISTORY = auto() # Pop tablet; push tablet history
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


from dubsar.semantic_ir import (
    ApplyMathVerb,
    AssignVerb,
    ConcludeVerb,
    DetermineVerb,
    DiscardVerb,
    EstablishVerb,
    FieldLookup,
    InscribeVerb,
    MakeDetermination,
    PostfixCalc,
    ProcedureRecipe,
    ReceiveInput,
    RepeatVerb,
    RetainVerb,
    SemanticProgram,
    SemanticVerb,
    TakeEmpty,
    TakeLiteral,
    TakeQuantity,
    TakeText,
    TuplePack,
    VerbExpr,
    ConsultTabletVerb,
    CreateWorkingTabletVerb,
    CopyTabletVerb,
    DeriveTabletVerb,
    InscribeTabletVerb,
    PutTabletEntryVerb,
    ReplaceTabletEntryVerb,
    RemoveTabletEntryVerb,
    TakeTabletEntry,
    SeekTabletEntry,
    InspectTabletHistory,
    ast_to_semantic_ir,
)


class Compiler:
    """Compiles DUB.SAR AST or Semantic IR to stack-oriented IR bytecode."""

    def __init__(self) -> None:
        self.current_chunk: Optional[BytecodeChunk] = None
        self.proc_param_counts: Dict[str, int] = {}

    def compile(self, program: Union[Program, SemanticProgram]) -> CompiledTablet:
        if isinstance(program, Program):
            sem_prog = ast_to_semantic_ir(program)
        else:
            sem_prog = program

        return self.compile_semantic_program(sem_prog)

    def compile_semantic_program(self, sem_prog: SemanticProgram) -> CompiledTablet:
        self.proc_param_counts = {proc.name: len(proc.parameters) for proc in sem_prog.procedures}
        # 1. Compile procedures
        procedures: Dict[str, BytecodeChunk] = {}
        for proc in sem_prog.procedures:
            proc_chunk = BytecodeChunk(name=f"proc:{proc.name}", parameters=proc.parameters)
            self.current_chunk = proc_chunk
            for verb in proc.body:
                self._compile_verb(verb)
            if not proc_chunk.instructions or proc_chunk.instructions[-1].op != OpCode.RETURN:
                proc_chunk.emit(OpCode.CONST, Quantity(0, DIMENSIONLESS), proc.line)
                proc_chunk.emit(OpCode.RETURN, 1, proc.line)
            procedures[proc.name] = proc_chunk

        # 2. Compile main chunk
        main_chunk = BytecodeChunk(name="main")
        self.current_chunk = main_chunk

        for verb in sem_prog.problem_verbs:
            self._compile_verb(verb)

        for verb in sem_prog.result_verbs:
            self._compile_verb(verb)

        main_chunk.emit(OpCode.HALT, None, sem_prog.line)

        return CompiledTablet(main_chunk=main_chunk, procedures=procedures)

    def _compile_verb(self, verb: SemanticVerb) -> None:
        assert self.current_chunk is not None
        chunk = self.current_chunk

        if isinstance(verb, EstablishVerb):
            self._compile_verb_expr(verb.value)
            if verb.unit is not None:
                u = lookup_unit(verb.unit)
                chunk.emit(OpCode.CONST, Quantity(1, u), verb.line)
                chunk.emit(OpCode.MUL, None, verb.line)
            chunk.emit(OpCode.STORE, verb.name, verb.line)

        elif isinstance(verb, AssignVerb):
            self._compile_verb_expr(verb.value)
            if len(verb.targets) == 1:
                chunk.emit(OpCode.STORE, verb.targets[0], verb.line)
            else:
                chunk.emit(OpCode.UNPACK, verb.targets, verb.line)

        elif isinstance(verb, DetermineVerb):
            self._compile_verb_expr(verb.condition)
            jump_false_idx = chunk.emit(OpCode.JUMP_IF_FALSE, None, verb.line)
            for v in verb.body:
                self._compile_verb(v)

            if verb.alternative:
                jump_end_idx = chunk.emit(OpCode.JUMP, None, verb.line)
                chunk.instructions[jump_false_idx].arg = len(chunk.instructions)
                for v in verb.alternative:
                    self._compile_verb(v)
                chunk.instructions[jump_end_idx].arg = len(chunk.instructions)
            else:
                chunk.instructions[jump_false_idx].arg = len(chunk.instructions)

        elif isinstance(verb, RepeatVerb):
            if verb.start is not None:
                self._compile_verb_expr(verb.start)
            else:
                chunk.emit(OpCode.CONST, Quantity(1, DIMENSIONLESS), verb.line)

            chunk.emit(OpCode.STORE, verb.target, verb.line)
            loop_start = len(chunk.instructions)

            chunk.emit(OpCode.LOAD, verb.target, verb.line)
            self._compile_verb_expr(verb.end)
            chunk.emit(OpCode.CMP, "<=", verb.line)

            jump_exit_idx = chunk.emit(OpCode.JUMP_IF_FALSE, None, verb.line)

            for v in verb.body:
                self._compile_verb(v)

            chunk.emit(OpCode.LOAD, verb.target, verb.line)
            chunk.emit(OpCode.CONST, Quantity(1, DIMENSIONLESS), verb.line)
            chunk.emit(OpCode.ADD, None, verb.line)
            chunk.emit(OpCode.STORE, verb.target, verb.line)
            chunk.emit(OpCode.JUMP, loop_start, verb.line)

            chunk.instructions[jump_exit_idx].arg = len(chunk.instructions)

        elif isinstance(verb, ConcludeVerb):
            for val in verb.values:
                self._compile_verb_expr(val)
            chunk.emit(OpCode.RETURN, len(verb.values), verb.line)

        elif isinstance(verb, InscribeVerb):
            self._compile_verb_expr(verb.value)
            chunk.emit(OpCode.OUTPUT, None, verb.line)

        elif isinstance(verb, DiscardVerb):
            self._compile_verb_expr(verb.expr)
            chunk.emit(OpCode.POP, None, verb.line)

        elif isinstance(verb, MakeDetermination):
            for fname in verb.fields:
                chunk.emit(OpCode.LOAD, fname, verb.line)
            chunk.emit(OpCode.DETERMINE, (verb.name, verb.fields), verb.line)

        elif isinstance(verb, RetainVerb):
            self._compile_verb_expr(verb.condition)
            chunk.emit(OpCode.RETAIN, (verb.candidate, verb.target), verb.line)

        elif isinstance(verb, ConsultTabletVerb):
            self._compile_verb_expr(verb.tablet_name)
            if verb.version:
                self._compile_verb_expr(verb.version)
                chunk.emit(OpCode.CONSULT, (True, verb.alias), verb.line)
            else:
                chunk.emit(OpCode.CONSULT, (False, verb.alias), verb.line)

        elif isinstance(verb, CreateWorkingTabletVerb):
            chunk.emit(OpCode.WORKING_CREATE, (verb.name, verb.shape), verb.line)

        elif isinstance(verb, CopyTabletVerb):
            has_source = False
            if verb.source:
                self._compile_verb_expr(verb.source)
                has_source = True
            has_version = False
            if verb.version:
                self._compile_verb_expr(verb.version)
                has_version = True
            chunk.emit(OpCode.TABLET_COPY, (verb.target, has_source, has_version), verb.line)

        elif isinstance(verb, DeriveTabletVerb):
            has_source = False
            if verb.source:
                self._compile_verb_expr(verb.source)
                has_source = True
            has_version = False
            if verb.version:
                self._compile_verb_expr(verb.version)
                has_version = True
            chunk.emit(OpCode.TABLET_DERIVE, (verb.target, has_source, has_version), verb.line)

        elif isinstance(verb, InscribeTabletVerb):
            self._compile_verb_expr(verb.target_name)
            chunk.emit(OpCode.TABLET_INSCRIBE, verb.working_name, verb.line)

        elif isinstance(verb, PutTabletEntryVerb):
            if verb.key is not None:
                self._compile_verb_expr(verb.key)
            else:
                chunk.emit(OpCode.EMPTY, None, verb.line)
            self._compile_verb_expr(verb.value)
            chunk.emit(OpCode.WORKING_PUT, verb.working_name, verb.line)

        elif isinstance(verb, ReplaceTabletEntryVerb):
            self._compile_verb_expr(verb.key)
            self._compile_verb_expr(verb.value)
            chunk.emit(OpCode.WORKING_REPLACE, verb.working_name, verb.line)

        elif isinstance(verb, RemoveTabletEntryVerb):
            self._compile_verb_expr(verb.key)
            chunk.emit(OpCode.WORKING_REMOVE, verb.working_name, verb.line)

    def _compile_verb_expr(self, expr: VerbExpr) -> None:
        assert self.current_chunk is not None
        chunk = self.current_chunk

        if isinstance(expr, TakeLiteral):
            u = lookup_unit(expr.unit) if expr.unit else DIMENSIONLESS
            chunk.emit(OpCode.CONST, Quantity(expr.value, u), expr.line)

        elif isinstance(expr, TakeText):
            chunk.emit(OpCode.CONST, expr.value, expr.line)

        elif isinstance(expr, TakeQuantity):
            chunk.emit(OpCode.LOAD, expr.name, expr.line)

        elif isinstance(expr, ReceiveInput):
            chunk.emit(OpCode.CONST, expr.prompt, expr.line)
            chunk.emit(OpCode.INPUT, None, expr.line)

        elif isinstance(expr, ApplyMathVerb):
            if expr.verb in ("FLOOR", "CEIL", "NEAREST", "ABS"):
                if expr.operands:
                    self._compile_verb_expr(expr.operands[0])
                op_code = getattr(OpCode, expr.verb)
                chunk.emit(op_code, None, expr.line)
            elif expr.verb == "INVOKE":
                callee = expr.callee or ""
                if callee == "floor" and len(expr.operands) == 1:
                    self._compile_verb_expr(expr.operands[0])
                    chunk.emit(OpCode.FLOOR, None, expr.line)
                elif callee == "ceil" and len(expr.operands) == 1:
                    self._compile_verb_expr(expr.operands[0])
                    chunk.emit(OpCode.CEIL, None, expr.line)
                elif callee == "nearest" and len(expr.operands) == 1:
                    self._compile_verb_expr(expr.operands[0])
                    chunk.emit(OpCode.NEAREST, None, expr.line)
                elif callee == "abs" and len(expr.operands) == 1:
                    self._compile_verb_expr(expr.operands[0])
                    chunk.emit(OpCode.ABS, None, expr.line)
                else:
                    argc = len(expr.operands)
                    if argc > 0:
                        for op_arg in expr.operands:
                            self._compile_verb_expr(op_arg)
                    else:
                        if callee in BUILTINS:
                            import inspect
                            argc = len(inspect.signature(BUILTINS[callee]).parameters)
                        else:
                            argc = self.proc_param_counts.get(callee, 0)
                    chunk.emit(OpCode.CALL, (callee, argc), expr.line)
            elif expr.verb == "NEGATE":
                self._compile_verb_expr(expr.operands[0])
                chunk.emit(OpCode.NEG, None, expr.line)
            elif expr.verb == "NOT":
                self._compile_verb_expr(expr.operands[0])
                chunk.emit(OpCode.NOT, None, expr.line)
            elif expr.verb == "COMPARE":
                cmp_map = {"lesser": "<", "greater": ">", "equal": "==", "not-equal": "!="}
                cmp_op = cmp_map.get(expr.relation, expr.relation or "<")
                if len(expr.operands) == 1:
                    self._compile_verb_expr(expr.operands[0])
                    if isinstance(expr.operands[0], TakeQuantity):
                        chunk.emit(OpCode.LOAD, "best", expr.line)
                        chunk.emit(OpCode.FIELD_GET, expr.operands[0].name, expr.line)
                    chunk.emit(OpCode.CMP, cmp_op, expr.line)
                elif len(expr.operands) >= 2:
                    self._compile_verb_expr(expr.operands[0])
                    self._compile_verb_expr(expr.operands[1])
                    chunk.emit(OpCode.CMP, cmp_op, expr.line)
            elif expr.verb == "IS":
                if expr.relation in ("empty", "none"):
                    self._compile_verb_expr(expr.operands[0])
                    chunk.emit(OpCode.EMPTY, None, expr.line)
                    chunk.emit(OpCode.CMP, "==", expr.line)
            elif expr.verb == "GET_FIELD":
                self._compile_verb_expr(expr.operands[0])
                chunk.emit(OpCode.FIELD_GET, expr.callee, expr.line)
            elif expr.verb == "ADD":
                self._compile_verb_expr(expr.operands[0])
                self._compile_verb_expr(expr.operands[1])
                chunk.emit(OpCode.ADD, None, expr.line)
            elif expr.verb == "SUBTRACT":
                self._compile_verb_expr(expr.operands[0])
                self._compile_verb_expr(expr.operands[1])
                chunk.emit(OpCode.SUB, None, expr.line)
            elif expr.verb == "MULTIPLY":
                self._compile_verb_expr(expr.operands[0])
                self._compile_verb_expr(expr.operands[1])
                chunk.emit(OpCode.MUL, None, expr.line)
            elif expr.verb == "DIVIDE":
                self._compile_verb_expr(expr.operands[0])
                self._compile_verb_expr(expr.operands[1])
                chunk.emit(OpCode.DIV, None, expr.line)
            elif expr.verb == "MODULO":
                self._compile_verb_expr(expr.operands[0])
                self._compile_verb_expr(expr.operands[1])
                chunk.emit(OpCode.REM, None, expr.line)
            elif expr.verb == "POWER":
                self._compile_verb_expr(expr.operands[0])
                self._compile_verb_expr(expr.operands[1])
                chunk.emit(OpCode.POW_INT, None, expr.line)

        elif isinstance(expr, TuplePack):
            for el in expr.elements:
                self._compile_verb_expr(el)

        elif isinstance(expr, TakeEmpty):
            chunk.emit(OpCode.EMPTY, None, expr.line)

        elif isinstance(expr, FieldLookup):
            self._compile_verb_expr(expr.record)
            chunk.emit(OpCode.FIELD_GET, expr.field, expr.line)

        elif isinstance(expr, PostfixCalc):
            for step in expr.steps:
                if isinstance(step, VerbExpr):
                    self._compile_verb_expr(step)
                elif isinstance(step, str):
                    if step == "add":
                        chunk.emit(OpCode.ADD, None, expr.line)
                    elif step == "subtract":
                        chunk.emit(OpCode.SUB, None, expr.line)
                    elif step == "multiply":
                        chunk.emit(OpCode.MUL, None, expr.line)
                    elif step == "divide":
                        chunk.emit(OpCode.DIV, None, expr.line)
                    elif step == "floor":
                        chunk.emit(OpCode.FLOOR, None, expr.line)
                    elif step == "ceil":
                        chunk.emit(OpCode.CEIL, None, expr.line)
                    elif step == "nearest":
                        chunk.emit(OpCode.NEAREST, None, expr.line)
                    elif step == "absolute":
                        chunk.emit(OpCode.ABS, None, expr.line)
                    elif step == "lesser":
                        chunk.emit(OpCode.CMP, "<", expr.line)
                    elif step == "greater":
                        chunk.emit(OpCode.CMP, ">", expr.line)
                    elif step == "equal":
                        chunk.emit(OpCode.CMP, "==", expr.line)
                    elif step == "not-equal":
                        chunk.emit(OpCode.CMP, "!=", expr.line)
                    elif step in ("take", "shu", "šu", "𒋗"):
                        chunk.emit(OpCode.ENTRY_TAKE, None, expr.line)

        elif isinstance(expr, TakeTabletEntry):
            self._compile_verb_expr(expr.tablet)
            self._compile_verb_expr(expr.key)
            chunk.emit(OpCode.ENTRY_TAKE, None, expr.line)

        elif isinstance(expr, SeekTabletEntry):
            self._compile_verb_expr(expr.tablet)
            self._compile_verb_expr(expr.target)
            chunk.emit(OpCode.ENTRY_SEEK, expr.mode, expr.line)

        elif isinstance(expr, InspectTabletHistory):
            self._compile_verb_expr(expr.tablet)
            chunk.emit(OpCode.TABLET_HISTORY, None, expr.line)

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

        elif isinstance(stmt, ConsultTablet):
            self._compile_expression(stmt.tablet_name)
            if stmt.version:
                self._compile_expression(stmt.version)
                chunk.emit(OpCode.CONSULT, (True, stmt.alias), stmt.line)
            else:
                chunk.emit(OpCode.CONSULT, (False, stmt.alias), stmt.line)

        elif isinstance(stmt, CreateWorkingTablet):
            chunk.emit(OpCode.WORKING_CREATE, (stmt.name, stmt.shape), stmt.line)

        elif isinstance(stmt, CopyTablet):
            has_source = False
            if stmt.source:
                self._compile_expression(stmt.source)
                has_source = True
            has_version = False
            if stmt.version:
                self._compile_expression(stmt.version)
                has_version = True
            chunk.emit(OpCode.TABLET_COPY, (stmt.target, has_source, has_version), stmt.line)

        elif isinstance(stmt, DeriveTablet):
            has_source = False
            if stmt.source:
                self._compile_expression(stmt.source)
                has_source = True
            has_version = False
            if stmt.version:
                self._compile_expression(stmt.version)
                has_version = True
            chunk.emit(OpCode.TABLET_DERIVE, (stmt.target, has_source, has_version), stmt.line)

        elif isinstance(stmt, InscribeTablet):
            self._compile_expression(stmt.target_name)
            chunk.emit(OpCode.TABLET_INSCRIBE, stmt.working_name, stmt.line)

        elif isinstance(stmt, PutEntry):
            if stmt.key is not None:
                self._compile_expression(stmt.key)
            else:
                chunk.emit(OpCode.EMPTY, None, stmt.line)
            self._compile_expression(stmt.value)
            chunk.emit(OpCode.WORKING_PUT, stmt.working_name, stmt.line)

        elif isinstance(stmt, ReplaceEntry):
            self._compile_expression(stmt.key)
            self._compile_expression(stmt.value)
            chunk.emit(OpCode.WORKING_REPLACE, stmt.working_name, stmt.line)

        elif isinstance(stmt, RemoveEntry):
            self._compile_expression(stmt.key)
            chunk.emit(OpCode.WORKING_REMOVE, stmt.working_name, stmt.line)

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

        elif isinstance(expr, TakeEntry):
            self._compile_expression(expr.tablet)
            self._compile_expression(expr.key)
            chunk.emit(OpCode.ENTRY_TAKE, None, expr.line)

        elif isinstance(expr, SeekEntry):
            self._compile_expression(expr.tablet)
            self._compile_expression(expr.target)
            chunk.emit(OpCode.ENTRY_SEEK, expr.mode, expr.line)

        elif isinstance(expr, TabletHistory):
            self._compile_expression(expr.tablet)
            chunk.emit(OpCode.TABLET_HISTORY, None, expr.line)

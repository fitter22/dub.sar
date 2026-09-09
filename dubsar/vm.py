"""DUB.SAR 1.0 — Virtual Machine (Stage 2).

Implements Section 22:
- Operand stack, call stack, environment stack
- Exact rational mathematical execution with units
- Execution of bytecode lowered from DUB.SAR tablets
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Union

from dubsar.builtins import BUILTINS
from dubsar.errors import (
    DubSarDivisionByZero,
    DubSarInputError,
    DubSarNameError,
    DubSarRangeError,
    DubSarReturnError,
    DubSarUnitError,
)
from dubsar.interpreter import Environment
from dubsar.ir import BytecodeChunk, CompiledTablet, Instruction, OpCode
from dubsar.numbers import Rational, parse_number
from dubsar.units import (
    DIMENSIONLESS,
    UNIT_TABLE,
    Quantity,
    Unit,
    lookup_unit,
    to_quantity,
)


from dubsar.values import DeterminationValue, EmptySentinel


class CallFrame:
    """A call frame on the VM call stack."""

    __slots__ = ("chunk", "ip", "env")

    def __init__(self, chunk: BytecodeChunk, env: Environment, ip: int = 0) -> None:
        self.chunk = chunk
        self.env = env
        self.ip = ip


class VirtualMachine:
    """Stack-based Virtual Machine executing DUB.SAR bytecode."""

    def __init__(
        self,
        input_fn: Optional[Callable[[str], str]] = None,
        output_fn: Optional[Callable[[str], None]] = None,
        format_mode: str = "canonical",
    ) -> None:
        self.input_fn = input_fn if input_fn is not None else input
        self.output_fn = output_fn if output_fn is not None else print
        self.format_mode = format_mode
        self.operand_stack: List[Any] = []
        self.call_stack: List[CallFrame] = []
        self.global_env = Environment(name="tablet")
        self.outputs: List[str] = []

    def execute(self, tablet: CompiledTablet) -> List[str]:
        """Executes a compiled tablet and returns emitted output lines."""
        self.operand_stack.clear()
        self.call_stack.clear()
        self.outputs.clear()
        self.global_env = Environment(name="tablet")

        # Push main frame
        main_frame = CallFrame(tablet.main_chunk, self.global_env, 0)
        self.call_stack.append(main_frame)

        while self.call_stack:
            frame = self.call_stack[-1]
            if frame.ip >= len(frame.chunk.instructions):
                # End of current chunk
                self.call_stack.pop()
                continue

            instr = frame.chunk.instructions[frame.ip]
            frame.ip += 1

            op = instr.op
            arg = instr.arg

            if op == OpCode.CONST:
                self.operand_stack.append(arg)

            elif op == OpCode.LOAD:
                if frame.env.has(arg):
                    self.operand_stack.append(frame.env.get(arg))
                elif arg in UNIT_TABLE:
                    self.operand_stack.append(Quantity(1, UNIT_TABLE[arg]))
                else:
                    raise DubSarNameError(f"Undefined quantity or variable: '{arg}'", line=instr.line)

            elif op == OpCode.STORE:
                val = self.operand_stack.pop()
                frame.env.update(arg, val)

            elif op == OpCode.UNPACK:
                val = self.operand_stack.pop()
                target_names: List[str] = arg
                if not isinstance(val, (list, tuple)):
                    raise DubSarReturnError(
                        f"Expected {len(target_names)} values to unpack, got single value",
                        line=instr.line,
                    )
                if len(val) != len(target_names):
                    raise DubSarReturnError(
                        f"Target unpack mismatch: expected {len(target_names)}, got {len(val)}",
                        line=instr.line,
                    )
                for name, item in zip(target_names, val):
                    frame.env.update(name, item)

            elif op == OpCode.POP:
                if self.operand_stack:
                    self.operand_stack.pop()

            # Mathematical operators
            elif op == OpCode.ADD:
                b = to_quantity(self.operand_stack.pop())
                a = to_quantity(self.operand_stack.pop())
                self.operand_stack.append(a + b)

            elif op == OpCode.SUB:
                b = to_quantity(self.operand_stack.pop())
                a = to_quantity(self.operand_stack.pop())
                self.operand_stack.append(a - b)

            elif op == OpCode.MUL:
                b = to_quantity(self.operand_stack.pop())
                a = to_quantity(self.operand_stack.pop())
                self.operand_stack.append(a * b)

            elif op == OpCode.DIV:
                b = to_quantity(self.operand_stack.pop())
                a = to_quantity(self.operand_stack.pop())
                self.operand_stack.append(a / b)

            elif op == OpCode.REM:
                b = to_quantity(self.operand_stack.pop())
                a = to_quantity(self.operand_stack.pop())
                self.operand_stack.append(a % b)

            elif op == OpCode.POW_INT:
                b = to_quantity(self.operand_stack.pop())
                a = to_quantity(self.operand_stack.pop())
                if not b.value.is_integer:
                    raise DubSarUnitError(f"Power exponent must be an integer, got {b.value}", line=instr.line)
                self.operand_stack.append(a ** int(b.value.numerator))

            elif op == OpCode.CMP:
                b_raw = self.operand_stack.pop()
                a_raw = self.operand_stack.pop()
                cmp_op = arg
                if isinstance(b_raw, EmptySentinel):
                    if cmp_op in ("<", "<="):
                        res = True
                    elif cmp_op in (">", ">="):
                        res = False
                    elif cmp_op == "==":
                        res = False
                    elif cmp_op == "!=":
                        res = True
                    else:
                        res = True
                elif isinstance(a_raw, EmptySentinel):
                    if cmp_op in ("<", "<="):
                        res = False
                    elif cmp_op in (">", ">="):
                        res = True
                    elif cmp_op == "==":
                        res = False
                    elif cmp_op == "!=":
                        res = True
                    else:
                        res = False
                elif isinstance(a_raw, DeterminationValue) or isinstance(b_raw, DeterminationValue):
                    if cmp_op == "==":
                        res = (isinstance(a_raw, DeterminationValue) and a_raw.is_empty and isinstance(b_raw, DeterminationValue) and b_raw.is_empty)
                    elif cmp_op == "!=":
                        res = not (isinstance(a_raw, DeterminationValue) and a_raw.is_empty and isinstance(b_raw, DeterminationValue) and b_raw.is_empty)
                    else:
                        res = False
                else:
                    b = to_quantity(b_raw)
                    a = to_quantity(a_raw)
                    if cmp_op == "==":
                        res = (a == b)
                    elif cmp_op == "!=":
                        res = (a != b)
                    elif cmp_op == "<":
                        res = (a < b)
                    elif cmp_op == "<=":
                        res = (a <= b)
                    elif cmp_op == ">":
                        res = (a > b)
                    elif cmp_op == ">=":
                        res = (a >= b)
                    else:
                        raise DubSarUnitError(f"Unknown comparison operator: {cmp_op}")
                self.operand_stack.append(res)

            elif op == OpCode.EMPTY:
                self.operand_stack.append(DeterminationValue({}))

            elif op == OpCode.DETERMINE:
                name, fields = arg
                popped = [self.operand_stack.pop() for _ in range(len(fields))]
                popped.reverse()
                vals = {fname: v for fname, v in zip(fields, popped)}
                det = DeterminationValue(vals)
                frame.env.update(name, det)

            elif op == OpCode.FIELD_GET:
                rec = self.operand_stack.pop()
                field_name = arg
                if isinstance(rec, DeterminationValue):
                    self.operand_stack.append(rec.get(field_name))
                else:
                    self.operand_stack.append(rec)

            elif op == OpCode.RETAIN:
                cand_name, target_name = arg
                cond = self.operand_stack.pop()
                target_val = frame.env.get(target_name) if frame.env.has(target_name) else DeterminationValue({})
                if bool(cond) or (isinstance(target_val, DeterminationValue) and target_val.is_empty):
                    cand_val = frame.env.get(cand_name)
                    if isinstance(cand_val, DeterminationValue):
                        frame.env.update(target_name, cand_val.clone())
                    else:
                        frame.env.update(target_name, cand_val)

            elif op == OpCode.NOT:
                a = self.operand_stack.pop()
                self.operand_stack.append(not bool(a))

            elif op == OpCode.NEG:
                a = to_quantity(self.operand_stack.pop())
                self.operand_stack.append(-a)

            # Control flow
            elif op == OpCode.JUMP:
                frame.ip = arg

            elif op == OpCode.JUMP_IF_FALSE:
                cond = self.operand_stack.pop()
                if not bool(cond):
                    frame.ip = arg

            # Math built-ins
            elif op == OpCode.FLOOR:
                a = to_quantity(self.operand_stack.pop())
                self.operand_stack.append(a.floor())

            elif op == OpCode.CEIL:
                a = to_quantity(self.operand_stack.pop())
                self.operand_stack.append(a.ceil())

            elif op == OpCode.NEAREST:
                a = to_quantity(self.operand_stack.pop())
                self.operand_stack.append(a.nearest())

            elif op == OpCode.ABS:
                a = to_quantity(self.operand_stack.pop())
                self.operand_stack.append(abs(a))

            # Procedures and Calls
            elif op == OpCode.CALL:
                callee, argc = arg
                # Pop arguments in reverse
                args = []
                for _ in range(argc):
                    args.append(self.operand_stack.pop())
                args.reverse()

                if callee in BUILTINS:
                    res = BUILTINS[callee](*args)
                    self.operand_stack.append(res)
                elif callee in tablet.procedures:
                    proc_chunk = tablet.procedures[callee]
                    proc_env = Environment(parent=self.global_env, name=f"proc:{callee}")
                    for param_name, val in zip(proc_chunk.parameters, args):
                        proc_env.set(param_name, val)
                    new_frame = CallFrame(proc_chunk, proc_env, 0)
                    self.call_stack.append(new_frame)
                else:
                    raise DubSarNameError(f"Undefined procedure: '{callee}'", line=instr.line)

            elif op == OpCode.RETURN:
                count = arg
                ret_vals = []
                for _ in range(count):
                    ret_vals.append(self.operand_stack.pop())
                ret_vals.reverse()

                # Pop current frame
                self.call_stack.pop()
                if not self.call_stack:
                    # Returned from main
                    break

                # Push return values onto caller stack
                if count == 1:
                    self.operand_stack.append(ret_vals[0])
                else:
                    self.operand_stack.append(ret_vals)

            elif op == OpCode.INPUT:
                prompt = self.operand_stack.pop()
                raw_input = self.input_fn(str(prompt)).strip()
                try:
                    parts = raw_input.split()
                    if len(parts) >= 2:
                        num_part = parts[0]
                        unit_part = " ".join(parts[1:])
                        rat = parse_number(num_part)
                        u = lookup_unit(unit_part)
                        self.operand_stack.append(Quantity(rat, u))
                    else:
                        rat = parse_number(raw_input)
                        unit_to_use = DIMENSIONLESS
                        prompt_lower = str(prompt).lower()
                        if "in days" in prompt_lower or "in day" in prompt_lower or "in 𒌓" in str(prompt):
                            unit_to_use = lookup_unit("day")
                        elif "in hours" in prompt_lower or "in hour" in prompt_lower:
                            unit_to_use = lookup_unit("hour")
                        elif "in minutes" in prompt_lower or "in minute" in prompt_lower:
                            unit_to_use = lookup_unit("minute")
                        elif "in seconds" in prompt_lower or "in second" in prompt_lower:
                            unit_to_use = lookup_unit("second")
                        elif "in months" in prompt_lower or "in month" in prompt_lower or "in 𒌗" in str(prompt):
                            unit_to_use = lookup_unit("month")
                        elif "in years" in prompt_lower or "in year" in prompt_lower or "in 𒈬" in str(prompt):
                            unit_to_use = lookup_unit("year")
                        self.operand_stack.append(Quantity(rat, unit_to_use))
                except Exception as e:
                    raise DubSarInputError(f"Invalid numeric input '{raw_input}': {e}", line=instr.line)

            elif op == OpCode.OUTPUT:
                val = self.operand_stack.pop()
                if isinstance(val, DeterminationValue):
                    for line in val.format_lines(format_mode=self.format_mode):
                        self.outputs.append(line)
                        self.output_fn(line)
                else:
                    if isinstance(val, bool):
                        out_str = "1" if val else "0"
                    elif isinstance(val, str):
                        out_str = val
                    elif isinstance(val, Quantity):
                        out_str = val.format(format_mode=self.format_mode)
                    elif isinstance(val, Rational):
                        out_str = val.format_canonical()
                    else:
                        out_str = str(val)
                    self.outputs.append(out_str)
                    self.output_fn(out_str)

            elif op == OpCode.HALT:
                break

        return self.outputs

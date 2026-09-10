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
    DubSarEntryNotFoundError,
    DubSarImmutableTabletError,
    DubSarInputError,
    DubSarNameError,
    DubSarRangeError,
    DubSarReturnError,
    DubSarUnitError,
    DubSarInvalidTabletError,
    DubSarInvalidEntryError,
    DubSarTabletNotFoundError,
    DubSarConsultationError,
)
from dubsar.archive.archive import SQLiteTabletArchive, TabletArchive
from dubsar.archive.models import (
    TabletReference,
    TabletShape,
    TabletVersionInfo,
)
from dubsar.archive.working import WorkingTablet
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
        archive: Optional[TabletArchive] = None,
    ) -> None:
        self.input_fn = input_fn if input_fn is not None else input
        self.output_fn = output_fn if output_fn is not None else print
        self.format_mode = format_mode
        self.operand_stack: List[Any] = []
        self.call_stack: List[CallFrame] = []
        self.iter_stack: List[List[Any]] = []
        self.global_env = Environment(name="tablet")
        self.outputs: List[str] = []
        self.archive = archive or SQLiteTabletArchive(":memory:")
        self.working_tablets: Dict[str, WorkingTablet] = {}
        self.consulted_tablets: Dict[str, TabletVersionInfo] = {}

    def _resolve_tablet(self, tab: Any, line: int) -> Any:
        if isinstance(tab, str):
            if tab in self.working_tablets:
                return self.working_tablets[tab]
            if tab in self.consulted_tablets:
                return self.consulted_tablets[tab]
            if self.call_stack and self.call_stack[-1].env.has(tab):
                val = self.call_stack[-1].env.get(tab)
                if isinstance(val, (WorkingTablet, TabletVersionInfo, TabletReference)):
                    return val
            try:
                info = self.archive.consult(tab)
                self.consulted_tablets[tab] = info
                return info
            except Exception:
                raise DubSarTabletNotFoundError(f"Tablet '{tab}' not found in archive", line=line)
        if isinstance(tab, (WorkingTablet, TabletVersionInfo, TabletReference)):
            return tab
        raise DubSarInvalidTabletError(f"Object {tab!r} is not a valid tablet", line=line)

    def _resolve_working_tablet(self, tab: Any, line: int) -> WorkingTablet:
        if isinstance(tab, str):
            if tab in self.working_tablets:
                return self.working_tablets[tab]
            if tab in self.consulted_tablets:
                raise DubSarImmutableTabletError(f"Cannot mutate persistent tablet '{tab}' (§57)", line=line)
            if self.call_stack and self.call_stack[-1].env.has(tab):
                val = self.call_stack[-1].env.get(tab)
                if isinstance(val, (TabletVersionInfo, TabletReference)):
                    raise DubSarImmutableTabletError(f"Cannot mutate persistent tablet '{tab}' (§57)", line=line)
                if isinstance(val, WorkingTablet):
                    return val
            try:
                _ = self.archive.consult(tab)
                raise DubSarImmutableTabletError(f"Cannot mutate persistent tablet '{tab}' (§57)", line=line)
            except DubSarImmutableTabletError:
                raise
            except Exception:
                pass
            raise DubSarInvalidTabletError(f"Working tablet '{tab}' not found", line=line)
        if isinstance(tab, (TabletVersionInfo, TabletReference)):
            raise DubSarImmutableTabletError(f"Cannot mutate persistent tablet '{getattr(tab, 'name', tab)}' (§57)", line=line)
        if isinstance(tab, WorkingTablet):
            return tab
        raise DubSarInvalidTabletError(f"Object {tab!r} is not a working tablet", line=line)

    def _eval_take(self, tab: Any, key_val: Any, line: int) -> Any:
        tab_obj = self._resolve_tablet(tab, line)
        if isinstance(tab_obj, (WorkingTablet, TabletVersionInfo)):
            res = tab_obj.get(key_val)
            if res is None:
                raise DubSarEntryNotFoundError(f"Entry {key_val!r} not found in tablet '{tab_obj.name}'", line=line)
            return res
        elif isinstance(tab_obj, TabletReference):
            info = self.archive.consult(tab_obj.name, version=tab_obj.version)
            res = info.get(key_val)
            if res is None:
                raise DubSarEntryNotFoundError(f"Entry {key_val!r} not found in tablet '{tab_obj.name}'", line=line)
            return res
        raise DubSarInvalidTabletError(f"Object {tab_obj!r} is not a valid tablet", line=line)

    def _eval_seek(self, tab: Any, target_val: Any, mode: str = "nearest", line: int = 0) -> Any:
        tab_obj = self._resolve_tablet(tab, line)
        entry = None
        if isinstance(tab_obj, (WorkingTablet, TabletVersionInfo)):
            if mode == "first":
                entry = tab_obj.first()
            elif mode == "last":
                entry = tab_obj.last()
            else:
                entry = tab_obj.seek_nearest(target_val)
            if entry is None:
                raise DubSarEntryNotFoundError(f"No entry found in tablet '{tab_obj.name}' for {mode}", line=line)
            return entry[1]
        elif isinstance(tab_obj, TabletReference):
            info = self.archive.consult(tab_obj.name, version=tab_obj.version)
            if mode == "first":
                entry = info.first()
            elif mode == "last":
                entry = info.last()
            else:
                entry = info.seek_nearest(target_val)
            if entry is None:
                raise DubSarEntryNotFoundError(f"No entry found in tablet '{tab_obj.name}' for {mode}", line=line)
            return entry[1]
        raise DubSarInvalidTabletError(f"Object {tab_obj!r} is not a valid tablet", line=line)

    def execute(self, tablet: CompiledTablet) -> List[str]:
        """Executes a compiled tablet and returns emitted output lines."""
        self.operand_stack.clear()
        self.call_stack.clear()
        self.iter_stack.clear()
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
                elif arg in self.working_tablets:
                    self.operand_stack.append(self.working_tablets[arg])
                elif arg in self.consulted_tablets:
                    self.operand_stack.append(self.consulted_tablets[arg])
                elif arg in UNIT_TABLE:
                    self.operand_stack.append(Quantity(1, UNIT_TABLE[arg]))
                else:
                    try:
                        info = self.archive.consult(arg)
                        self.consulted_tablets[arg] = info
                        self.operand_stack.append(info)
                    except Exception:
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
                elif isinstance(val, (WorkingTablet, TabletVersionInfo)):
                    out_str = f'tablet "{val.name}" v{getattr(val, "version", 1)}'
                    self.outputs.append(out_str)
                    self.output_fn(out_str)
                elif isinstance(val, list) and all(isinstance(x, TabletVersionInfo) for x in val):
                    for v in val:
                        out_str = f'version {v.version}: checksum={v.checksum[:8]} created_by={v.created_by}'
                        self.outputs.append(out_str)
                        self.output_fn(out_str)
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

            elif op == OpCode.CONSULT:
                has_version, alias = arg
                v_num = int(to_quantity(self.operand_stack.pop()).value.numerator) if has_version else None
                name_pop = self.operand_stack.pop()
                if isinstance(name_pop, (TabletVersionInfo, WorkingTablet)):
                    name_val = name_pop.name
                else:
                    name_val = str(name_pop)
                info = self.archive.consult(name_val, version=v_num)
                target_alias = alias or name_val
                self.consulted_tablets[target_alias] = info
                frame.env.update(target_alias, info)

            elif op == OpCode.WORKING_CREATE:
                if len(arg) == 3:
                    name, shape_str, has_len = arg
                    length_val = int(to_quantity(self.operand_stack.pop()).value.numerator) if has_len else None
                else:
                    name, shape_str = arg
                    length_val = None
                shape = TabletShape(shape_str) if shape_str in ("table", "scalar", "sequence", "structured", "text") else TabletShape.TABLE
                wt = self.archive.create_working(name, shape=shape)
                if length_val is not None:
                    wt.shape = TabletShape.SEQUENCE
                self.working_tablets[name] = wt
                frame.env.update(name, wt)

            elif op == OpCode.TABLET_COPY:
                target, has_source, has_version = arg
                v_num = int(to_quantity(self.operand_stack.pop()).value.numerator) if has_version else None
                if has_source:
                    source = str(self.operand_stack.pop())
                else:
                    if not self.consulted_tablets:
                        raise DubSarConsultationError("No consulted tablet available to copy", line=instr.line)
                    source = list(self.consulted_tablets.values())[-1].name
                wt = self.archive.copy(source, target_name=target, version=v_num)
                self.working_tablets[target] = wt
                frame.env.update(target, wt)

            elif op == OpCode.TABLET_DERIVE:
                target, has_source, has_version = arg
                v_num = int(to_quantity(self.operand_stack.pop()).value.numerator) if has_version else None
                if has_source:
                    source = str(self.operand_stack.pop())
                else:
                    if not self.consulted_tablets:
                        raise DubSarConsultationError("No consulted tablet available to derive from", line=instr.line)
                    source = list(self.consulted_tablets.values())[-1].name
                wt = self.archive.derive(source, target_name=target, version=v_num)
                self.working_tablets[target] = wt
                frame.env.update(target, wt)

            elif op == OpCode.TABLET_INSCRIBE:
                working_name = arg
                target_pop = self.operand_stack.pop()
                if isinstance(target_pop, (TabletVersionInfo, WorkingTablet)):
                    target_name = target_pop.name
                else:
                    target_name = str(target_pop)
                wt = self.working_tablets.get(working_name)
                if wt is None and frame.env.has(working_name):
                    wt = frame.env.get(working_name)
                if not isinstance(wt, WorkingTablet):
                    raise DubSarInvalidTabletError(f"'{working_name}' is not a working tablet", line=instr.line)
                new_info = self.archive.inscribe(wt, target_name=target_name)
                self.consulted_tablets[target_name] = new_info
                frame.env.update(target_name, new_info)

            elif op == OpCode.WORKING_PUT:
                working_name = arg
                val = self.operand_stack.pop()
                k = self.operand_stack.pop()
                wt = self._resolve_working_tablet(working_name, instr.line)
                if k is None or isinstance(k, EmptySentinel) or (isinstance(k, DeterminationValue) and k.is_empty) or k == "":
                    if isinstance(val, DeterminationValue):
                        for f_k, f_v in val.fields.items():
                            wt.put(f_k, f_v)
                    elif isinstance(val, dict):
                        for f_k, f_v in val.items():
                            wt.put(f_k, f_v)
                    else:
                        wt.put(getattr(val, "name", "value"), val)
                else:
                    wt.put(k, val)

            elif op == OpCode.WORKING_PUT_STACK:
                val = self.operand_stack.pop()
                k = self.operand_stack.pop()
                tab = self.operand_stack.pop()
                wt = self._resolve_working_tablet(tab, instr.line)
                wt.put(k, val)

            elif op == OpCode.WORKING_APPEND:
                working_name = arg
                val = self.operand_stack.pop()
                wt = self._resolve_working_tablet(working_name, instr.line)
                wt.append(val)

            elif op == OpCode.WORKING_APPEND_STACK:
                val = self.operand_stack.pop()
                tab = self.operand_stack.pop()
                wt = self._resolve_working_tablet(tab, instr.line)
                next_k = wt.append(val)
                self.operand_stack.append(Quantity(next_k, DIMENSIONLESS))

            elif op == OpCode.WORKING_REPLACE:
                working_name = arg
                val = self.operand_stack.pop()
                k = self.operand_stack.pop()
                wt = self._resolve_working_tablet(working_name, instr.line)
                wt.replace(k, val)

            elif op == OpCode.WORKING_REMOVE:
                working_name = arg
                k = self.operand_stack.pop()
                wt = self._resolve_working_tablet(working_name, instr.line)
                wt.remove(k)

            elif op == OpCode.WORKING_REMOVE_STACK:
                k = self.operand_stack.pop()
                tab = self.operand_stack.pop()
                wt = self._resolve_working_tablet(tab, instr.line)
                wt.remove(k)

            elif op == OpCode.ENTRY_TAKE:
                key_val = self.operand_stack.pop()
                tab = self.operand_stack.pop()
                self.operand_stack.append(self._eval_take(tab, key_val, instr.line))

            elif op == OpCode.ENTRY_SEEK:
                mode = arg or "nearest"
                if mode in ("first", "last"):
                    tab = self.operand_stack.pop()
                    self.operand_stack.append(self._eval_seek(tab, None, mode=mode, line=instr.line))
                else:
                    target_val = self.operand_stack.pop()
                    tab = self.operand_stack.pop()
                    self.operand_stack.append(self._eval_seek(tab, target_val, mode=mode, line=instr.line))

            elif op == OpCode.TABLET_HISTORY:
                tab = self.operand_stack.pop()
                name = getattr(tab, "name", str(tab))
                self.operand_stack.append(self.archive.history(name))

            elif op == OpCode.SEQUENCE_LENGTH:
                tab = self.operand_stack.pop()
                tab_obj = self._resolve_tablet(tab, instr.line)
                if hasattr(tab_obj, "length"):
                    ln = tab_obj.length()
                elif hasattr(tab_obj, "entries"):
                    ln = len(tab_obj.entries)
                else:
                    ln = len(tab_obj)
                self.operand_stack.append(Quantity(Rational(ln), DIMENSIONLESS))

            elif op == OpCode.ITER_START:
                tab = self.operand_stack.pop()
                tab_obj = self._resolve_tablet(tab, instr.line)
                if isinstance(tab_obj, (WorkingTablet, TabletVersionInfo)):
                    entries = tab_obj.items()
                elif isinstance(tab_obj, TabletReference):
                    info = self.archive.consult(tab_obj.name, version=tab_obj.version)
                    entries = info.items()
                elif hasattr(tab_obj, "entries"):
                    if isinstance(tab_obj.entries, dict):
                        entries = list(tab_obj.entries.items())
                    elif isinstance(tab_obj.entries, list):
                        entries = list(tab_obj.entries)
                    else:
                        entries = []
                else:
                    entries = []
                self.iter_stack.append([entries, 0])

            elif op == OpCode.ITER_NEXT:
                key_var, val_var, exit_addr = arg
                iter_info = self.iter_stack[-1]
                entries, idx = iter_info
                if idx >= len(entries):
                    frame.ip = exit_addr
                else:
                    k, v = entries[idx]
                    iter_info[1] = idx + 1
                    if key_var:
                        k_val = Quantity(k, DIMENSIONLESS) if isinstance(k, (int, Rational)) else k
                        frame.env.update(key_var, k_val)
                    frame.env.update(val_var, v)
                    if val_var == "entry":
                        frame.env.update("v", v)

            elif op == OpCode.ITER_END:
                if self.iter_stack:
                    self.iter_stack.pop()

            elif op == OpCode.HALT:
                break

        return self.outputs

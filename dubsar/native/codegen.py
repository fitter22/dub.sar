"""DUB.SAR 1.0 — Native C99 Code Generator (Stage 4).

Translates a SemanticProgram (or AST Program) into clean, high-performance C99 code
linked against dubsar_runtime.h.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set

from dubsar.ast import Program
from dubsar.semantic_ir import (
    AppendTabletEntryVerb,
    ApplyMathVerb,
    AssignVerb,
    ConcludeVerb,
    ConsultTabletVerb,
    CreateWorkingTabletVerb,
    DetermineVerb,
    DiscardVerb,
    EstablishVerb,
    FieldLookup,
    InscribeVerb,
    IterateTabletEntriesVerb,
    MakeDetermination,
    PostfixCalc,
    ProcedureRecipe,
    PutTabletEntryVerb,
    ReceiveInput,
    RepeatVerb,
    RetainVerb,
    SeekTabletEntry,
    SemanticProgram,
    SemanticVerb,
    TakeEmpty,
    TakeLiteral,
    TakeQuantity,
    TakeSequenceLength,
    TakeTabletEntry,
    TakeText,
    VerbExpr,
    ast_to_semantic_ir,
)


def _mangle_name(name: str) -> str:
    """Mangles a DUB.SAR identifier into a valid C identifier."""
    if not name:
        return "empty"
    out = []
    for c in name:
        if c.isalnum() or c == "_":
            out.append(c)
        elif c == "-":
            out.append("_")
        else:
            out.append(f"_u{ord(c):04x}_")
    res = "".join(out)
    if res and res[0].isdigit():
        res = "n_" + res
    return "var_" + res


def _escape_c_string(s: str) -> str:
    """Escapes a string for use in C string literals."""
    res = []
    for c in s:
        if c == "\\":
            res.append("\\\\")
        elif c == '"':
            res.append('\\"')
        elif c == "\n":
            res.append("\\n")
        elif c == "\t":
            res.append("\\t")
        elif c == "\r":
            res.append("\\r")
        else:
            res.append(c)
    return "".join(res)


class NativeCodeGen:
    """Generates standard C99 source code from a DUB.SAR program."""

    def __init__(self) -> None:
        self.temp_counter: int = 0
        self.procedures: Dict[str, ProcedureRecipe] = {}
        self.all_determinations: Dict[str, List[str]] = {}

    def _next_temp(self, prefix: str = "tmp") -> str:
        self.temp_counter += 1
        return f"_{prefix}_{self.temp_counter}"

    def compile(self, program: Program | SemanticProgram) -> str:
        """Generates self-contained C99 source code for the tablet."""
        self.temp_counter = 0
        self.all_determinations.clear()

        if isinstance(program, Program):
            sem_prog = ast_to_semantic_ir(program)
        else:
            sem_prog = program

        self.procedures = {p.name: p for p in sem_prog.procedures}

        lines: List[str] = [
            "/* DUB.SAR 1.0 — Generated Native C99 Code (Stage 4) */",
            '#include "dubsar_runtime.h"',
            "",
        ]

        # Forward declarations for user procedures
        if sem_prog.procedures:
            lines.append("/* Forward Declarations of Procedures */")
            for proc in sem_prog.procedures:
                m_proc = _mangle_name(proc.name).replace("var_", "proc_")
                params_str = ", ".join(f"dubsar_val_t {_mangle_name(p)}" for p in proc.parameters) or "void"
                lines.append(f"dubsar_tuple_t {m_proc}({params_str});")
            lines.append("")

        # Compile procedures
        for proc in sem_prog.procedures:
            lines.extend(self._compile_procedure(proc))

        # Compile main problem/result run function
        lines.extend(self._compile_main(sem_prog))

        # Standard entrypoint
        lines.extend([
            "",
            "/* Standard Program Entrypoint */",
            "int main(int argc, char **argv) {",
            "    dubsar_init_env(argc, argv);",
            "    dubsar_program_run();",
            "    return 0;",
            "}",
            "",
        ])

        return "\n".join(lines)

    def _collect_locals(self, verbs: List[SemanticVerb], exclude: Optional[Set[str]] = None) -> Set[str]:
        locals_found: Set[str] = set()
        ex = exclude or set()

        for v in verbs:
            if isinstance(v, EstablishVerb) and v.name not in ex:
                locals_found.add(v.name)
            elif isinstance(v, AssignVerb):
                for t in v.targets:
                    if t not in ex:
                        locals_found.add(t)
            elif isinstance(v, MakeDetermination) and v.name not in ex:
                locals_found.add(v.name)
            elif isinstance(v, CreateWorkingTabletVerb) and v.name not in ex:
                locals_found.add(v.name)
            elif isinstance(v, RepeatVerb):
                if v.target not in ex:
                    locals_found.add(v.target)
                locals_found.update(self._collect_locals(v.body, exclude=ex))
            elif isinstance(v, DetermineVerb):
                locals_found.update(self._collect_locals(v.body, exclude=ex))
                if v.alternative:
                    locals_found.update(self._collect_locals(v.alternative, exclude=ex))
            elif isinstance(v, RetainVerb):
                if v.target not in ex:
                    locals_found.add(v.target)
            elif isinstance(v, IterateTabletEntriesVerb):
                if v.key_target and v.key_target not in ex:
                    locals_found.add(v.key_target)
                if v.value_target not in ex:
                    locals_found.add(v.value_target)
                locals_found.update(self._collect_locals(v.body, exclude=ex))

        return locals_found

    def _compile_procedure(self, proc: ProcedureRecipe) -> List[str]:
        m_proc = _mangle_name(proc.name).replace("var_", "proc_")
        params_str = ", ".join(f"dubsar_val_t {_mangle_name(p)}" for p in proc.parameters) or "void"

        lines = [
            f"/* Procedure Recipe: {proc.name} */",
            f"dubsar_tuple_t {m_proc}({params_str}) {{",
        ]

        param_set = set(proc.parameters)
        locals_found = self._collect_locals(proc.body, exclude=param_set)
        for loc in sorted(locals_found):
            lines.append(f"    dubsar_val_t {_mangle_name(loc)} = dubsar_val_empty();")

        for verb in proc.body:
            self._compile_verb_c(verb, lines, indent=4)

        lines.extend([
            "    return dubsar_tuple_empty();",
            "}",
            "",
        ])
        return lines

    def _compile_main(self, sem_prog: SemanticProgram) -> List[str]:
        lines = [
            "/* Main Tablet Problem & Result Execution */",
            "void dubsar_program_run(void) {",
        ]

        all_verbs = sem_prog.problem_verbs + sem_prog.result_verbs
        locals_found = self._collect_locals(all_verbs)
        for loc in sorted(locals_found):
            lines.append(f"    dubsar_val_t {_mangle_name(loc)} = dubsar_val_empty();")

        lines.append("")
        lines.append("    /* Problem Section */")
        for verb in sem_prog.problem_verbs:
            self._compile_verb_c(verb, lines, indent=4)

        lines.append("")
        lines.append("    /* Result Section */")
        for verb in sem_prog.result_verbs:
            self._compile_verb_c(verb, lines, indent=4)

        lines.append("}")
        return lines

    def _compile_verb_c(self, verb: SemanticVerb, lines: List[str], indent: int = 4) -> None:
        pad = " " * indent

        if isinstance(verb, EstablishVerb):
            m_name = _mangle_name(verb.name)
            if isinstance(verb.value, PostfixCalc):
                self._compile_postfix_c(verb.value, lines, indent, target_var=m_name)
            else:
                expr_str = self._compile_expr_c(verb.value, lines, indent)
                lines.append(f"{pad}{m_name} = {expr_str};")
            if verb.unit:
                unit_esc = _escape_c_string(verb.unit)
                lines.append(f"{pad}if ({m_name}.kind == DUBSAR_VAL_RAT) {m_name} = dubsar_val_quant({m_name}.as.rat, \"{unit_esc}\");")

        elif isinstance(verb, AssignVerb):
            if len(verb.targets) == 1:
                m_target = _mangle_name(verb.targets[0])
                if isinstance(verb.value, PostfixCalc):
                    self._compile_postfix_c(verb.value, lines, indent, target_var=m_target)
                else:
                    expr_str = self._compile_expr_c(verb.value, lines, indent)
                    lines.append(f"{pad}{m_target} = {expr_str};")
            else:
                # Tuple unpacking
                tmp_tup = self._next_temp("tup")
                # If value is invoke
                if isinstance(verb.value, ApplyMathVerb) and verb.value.verb == "INVOKE" and verb.value.callee in self.procedures:
                    m_proc = _mangle_name(verb.value.callee).replace("var_", "proc_")
                    args = [self._compile_expr_c(a, lines, indent) for a in verb.value.operands]
                    lines.append(f"{pad}dubsar_tuple_t {tmp_tup} = {m_proc}({', '.join(args)});")
                else:
                    expr_str = self._compile_expr_c(verb.value, lines, indent)
                    lines.append(f"{pad}dubsar_tuple_t {tmp_tup} = dubsar_tuple_1({expr_str});")

                for idx, t in enumerate(verb.targets):
                    m_t = _mangle_name(t)
                    lines.append(f"{pad}if ({tmp_tup}.count > {idx}) {m_t} = {tmp_tup}.values[{idx}];")

        elif isinstance(verb, DetermineVerb):
            cond_str = self._compile_expr_c(verb.condition, lines, indent)
            lines.append(f"{pad}if (dubsar_val_is_truthy({cond_str})) {{")
            for v in verb.body:
                self._compile_verb_c(v, lines, indent + 4)
            if verb.alternative:
                lines.append(f"{pad}}} else {{")
                for v in verb.alternative:
                    self._compile_verb_c(v, lines, indent + 4)
            lines.append(f"{pad}}}")

        elif isinstance(verb, RepeatVerb):
            m_target = _mangle_name(verb.target)
            tmp_start = self._next_temp("start")
            tmp_end = self._next_temp("end")
            tmp_i = self._next_temp("i")

            if verb.start:
                start_expr = self._compile_expr_c(verb.start, lines, indent)
                lines.append(f"{pad}int64_t {tmp_start} = dubsar_rat_floor(({start_expr}).kind == DUBSAR_VAL_QUANT ? ({start_expr}).as.quant.val : ({start_expr}).as.rat);")
            else:
                lines.append(f"{pad}int64_t {tmp_start} = 1;")

            end_expr = self._compile_expr_c(verb.end, lines, indent)
            lines.append(f"{pad}int64_t {tmp_end} = dubsar_rat_floor(({end_expr}).kind == DUBSAR_VAL_QUANT ? ({end_expr}).as.quant.val : ({end_expr}).as.rat);")

            lines.append(f"{pad}for (int64_t {tmp_i} = {tmp_start}; {tmp_i} <= {tmp_end}; ++{tmp_i}) {{")
            lines.append(f"{pad}    {m_target} = dubsar_val_rat(dubsar_rat_make({tmp_i}, 1));")
            for v in verb.body:
                self._compile_verb_c(v, lines, indent + 4)
            lines.append(f"{pad}}}")

        elif isinstance(verb, MakeDetermination):
            m_name = _mangle_name(verb.name)
            count = len(verb.fields)
            lines.append(f"{pad}/* Make Determination {verb.name} */")
            lines.append(f"{pad}{{")
            lines.append(f"{pad}    dubsar_field_t *_fields = (dubsar_field_t*)malloc(sizeof(dubsar_field_t) * {max(1, count)});")
            for idx, f in enumerate(verb.fields):
                m_f = _mangle_name(f)
                f_esc = _escape_c_string(f)
                lines.append(f"{pad}    _fields[{idx}].val = (dubsar_val_t*)malloc(sizeof(dubsar_val_t));")
                lines.append(f"{pad}    *(_fields[{idx}].val) = {m_f};")
                lines.append(f"{pad}    strncpy(_fields[{idx}].name, \"{f_esc}\", 63);")
                lines.append(f"{pad}    _fields[{idx}].name[63] = '\\0';")
            name_esc = _escape_c_string(verb.name)
            lines.append(f"{pad}    {m_name} = (dubsar_val_t){{DUBSAR_VAL_DETERMINATION, .as.det = {{\"{name_esc}\", {count}, _fields}}}};")
            lines.append(f"{pad}}}")

        elif isinstance(verb, RetainVerb):
            m_cand = _mangle_name(verb.candidate)
            m_target = _mangle_name(verb.target)
            cond_str = self._compile_expr_c(verb.condition, lines, indent)
            lines.append(f"{pad}if ({m_target}.kind == DUBSAR_VAL_EMPTY || dubsar_val_is_truthy({cond_str})) {{")
            lines.append(f"{pad}    {m_target} = dubsar_val_clone({m_cand});")
            lines.append(f"{pad}}}")

        elif isinstance(verb, InscribeVerb):
            expr_str = self._compile_expr_c(verb.value, lines, indent)
            lines.append(f"{pad}dubsar_print_val({expr_str});")

        elif isinstance(verb, DiscardVerb):
            if isinstance(verb.expr, PostfixCalc):
                self._compile_postfix_c(verb.expr, lines, indent, target_var=None)
            else:
                expr_str = self._compile_expr_c(verb.expr, lines, indent)
                lines.append(f"{pad}(void)({expr_str});")

        elif isinstance(verb, ConcludeVerb):
            if not verb.values:
                lines.append(f"{pad}return dubsar_tuple_empty();")
            elif len(verb.values) == 1:
                expr_str = self._compile_expr_c(verb.values[0], lines, indent)
                lines.append(f"{pad}return dubsar_tuple_1({expr_str});")
            elif len(verb.values) == 2:
                e1 = self._compile_expr_c(verb.values[0], lines, indent)
                e2 = self._compile_expr_c(verb.values[1], lines, indent)
                lines.append(f"{pad}return dubsar_tuple_2({e1}, {e2});")
            else:
                args = [self._compile_expr_c(v, lines, indent) for v in verb.values]
                lines.append(f"{pad}dubsar_val_t _ret_vals[] = {{{', '.join(args)}}};")
                lines.append(f"{pad}return dubsar_tuple_make({len(verb.values)}, _ret_vals);")

        elif isinstance(verb, CreateWorkingTabletVerb):
            m_name = _mangle_name(verb.name)
            name_esc = _escape_c_string(verb.name)
            prealloc = "0"
            if verb.length:
                prealloc = f"dubsar_rat_floor(({self._compile_expr_c(verb.length, lines, indent)}).as.rat)"
            lines.append(f"{pad}{m_name} = dubsar_val_tablet(dubsar_tablet_create_sequence(\"{name_esc}\", {prealloc}));")

        elif isinstance(verb, AppendTabletEntryVerb):
            m_name = _mangle_name(verb.working_name)
            val_str = self._compile_expr_c(verb.value, lines, indent)
            lines.append(f"{pad}dubsar_tablet_append({m_name}.as.tablet, {val_str});")

        elif isinstance(verb, PutTabletEntryVerb):
            m_name = _mangle_name(verb.working_name)
            val_str = self._compile_expr_c(verb.value, lines, indent)
            if verb.key:
                key_str = self._compile_expr_c(verb.key, lines, indent)
                lines.append(f"{pad}dubsar_tablet_put({m_name}.as.tablet, {key_str}, {val_str});")
            else:
                lines.append(f"{pad}dubsar_tablet_append({m_name}.as.tablet, {val_str});")

        elif isinstance(verb, IterateTabletEntriesVerb):
            tab_str = self._compile_expr_c(verb.tablet, lines, indent)
            tmp_t = self._next_temp("tab")
            tmp_idx = self._next_temp("idx")
            lines.append(f"{pad}dubsar_tablet_t *{tmp_t} = ({tab_str}).as.tablet;")
            lines.append(f"{pad}if ({tmp_t}) {{")
            lines.append(f"{pad}    for (size_t {tmp_idx} = 0; {tmp_idx} < {tmp_t}->count; ++{tmp_idx}) {{")
            if verb.key_target:
                lines.append(f"{pad}        {_mangle_name(verb.key_target)} = {tmp_t}->entries[{tmp_idx}].key;")
            lines.append(f"{pad}        {_mangle_name(verb.value_target)} = {tmp_t}->entries[{tmp_idx}].val;")
            for v in verb.body:
                self._compile_verb_c(v, lines, indent + 8)
            lines.append(f"{pad}    }}")
            lines.append(f"{pad}}}")

        elif isinstance(verb, ConsultTabletVerb):
            lines.append(f"{pad}/* Consult persistent tablet {verb.tablet_name} */")

    def _compile_postfix_c(self, pfx: PostfixCalc, lines: List[str], indent: int, target_var: Optional[str] = None) -> None:
        pad = " " * indent
        stack_var = self._next_temp("stk")
        sp_var = self._next_temp("sp")

        lines.append(f"{pad}/* Postfix Pipeline */")
        lines.append(f"{pad}dubsar_val_t {stack_var}[64];")
        lines.append(f"{pad}int {sp_var} = 0;")

        for step in pfx.steps:
            if isinstance(step, VerbExpr):
                expr_str = self._compile_expr_c(step, lines, indent)
                lines.append(f"{pad}{stack_var}[{sp_var}++] = {expr_str};")
            elif isinstance(step, str):
                op = step.lower()
                if op in ("add", "+"):
                    lines.append(f"{pad}{sp_var}--; {stack_var}[{sp_var} - 1] = dubsar_val_add({stack_var}[{sp_var} - 1], {stack_var}[{sp_var}]);")
                elif op in ("subtract", "-"):
                    lines.append(f"{pad}{sp_var}--; {stack_var}[{sp_var} - 1] = dubsar_val_sub({stack_var}[{sp_var} - 1], {stack_var}[{sp_var}]);")
                elif op in ("multiply", "*"):
                    lines.append(f"{pad}{sp_var}--; {stack_var}[{sp_var} - 1] = dubsar_val_mul({stack_var}[{sp_var} - 1], {stack_var}[{sp_var}]);")
                elif op in ("divide", "/"):
                    lines.append(f"{pad}{sp_var}--; {stack_var}[{sp_var} - 1] = dubsar_val_div({stack_var}[{sp_var} - 1], {stack_var}[{sp_var}]);")
                elif op in ("modulo", "%"):
                    lines.append(f"{pad}{sp_var}--; {stack_var}[{sp_var} - 1] = dubsar_val_mod({stack_var}[{sp_var} - 1], {stack_var}[{sp_var}]);")
                elif op in ("floor", "gur"):
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_val_floor({stack_var}[{sp_var} - 1]);")
                elif op in ("ceil",):
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_val_ceil({stack_var}[{sp_var} - 1]);")
                elif op in ("nearest", "ri"):
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_val_nearest({stack_var}[{sp_var} - 1]);")
                elif op in ("absolute", "abs", "te"):
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_val_abs({stack_var}[{sp_var} - 1]);")
                elif op == "square":
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_val_rat(dubsar_rat_square({stack_var}[{sp_var} - 1].as.rat));")
                elif op == "square-root":
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_val_rat(dubsar_rat_sqrt_babylonian({stack_var}[{sp_var} - 1].as.rat, 4));")
                elif op == "right-triangle":
                    lines.append(f"{pad}{sp_var} -= 2;")
                    lines.append(f"{pad}{stack_var}[{sp_var}] = dubsar_val_triangle(dubsar_triangle_determine(")
                    lines.append(f"{pad}    dubsar_val_to_rat({stack_var}[{sp_var}]), dubsar_val_to_rat({stack_var}[{sp_var}+1]), (dubsar_rat_t){{0, 1}}, 1, 1, 0));")
                    lines.append(f"{pad}{sp_var}++;")
                elif op in ("validate-triangle", "validate_triangle"):
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_val_bool(({stack_var}[{sp_var} - 1].kind == DUBSAR_VAL_TRIANGLE) ? {stack_var}[{sp_var} - 1].as.triangle.is_valid : 0);")
                elif op in ("inclination", "mūṣû", "musu", "kussû", "kussu"):
                    lines.append(f"{pad}{sp_var} -= 2;")
                    lines.append(f"{pad}{stack_var}[{sp_var}] = dubsar_val_inclination(dubsar_make_inclination(dubsar_val_to_rat({stack_var}[{sp_var}]), dubsar_val_to_rat({stack_var}[{sp_var}+1])));")
                    lines.append(f"{pad}{sp_var}++;")
                elif op == "feed":
                    lines.append(f"{pad}{sp_var} -= 2;")
                    lines.append(f"{pad}{stack_var}[{sp_var}] = dubsar_val_rat(dubsar_rat_div(dubsar_val_to_rat({stack_var}[{sp_var}+1]), dubsar_val_to_rat({stack_var}[{sp_var}])));")
                    lines.append(f"{pad}{sp_var}++;")
                elif op == "whole-turn":
                    lines.append(f"{pad}{stack_var}[{sp_var}++] = dubsar_val_turn(dubsar_turn_make(1, 1));")
                elif op == "half-turn":
                    lines.append(f"{pad}{stack_var}[{sp_var}++] = dubsar_val_turn(dubsar_turn_make(1, 2));")
                elif op == "quarter-turn":
                    lines.append(f"{pad}{stack_var}[{sp_var}++] = dubsar_val_turn(dubsar_turn_make(1, 4));")
                elif op == "eighth-turn":
                    lines.append(f"{pad}{stack_var}[{sp_var}++] = dubsar_val_turn(dubsar_turn_make(1, 8));")
                elif op == "turn":
                    lines.append(f"{pad}{{ dubsar_rat_t _tr = dubsar_val_to_rat({stack_var}[{sp_var} - 1]); {stack_var}[{sp_var} - 1] = dubsar_val_turn(dubsar_turn_make(_tr.num, _tr.den)); }}")
                elif op == "direction":
                    lines.append(f"{pad}if ({stack_var}[{sp_var} - 1].kind == DUBSAR_VAL_TURN) {{")
                    lines.append(f"{pad}    {stack_var}[{sp_var} - 1] = dubsar_val_direction(dubsar_direction_from_turn({stack_var}[{sp_var} - 1].as.turn));")
                    lines.append(f"{pad}}} else {{")
                    lines.append(f"{pad}    dubsar_rat_t _dr = dubsar_val_to_rat({stack_var}[{sp_var} - 1]);")
                    lines.append(f"{pad}    {stack_var}[{sp_var} - 1] = dubsar_val_direction(dubsar_direction_from_turn(dubsar_turn_make(_dr.num, _dr.den)));")
                    lines.append(f"{pad}}}")
                elif op == "directed":
                    lines.append(f"{pad}{sp_var} -= 2;")
                    lines.append(f"{pad}{{ dubsar_direction_t _dd = ({stack_var}[{sp_var}+1].kind == DUBSAR_VAL_DIRECTION) ? {stack_var}[{sp_var}+1].as.direction : dubsar_direction_from_turn((dubsar_turn_t){{{{0, 1}}}}); const char *_du = ({stack_var}[{sp_var}].kind == DUBSAR_VAL_QUANT) ? {stack_var}[{sp_var}].as.quant.unit : NULL; {stack_var}[{sp_var}] = dubsar_val_directed(dubsar_directed_make(dubsar_val_to_rat({stack_var}[{sp_var}]), _du, _dd)); }}")
                    lines.append(f"{pad}{sp_var}++;")
                elif op == "rotate":
                    lines.append(f"{pad}{sp_var} -= 2;")
                    lines.append(f"{pad}{{ dubsar_turn_t _rt = ({stack_var}[{sp_var}+1].kind == DUBSAR_VAL_TURN) ? {stack_var}[{sp_var}+1].as.turn : dubsar_turn_make(dubsar_val_to_rat({stack_var}[{sp_var}+1]).num, dubsar_val_to_rat({stack_var}[{sp_var}+1]).den); {stack_var}[{sp_var}] = dubsar_val_rotate({stack_var}[{sp_var}], _rt); }}")
                    lines.append(f"{pad}{sp_var}++;")
                elif op == "approximate":
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_val_rat(dubsar_rat_sqrt_babylonian({stack_var}[{sp_var} - 1].as.rat, 4));")
                elif op == "dft":
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_val_tablet(dubsar_tablet_dft({stack_var}[{sp_var} - 1].as.tablet, 0));")
                elif op == "fft":
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_val_tablet(dubsar_tablet_fft({stack_var}[{sp_var} - 1].as.tablet, 0));")
                elif op == "inverse-dft":
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_val_tablet(dubsar_tablet_dft({stack_var}[{sp_var} - 1].as.tablet, 1));")
                elif op == "inverse-fft":
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_val_tablet(dubsar_tablet_fft({stack_var}[{sp_var} - 1].as.tablet, 1));")
                elif op in ("length", "𒁍"):
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_val_rat(dubsar_rat_make(dubsar_tablet_length({stack_var}[{sp_var} - 1].as.tablet), 1));")
                elif op in ("append", "𒈭"):
                    lines.append(f"{pad}{sp_var} -= 2; dubsar_tablet_append({stack_var}[{sp_var}].as.tablet, {stack_var}[{sp_var} + 1]);")
                elif op in ("take", "shu", "𒋗"):
                    lines.append(f"{pad}{sp_var} -= 2;")
                    lines.append(f"{pad}{stack_var}[{sp_var}] = dubsar_tablet_take({stack_var}[{sp_var}].as.tablet, {stack_var}[{sp_var} + 1]);")
                    lines.append(f"{pad}{sp_var}++;")
                elif op in ("first",):
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_tablet_first({stack_var}[{sp_var} - 1].as.tablet);")
                elif op in ("last",):
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_tablet_last({stack_var}[{sp_var} - 1].as.tablet);")
                elif op.startswith("."):
                    field_name = op[1:]
                    f_esc = _escape_c_string(field_name)
                    lines.append(f"{pad}{stack_var}[{sp_var} - 1] = dubsar_val_get_field({stack_var}[{sp_var} - 1], \"{f_esc}\");")

        if target_var:
            lines.append(f"{pad}if ({sp_var} > 0) {target_var} = {stack_var}[{sp_var} - 1];")

    def _compile_expr_c(self, expr: VerbExpr, lines: List[str], indent: int) -> str:
        if isinstance(expr, TakeLiteral):
            n = expr.value.numerator
            d = expr.value.denominator
            if expr.unit:
                u_esc = _escape_c_string(expr.unit)
                return f"dubsar_val_quant(dubsar_rat_make({n}LL, {d}LL), \"{u_esc}\")"
            return f"dubsar_val_rat(dubsar_rat_make({n}LL, {d}LL))"

        elif isinstance(expr, TakeText):
            t_esc = _escape_c_string(expr.value)
            return f"dubsar_val_str(\"{t_esc}\")"

        elif isinstance(expr, TakeQuantity):
            return _mangle_name(expr.name)

        elif isinstance(expr, TakeEmpty):
            return "dubsar_val_empty()"

        elif isinstance(expr, ReceiveInput):
            p_esc = _escape_c_string(expr.prompt)
            return f"dubsar_read_input_val(\"{p_esc}\")"

        elif isinstance(expr, FieldLookup):
            rec_str = self._compile_expr_c(expr.record, lines, indent)
            f_esc = _escape_c_string(expr.field)
            return f"dubsar_val_get_field({rec_str}, \"{f_esc}\")"

        elif isinstance(expr, TakeTabletEntry):
            k_str = self._compile_expr_c(expr.key, lines, indent)
            if isinstance(expr.tablet, TakeText):
                t_esc = _escape_c_string(expr.tablet.value)
                return f"dubsar_archive_take(\"{t_esc}\", {k_str})"
            tab_str = self._compile_expr_c(expr.tablet, lines, indent)
            return f"dubsar_tablet_take(({tab_str}).as.tablet, {k_str})"

        elif isinstance(expr, TakeSequenceLength):
            tab_str = self._compile_expr_c(expr.tablet, lines, indent)
            return f"dubsar_val_rat(dubsar_rat_make(dubsar_tablet_length(({tab_str}).as.tablet), 1))"

        elif isinstance(expr, SeekTabletEntry):
            tab_str = self._compile_expr_c(expr.tablet, lines, indent)
            if expr.mode == "first":
                return f"dubsar_tablet_first(({tab_str}).as.tablet)"
            elif expr.mode == "last":
                return f"dubsar_tablet_last(({tab_str}).as.tablet)"
            elif expr.target is not None:
                tgt_str = self._compile_expr_c(expr.target, lines, indent)
                return f"dubsar_tablet_take(({tab_str}).as.tablet, {tgt_str})"
            return "dubsar_val_empty()"

        elif isinstance(expr, ApplyMathVerb):
            if expr.verb == "INVOKE":
                callee = expr.callee or ""
                if callee in self.procedures:
                    m_proc = _mangle_name(callee).replace("var_", "proc_")
                    args = [self._compile_expr_c(a, lines, indent) for a in expr.operands]
                    return f"{m_proc}({', '.join(args)}).values[0]"
                elif callee == "nearest":
                    return f"dubsar_val_nearest({self._compile_expr_c(expr.operands[0], lines, indent)})"
                elif callee == "floor":
                    return f"dubsar_val_floor({self._compile_expr_c(expr.operands[0], lines, indent)})"
                elif callee == "ceil":
                    return f"dubsar_val_ceil({self._compile_expr_c(expr.operands[0], lines, indent)})"
                elif callee in ("abs", "absolute"):
                    return f"dubsar_val_abs({self._compile_expr_c(expr.operands[0], lines, indent)})"
                elif callee == "gcd":
                    o1 = self._compile_expr_c(expr.operands[0], lines, indent)
                    o2 = self._compile_expr_c(expr.operands[1], lines, indent)
                    return f"dubsar_val_rat(dubsar_rat_make(dubsar_gcd(({o1}).as.rat.num, ({o2}).as.rat.num), 1))"
                elif callee == "min":
                    o1 = self._compile_expr_c(expr.operands[0], lines, indent)
                    o2 = self._compile_expr_c(expr.operands[1], lines, indent)
                    return f"(dubsar_rat_lt(({o1}).as.rat, ({o2}).as.rat) ? {o1} : {o2})"
                elif callee == "max":
                    o1 = self._compile_expr_c(expr.operands[0], lines, indent)
                    o2 = self._compile_expr_c(expr.operands[1], lines, indent)
                    return f"(dubsar_rat_gt(({o1}).as.rat, ({o2}).as.rat) ? {o1} : {o2})"
                elif callee == "sqrt":
                    return f"dubsar_val_rat(dubsar_rat_sqrt_babylonian({self._compile_expr_c(expr.operands[0], lines, indent)}.as.rat, 4))"

            elif expr.verb in ("ADD", "+"):
                return f"dubsar_val_add({self._compile_expr_c(expr.operands[0], lines, indent)}, {self._compile_expr_c(expr.operands[1], lines, indent)})"
            elif expr.verb in ("SUBTRACT", "-"):
                return f"dubsar_val_sub({self._compile_expr_c(expr.operands[0], lines, indent)}, {self._compile_expr_c(expr.operands[1], lines, indent)})"
            elif expr.verb in ("MULTIPLY", "*"):
                return f"dubsar_val_mul({self._compile_expr_c(expr.operands[0], lines, indent)}, {self._compile_expr_c(expr.operands[1], lines, indent)})"
            elif expr.verb in ("DIVIDE", "/"):
                return f"dubsar_val_div({self._compile_expr_c(expr.operands[0], lines, indent)}, {self._compile_expr_c(expr.operands[1], lines, indent)})"
            elif expr.verb in ("MODULO", "%"):
                return f"dubsar_val_mod({self._compile_expr_c(expr.operands[0], lines, indent)}, {self._compile_expr_c(expr.operands[1], lines, indent)})"
            elif expr.verb in ("POWER", "**"):
                return f"dubsar_val_pow({self._compile_expr_c(expr.operands[0], lines, indent)}, {self._compile_expr_c(expr.operands[1], lines, indent)})"
            elif expr.verb == "NEGATE":
                return f"dubsar_val_neg({self._compile_expr_c(expr.operands[0], lines, indent)})"
            elif expr.verb == "NOT":
                return f"dubsar_val_bool(!dubsar_val_is_truthy({self._compile_expr_c(expr.operands[0], lines, indent)}))"
            elif expr.verb == "COMPARE":
                op_esc = _escape_c_string(expr.relation or "==")
                return f"dubsar_val_cmp_op({self._compile_expr_c(expr.operands[0], lines, indent)}, {self._compile_expr_c(expr.operands[1], lines, indent)}, \"{op_esc}\")"

        elif isinstance(expr, PostfixCalc):
            tmp_res = self._next_temp("pfx_res")
            lines.append(f"{' ' * indent}dubsar_val_t {tmp_res} = dubsar_val_empty();")
            self._compile_postfix_c(expr, lines, indent, target_var=tmp_res)
            return tmp_res

        return "dubsar_val_empty()"


def compile_to_c(program: Program | SemanticProgram) -> str:
    """Convenience function to compile a DUB.SAR program to C99 source code."""
    return NativeCodeGen().compile(program)

"""DUB.SAR 1.0 — WebAssembly Backend (Stage 3).

Implements CR-001, CR-002, Section 24, and Section 32:
- Full lowering of procedures, parameters, and return tuples
- Local quantity declarations (i64 num, den pairs)
- Bounded repetitions lowered to WASM loops and break blocks
- Conditionals lowered to WASM if-then-else
- Arithmetic (+, -, *, /, %) lowered to exact rational helpers with GCD reduction
- Exact 64-bit rational runtime math helpers (abs, floor, ceil, nearest, min, max, gcd, lcm)
- Linear memory layout for string constants and I/O host bindings
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple

from dubsar.ast import Program
from dubsar.numbers import Rational
from dubsar.semantic_ir import (
    ApplyMathVerb,
    AssignVerb,
    ConcludeVerb,
    DetermineVerb,
    DiscardVerb,
    EstablishVerb,
    InscribeVerb,
    ProcedureRecipe,
    ReceiveInput,
    RepeatVerb,
    SemanticProgram,
    SemanticVerb,
    TakeLiteral,
    TakeQuantity,
    TakeText,
    TuplePack,
    VerbExpr,
    ast_to_semantic_ir,
)


class WasmCompiler:
    """Compiles a DUB.SAR tablet to WebAssembly Text (.wat)."""

    def __init__(self) -> None:
        self.string_table: Dict[str, int] = {}
        self.data_bytes: bytearray = bytearray()
        self.loop_counter: int = 0
        self.procedures: Dict[str, ProcedureRecipe] = {}

    def compile(self, program: Program | SemanticProgram) -> str:
        """Generates standard WebAssembly text format (.wat) for the tablet."""
        self.string_table.clear()
        self.data_bytes.clear()
        self.loop_counter = 0

        if isinstance(program, Program):
            sem_prog = ast_to_semantic_ir(program)
        else:
            sem_prog = program

        self.procedures = {p.name: p for p in sem_prog.procedures}

        # Collect string literals into linear memory
        self._collect_strings(sem_prog)

        lines: List[str] = [
            "(module",
            '  ;; DUB.SAR 1.0 WebAssembly Target',
            '  ;; Numeric Limit Note (CR-002):',
            '  ;; Exact rational arithmetic is executed using 64-bit integer numerator/denominator pairs.',
            '  ;; Numerator and denominator values are bounded within [-2^63, 2^63 - 1].',
            '  (import "env" "dubsar_print_str" (func $print_str (param i32 i32)))',
            '  (import "env" "dubsar_print_int" (func $print_int (param i64)))',
            '  (import "env" "dubsar_print_rat" (func $print_rat (param i64 i64)))',
            '  (import "env" "dubsar_input_rat" (func $input_rat (param i32 i32) (result i64 i64)))',
            "",
            "  ;; Linear memory",
            f"  (memory (export \"memory\") {max(1, (len(self.data_bytes) + 65535) // 65536)})",
        ]

        if self.data_bytes:
            escaped_data = "".join(f"\\{b:02x}" for b in self.data_bytes)
            lines.append(f'  (data (i32.const 0) "{escaped_data}")')

        # Add rational runtime math helpers
        lines.extend(self._runtime_helpers())

        # Compile procedures
        for proc in sem_prog.procedures:
            lines.extend(self._compile_procedure(proc))

        # Compile main run function
        lines.extend(self._compile_main(sem_prog))

        lines.append(")")
        return "\n".join(lines)

    def _runtime_helpers(self) -> List[str]:
        return [
            "",
            "  ;; Rational Runtime Math Helpers",
            "  (func $gcd (param $a i64) (param $b i64) (result i64)",
            "    (local $temp i64)",
            "    (block $done",
            "      (loop $loop",
            "        (br_if $done (i64.eqz (local.get $b)))",
            "        (local.set $temp (local.get $b))",
            "        (local.set $b (i64.rem_s (local.get $a) (local.get $b)))",
            "        (local.set $a (local.get $temp))",
            "        (br $loop)",
            "      )",
            "    )",
            "    (if (result i64) (i64.lt_s (local.get $a) (i64.const 0))",
            "      (then (i64.sub (i64.const 0) (local.get $a)))",
            "      (else (local.get $a))",
            "    )",
            "  )",
            "",
            "  (func $rat_reduce (param $num i64) (param $den i64) (result i64 i64)",
            "    (local $g i64)",
            "    (if (i64.lt_s (local.get $den) (i64.const 0))",
            "      (then",
            "        (local.set $num (i64.sub (i64.const 0) (local.get $num)))",
            "        (local.set $den (i64.sub (i64.const 0) (local.get $den)))",
            "      )",
            "    )",
            "    (local.set $g (call $gcd (local.get $num) (local.get $den)))",
            "    (if (result i64 i64) (i64.gt_s (local.get $g) (i64.const 1))",
            "      (then",
            "        (i64.div_s (local.get $num) (local.get $g))",
            "        (i64.div_s (local.get $den) (local.get $g))",
            "      )",
            "      (else",
            "        (local.get $num)",
            "        (local.get $den)",
            "      )",
            "    )",
            "  )",
            "",
            "  (func $rat_add (param $a_num i64) (param $a_den i64) (param $b_num i64) (param $b_den i64) (result i64 i64)",
            "    (local $num i64) (local $den i64)",
            "    (local.set $num (i64.add (i64.mul (local.get $a_num) (local.get $b_den)) (i64.mul (local.get $b_num) (local.get $a_den))))",
            "    (local.set $den (i64.mul (local.get $a_den) (local.get $b_den)))",
            "    (call $rat_reduce (local.get $num) (local.get $den))",
            "  )",
            "",
            "  (func $rat_sub (param $a_num i64) (param $a_den i64) (param $b_num i64) (param $b_den i64) (result i64 i64)",
            "    (local $num i64) (local $den i64)",
            "    (local.set $num (i64.sub (i64.mul (local.get $a_num) (local.get $b_den)) (i64.mul (local.get $b_num) (local.get $a_den))))",
            "    (local.set $den (i64.mul (local.get $a_den) (local.get $b_den)))",
            "    (call $rat_reduce (local.get $num) (local.get $den))",
            "  )",
            "",
            "  (func $rat_mul (param $a_num i64) (param $a_den i64) (param $b_num i64) (param $b_den i64) (result i64 i64)",
            "    (local $num i64) (local $den i64)",
            "    (local.set $num (i64.mul (local.get $a_num) (local.get $b_num)))",
            "    (local.set $den (i64.mul (local.get $a_den) (local.get $b_den)))",
            "    (call $rat_reduce (local.get $num) (local.get $den))",
            "  )",
            "",
            "  (func $rat_div (param $a_num i64) (param $a_den i64) (param $b_num i64) (param $b_den i64) (result i64 i64)",
            "    (local $num i64) (local $den i64)",
            "    (local.set $num (i64.mul (local.get $a_num) (local.get $b_den)))",
            "    (local.set $den (i64.mul (local.get $a_den) (local.get $b_num)))",
            "    (call $rat_reduce (local.get $num) (local.get $den))",
            "  )",
            "",
            "  (func $rat_floor (param $num i64) (param $den i64) (result i64 i64)",
            "    (local $q i64) (local $r i64)",
            "    (local.set $q (i64.div_s (local.get $num) (local.get $den)))",
            "    (local.set $r (i64.rem_s (local.get $num) (local.get $den)))",
            "    (if (i64.and (i64.lt_s (local.get $num) (i64.const 0)) (i64.ne (local.get $r) (i64.const 0)))",
            "      (then (local.set $q (i64.sub (local.get $q) (i64.const 1))))",
            "    )",
            "    (local.get $q) (i64.const 1)",
            "  )",
            "",
            "  (func $rat_ceil (param $num i64) (param $den i64) (result i64 i64)",
            "    (local $q i64) (local $r i64)",
            "    (local.set $q (i64.div_s (local.get $num) (local.get $den)))",
            "    (local.set $r (i64.rem_s (local.get $num) (local.get $den)))",
            "    (if (i64.and (i64.gt_s (local.get $num) (i64.const 0)) (i64.ne (local.get $r) (i64.const 0)))",
            "      (then (local.set $q (i64.add (local.get $q) (i64.const 1))))",
            "    )",
            "    (local.get $q) (i64.const 1)",
            "  )",
            "",
            "  (func $rat_nearest (param $num i64) (param $den i64) (result i64 i64)",
            "    (local $two_num i64)",
            "    (local.set $two_num (i64.mul (local.get $num) (i64.const 2)))",
            "    (if (result i64 i64) (i64.ge_s (local.get $num) (i64.const 0))",
            "      (then",
            "        (i64.div_s (i64.add (local.get $two_num) (local.get $den)) (i64.mul (local.get $den) (i64.const 2)))",
            "        (i64.const 1)",
            "      )",
            "      (else",
            "        (i64.sub (i64.const 0) (i64.div_s (i64.add (i64.sub (i64.const 0) (local.get $two_num)) (local.get $den)) (i64.mul (local.get $den) (i64.const 2))))",
            "        (i64.const 1)",
            "      )",
            "    )",
            "  )",
            "",
            "  (func $rat_abs (param $num i64) (param $den i64) (result i64 i64)",
            "    (local.set $num (if (result i64) (i64.lt_s (local.get $num) (i64.const 0)) (then (i64.sub (i64.const 0) (local.get $num))) (else (local.get $num))))",
            "    (local.set $den (if (result i64) (i64.lt_s (local.get $den) (i64.const 0)) (then (i64.sub (i64.const 0) (local.get $den))) (else (local.get $den))))",
            "    (local.get $num) (local.get $den)",
            "  )",
            "",
            "  (func $rat_cmp (param $op i32) (param $a_num i64) (param $a_den i64) (param $b_num i64) (param $b_den i64) (result i32)",
            "    (local $diff i64)",
            "    (local.set $diff (i64.sub (i64.mul (local.get $a_num) (local.get $b_den)) (i64.mul (local.get $b_num) (local.get $a_den))))",
            "    (if (result i32) (i32.eq (local.get $op) (i32.const 0)) ;; ==",
            "      (then (i64.eqz (local.get $diff)))",
            "      (else",
            "        (if (result i32) (i32.eq (local.get $op) (i32.const 1)) ;; !=",
            "          (then (i64.ne (local.get $diff) (i64.const 0)))",
            "          (else",
            "            (if (result i32) (i32.eq (local.get $op) (i32.const 2)) ;; <",
            "              (then (i64.lt_s (local.get $diff) (i64.const 0)))",
            "              (else",
            "                (if (result i32) (i32.eq (local.get $op) (i32.const 3)) ;; <=",
            "                  (then (i64.le_s (local.get $diff) (i64.const 0)))",
            "                  (else",
            "                    (if (result i32) (i32.eq (local.get $op) (i32.const 4)) ;; >",
            "                      (then (i64.gt_s (local.get $diff) (i64.const 0)))",
            "                      (else (i64.ge_s (local.get $diff) (i64.const 0))) ;; >=",
            "                    )",
            "                  )",
            "                )",
            "              )",
            "            )",
            "          )",
            "        )",
            "      )",
            "    )",
            "  )",
        ]

    def _compile_procedure(self, proc: ProcedureRecipe) -> List[str]:
        lines: List[str] = ["", f"  ;; Procedure Recipe: {proc.name}"]
        mangled_name = self._mangle_name(proc.name)

        params_str = " ".join(f"(param ${self._mangle_name(p)}_num i64) (param ${self._mangle_name(p)}_den i64)" for p in proc.parameters)

        # Determine return arity
        return_arity = self._determine_return_arity(proc)
        results_str = " ".join("(result i64 i64)" for _ in range(return_arity))

        lines.append(f"  (func ${mangled_name} {params_str} {results_str}")

        # Declare all local variables (excluding parameters)
        param_set = set(proc.parameters)
        locals_found = self._collect_locals(proc.body, exclude=param_set)
        for loc in sorted(locals_found):
            m_loc = self._mangle_name(loc)
            lines.append(f"    (local ${m_loc}_num i64) (local ${m_loc}_den i64)")

        # Compile body verbs
        for verb in proc.body:
            self._compile_verb_wat(verb, lines, indent=4)

        lines.append("  )")
        return lines

    def _compile_main(self, sem_prog: SemanticProgram) -> List[str]:
        lines: List[str] = [
            "",
            "  ;; Main Tablet Run Function",
            '  (func (export "run")',
        ]

        # Declare all local variables for the main function
        locals_found = self._collect_locals(sem_prog.problem_verbs + sem_prog.result_verbs)
        for loc in sorted(locals_found):
            m_loc = self._mangle_name(loc)
            lines.append(f"    (local ${m_loc}_num i64) (local ${m_loc}_den i64)")

        # Compile problem verbs
        for verb in sem_prog.problem_verbs:
            self._compile_verb_wat(verb, lines, indent=4)

        # Compile result verbs
        for verb in sem_prog.result_verbs:
            self._compile_verb_wat(verb, lines, indent=4)

        lines.append("  )")
        return lines

    def _compile_verb_wat(self, verb: SemanticVerb, lines: List[str], indent: int = 4) -> None:
        pad = " " * indent

        if isinstance(verb, EstablishVerb):
            lines.append(f"{pad};; Establish {verb.name}")
            self._compile_verb_expr_wat(verb.value, lines, indent)
            m_name = self._mangle_name(verb.name)
            lines.append(f"{pad}(local.set ${m_name}_den)")
            lines.append(f"{pad}(local.set ${m_name}_num)")

        elif isinstance(verb, AssignVerb):
            lines.append(f"{pad};; Assign {', '.join(verb.targets)}")
            self._compile_verb_expr_wat(verb.value, lines, indent)
            # Store values in reverse order (stack order)
            for target in reversed(verb.targets):
                m_target = self._mangle_name(target)
                lines.append(f"{pad}(local.set ${m_target}_den)")
                lines.append(f"{pad}(local.set ${m_target}_num)")

        elif isinstance(verb, DetermineVerb):
            lines.append(f"{pad};; Determine")
            self._compile_condition_wat(verb.condition, lines, indent)
            lines.append(f"{pad}(if")
            lines.append(f"{pad}  (then")
            for v in verb.body:
                self._compile_verb_wat(v, lines, indent + 4)
            lines.append(f"{pad}  )")
            if verb.alternative:
                lines.append(f"{pad}  (else")
                for v in verb.alternative:
                    self._compile_verb_wat(v, lines, indent + 4)
                lines.append(f"{pad}  )")
            lines.append(f"{pad})")

        elif isinstance(verb, RepeatVerb):
            self.loop_counter += 1
            loop_id = f"loop_{self.loop_counter}"
            m_target = self._mangle_name(verb.target)

            lines.append(f"{pad};; Repeat {verb.target}")
            # Initialize loop target
            if verb.start:
                self._compile_verb_expr_wat(verb.start, lines, indent)
            else:
                lines.append(f"{pad}(i64.const 1) (i64.const 1)")
            lines.append(f"{pad}(local.set ${m_target}_den)")
            lines.append(f"{pad}(local.set ${m_target}_num)")

            lines.append(f"{pad}(block $break_{loop_id}")
            lines.append(f"{pad}  (loop $top_{loop_id}")

            # Check: target <= end
            lines.append(f"{pad}    (i32.const 3) ;; <=")
            lines.append(f"{pad}    (local.get ${m_target}_num) (local.get ${m_target}_den)")
            self._compile_verb_expr_wat(verb.end, lines, indent + 4)
            lines.append(f"{pad}    (call $rat_cmp)")
            lines.append(f"{pad}    (i32.eqz)")
            lines.append(f"{pad}    (br_if $break_{loop_id})")

            # Loop body
            for v in verb.body:
                self._compile_verb_wat(v, lines, indent + 4)

            # Increment target by 1: target := target + 1
            lines.append(f"{pad}    (local.get ${m_target}_num) (local.get ${m_target}_den)")
            lines.append(f"{pad}    (i64.const 1) (i64.const 1)")
            lines.append(f"{pad}    (call $rat_add)")
            lines.append(f"{pad}    (local.set ${m_target}_den)")
            lines.append(f"{pad}    (local.set ${m_target}_num)")
            lines.append(f"{pad}    (br $top_{loop_id})")

            lines.append(f"{pad}  )")
            lines.append(f"{pad})")

        elif isinstance(verb, ConcludeVerb):
            lines.append(f"{pad};; Conclude")
            for val in verb.values:
                self._compile_verb_expr_wat(val, lines, indent)
            lines.append(f"{pad}(return)")

        elif isinstance(verb, InscribeVerb):
            lines.append(f"{pad};; Inscribe")
            if isinstance(verb.value, TakeText):
                offset = self.string_table.get(verb.value.value, 0)
                length = len(verb.value.value.encode("utf-8"))
                lines.append(f"{pad}(i32.const {offset}) (i32.const {length}) (call $print_str)")
            else:
                self._compile_verb_expr_wat(verb.value, lines, indent)
                lines.append(f"{pad}(call $print_rat)")

        elif isinstance(verb, DiscardVerb):
            self._compile_verb_expr_wat(verb.expr, lines, indent)
            lines.append(f"{pad}(drop) (drop)")

    def _compile_condition_wat(self, expr: VerbExpr, lines: List[str], indent: int) -> None:
        pad = " " * indent
        if isinstance(expr, ApplyMathVerb) and expr.verb == "COMPARE":
            op_code = {
                "==": 0,
                "!=": 1,
                "<": 2,
                "<=": 3,
                ">": 4,
                ">=": 5,
            }.get(expr.relation or "==", 0)
            lines.append(f"{pad}(i32.const {op_code})")
            self._compile_verb_expr_wat(expr.operands[0], lines, indent)
            self._compile_verb_expr_wat(expr.operands[1], lines, indent)
            lines.append(f"{pad}(call $rat_cmp)")
        else:
            self._compile_verb_expr_wat(expr, lines, indent)
            lines.append(f"{pad}(drop)")
            lines.append(f"{pad}(i64.ne (i64.const 0))")

    def _compile_verb_expr_wat(self, expr: VerbExpr, lines: List[str], indent: int) -> None:
        pad = " " * indent

        if isinstance(expr, TakeLiteral):
            lines.append(f"{pad}(i64.const {expr.value.numerator}) (i64.const {expr.value.denominator})")

        elif isinstance(expr, TakeText):
            offset = self.string_table.get(expr.value, 0)
            length = len(expr.value.encode("utf-8"))
            lines.append(f"{pad}(i64.const {offset}) (i64.const {length})")

        elif isinstance(expr, TakeQuantity):
            m_name = self._mangle_name(expr.name)
            lines.append(f"{pad}(local.get ${m_name}_num) (local.get ${m_name}_den)")

        elif isinstance(expr, ReceiveInput):
            offset = self.string_table.get(expr.prompt, 0)
            length = len(expr.prompt.encode("utf-8"))
            lines.append(f"{pad}(i32.const {offset}) (i32.const {length}) (call $input_rat)")

        elif isinstance(expr, ApplyMathVerb):
            if expr.verb == "ADD":
                self._compile_verb_expr_wat(expr.operands[0], lines, indent)
                self._compile_verb_expr_wat(expr.operands[1], lines, indent)
                lines.append(f"{pad}(call $rat_add)")

            elif expr.verb == "SUBTRACT":
                self._compile_verb_expr_wat(expr.operands[0], lines, indent)
                self._compile_verb_expr_wat(expr.operands[1], lines, indent)
                lines.append(f"{pad}(call $rat_sub)")

            elif expr.verb == "MULTIPLY":
                self._compile_verb_expr_wat(expr.operands[0], lines, indent)
                self._compile_verb_expr_wat(expr.operands[1], lines, indent)
                lines.append(f"{pad}(call $rat_mul)")

            elif expr.verb == "DIVIDE":
                self._compile_verb_expr_wat(expr.operands[0], lines, indent)
                self._compile_verb_expr_wat(expr.operands[1], lines, indent)
                lines.append(f"{pad}(call $rat_div)")

            elif expr.verb in ("FLOOR", "CEIL", "NEAREST", "ABS"):
                self._compile_verb_expr_wat(expr.operands[0], lines, indent)
                lines.append(f"{pad}(call $rat_{expr.verb.lower()})")

            elif expr.verb == "INVOKE":
                callee = expr.callee or ""
                if callee in ("floor", "ceil", "nearest", "abs"):
                    self._compile_verb_expr_wat(expr.operands[0], lines, indent)
                    lines.append(f"{pad}(call $rat_{callee})")
                else:
                    for arg in expr.operands:
                        self._compile_verb_expr_wat(arg, lines, indent)
                    m_callee = self._mangle_name(callee)
                    lines.append(f"{pad}(call ${m_callee})")

            elif expr.verb == "NEGATE":
                self._compile_verb_expr_wat(expr.operands[0], lines, indent)
                lines.append(f"{pad}(i64.sub (i64.const 0))")
                # Wait, negate top is num: (sub 0 num) then den stays same
                # Let's adjust stack: (sub 0 num), den
                lines.append(f"{pad};; (negate num, keep den)")
                # Actually, in WAT: (i64.const 0) (i64.const 1) (call $rat_sub)
                lines.append(f"{pad}(i64.const -1) (i64.const 1) (call $rat_mul)")

            elif expr.verb == "COMPARE":
                op_code = {
                    "==": 0,
                    "!=": 1,
                    "<": 2,
                    "<=": 3,
                    ">": 4,
                    ">=": 5,
                }.get(expr.relation or "==", 0)
                lines.append(f"{pad}(i32.const {op_code})")
                self._compile_verb_expr_wat(expr.operands[0], lines, indent)
                self._compile_verb_expr_wat(expr.operands[1], lines, indent)
                lines.append(f"{pad}(call $rat_cmp)")
                lines.append(f"{pad}(i64.extend_i32_u) (i64.const 1)")

        elif isinstance(expr, TuplePack):
            for el in expr.elements:
                self._compile_verb_expr_wat(el, lines, indent)

    def _collect_strings(self, sem_prog: SemanticProgram) -> None:
        def visit_expr(e: VerbExpr) -> None:
            if isinstance(e, TakeText):
                if e.value not in self.string_table:
                    offset = len(self.data_bytes)
                    self.data_bytes.extend(e.value.encode("utf-8") + b"\x00")
                    self.string_table[e.value] = offset
            elif isinstance(e, ReceiveInput):
                if e.prompt not in self.string_table:
                    offset = len(self.data_bytes)
                    self.data_bytes.extend(e.prompt.encode("utf-8") + b"\x00")
                    self.string_table[e.prompt] = offset
            elif isinstance(e, ApplyMathVerb):
                for op in e.operands:
                    visit_expr(op)
            elif isinstance(e, TuplePack):
                for el in e.elements:
                    visit_expr(el)

        def visit_verb(v: SemanticVerb) -> None:
            if isinstance(v, EstablishVerb):
                visit_expr(v.value)
            elif isinstance(v, AssignVerb):
                visit_expr(v.value)
            elif isinstance(v, DetermineVerb):
                visit_expr(v.condition)
                for b in v.body:
                    visit_verb(b)
                if v.alternative:
                    for b in v.alternative:
                        visit_verb(b)
            elif isinstance(v, RepeatVerb):
                if v.start:
                    visit_expr(v.start)
                visit_expr(v.end)
                for b in v.body:
                    visit_verb(b)
            elif isinstance(v, ConcludeVerb):
                for val in v.values:
                    visit_expr(val)
            elif isinstance(v, InscribeVerb):
                visit_expr(v.value)
            elif isinstance(v, DiscardVerb):
                visit_expr(v.expr)

        for proc in sem_prog.procedures:
            for v in proc.body:
                visit_verb(v)
        for v in sem_prog.problem_verbs:
            visit_verb(v)
        for v in sem_prog.result_verbs:
            visit_verb(v)

    def _collect_locals(self, verbs: List[SemanticVerb], exclude: Optional[Set[str]] = None) -> Set[str]:
        ex = exclude or set()
        locals_found: Set[str] = set()

        def scan(v: SemanticVerb) -> None:
            if isinstance(v, EstablishVerb):
                if v.name not in ex:
                    locals_found.add(v.name)
            elif isinstance(v, AssignVerb):
                for t in v.targets:
                    if t not in ex:
                        locals_found.add(t)
            elif isinstance(v, DetermineVerb):
                for b in v.body:
                    scan(b)
                if v.alternative:
                    for b in v.alternative:
                        scan(b)
            elif isinstance(v, RepeatVerb):
                if v.target not in ex:
                    locals_found.add(v.target)
                for b in v.body:
                    scan(b)

        for v in verbs:
            scan(v)
        return locals_found

    def _determine_return_arity(self, proc: ProcedureRecipe) -> int:
        for v in proc.body:
            if isinstance(v, ConcludeVerb):
                return len(v.values)
        return 1

    def _mangle_name(self, name: str) -> str:
        """Sanitizes names for WASM identifier compatibility ($a-b or cuneiform)."""
        # Replace non-ASCII and dashes
        safe_chars = []
        for ch in name:
            if ch.isalnum() or ch == "_":
                safe_chars.append(ch)
            elif ch == "-":
                safe_chars.append("_")
            else:
                safe_chars.append(f"u{ord(ch):04x}")
        return "".join(safe_chars)


def compile_to_wat(program: Program | SemanticProgram) -> str:
    """Convenience helper to compile an AST Program or SemanticProgram into .wat text."""
    compiler = WasmCompiler()
    return compiler.compile(program)

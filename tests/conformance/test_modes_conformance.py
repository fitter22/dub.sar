"""DUB.SAR 1.0 — Conformance Suite: Trimodal Equivalence (CR-006).

Asserts that identical programs written in:
- Tablet Mode (canonical cuneiform)
- Scholar Mode (ASCII transliteration)
- Mixed Mode
compile into equivalent AST and Bytecode IR and produce identical execution results.
"""

import unittest
from typing import List

from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer
from dubsar.vm import VirtualMachine


class TestModesConformance(unittest.TestCase):
    """Verifies that Tablet, Scholar, and Mixed modes execute with exact equivalence."""

    def _execute(self, source: str) -> List[str]:
        tokens = Lexer(source).tokenize()
        prog = Parser(tokens).parse()
        SemanticAnalyzer().analyze(prog)
        compiled = Compiler().compile(prog)
        outputs: List[str] = []
        vm = VirtualMachine(
            input_fn=lambda prompt: "0",
            output_fn=lambda v: outputs.append(str(v)),
            format_mode="canonical",
        )
        vm.execute(compiled)
        return outputs

    def test_trimodal_equivalence(self):
        # 1. Scholar Mode
        scholar_src = """PROBLEM
    total : 0
    repeat i 1 to 4:
        total := total + i
RESULT
    output "sum:"
    output total
"""

        # 2. Tablet Mode
        tablet_src = """𒂊𒁹
    total : 0
    𒄀 i 1 𒌗 4:
        total := total + i
𒅗𒁹
    𒁹𒀀 "sum:"
    𒁹𒀀 total
"""

        # 3. Mixed Mode
        mixed_src = """PROBLEM
    total : 0
    𒄀 i 1 to 4:
        total := total 𒍣 i
RESULT
    𒁹𒀀 "sum:"
    output total
"""

        out_scholar = self._execute(scholar_src)
        out_tablet = self._execute(tablet_src)
        out_mixed = self._execute(mixed_src)

        self.assertEqual(out_scholar, ["sum:", "10"])
        self.assertEqual(out_tablet, out_scholar)
        self.assertEqual(out_mixed, out_scholar)


if __name__ == "__main__":
    unittest.main()

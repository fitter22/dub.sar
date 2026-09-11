"""DUB.SAR 1.0 — Fourier Mathematics Foundation Tests (Layer H).

Tests:
- Powers of two and turn divisions table consultation
- Reference DFT on sequence tablets
- Recursive Radix-2 FFT on sequence tablets
- Mathematical equivalence of DFT and FFT within tolerance
- Reversibility: Inverse DFT and Inverse FFT recovering original signal
- Language-level execution in AST interpreter and VM
"""

import textwrap
import unittest

from dubsar.archive.archive import SQLiteTabletArchive
from dubsar.archive.models import HistoricalTag, TabletKind, TabletShape
from dubsar.archive.working import WorkingTablet
from dubsar.geometry import (
    DirectedQuantity,
    Direction,
    Turn,
    reference_dft,
    recursive_fft,
    sequence_to_directed_list,
)
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.numbers import Rational
from dubsar.parser import Parser
from dubsar.units import DIMENSIONLESS, Quantity, lookup_unit
from dubsar.vm import VirtualMachine


class TestStandardFourierArchive(unittest.TestCase):
    """Tests consultation of standard mathematical tables supporting Fourier computation."""

    def setUp(self):
        self.archive = SQLiteTabletArchive(":memory:")

    def tearDown(self):
        self.archive.close()

    def test_powers_of_two_table(self):
        tab = self.archive.consult("powers-of-two")
        self.assertEqual(tab.get(0), Rational(1))
        self.assertEqual(tab.get(1), Rational(2))
        self.assertEqual(tab.get(4), Rational(16))
        self.assertEqual(tab.get("2^8"), Rational(256))
        self.assertEqual(tab.get("len-16"), Rational(4))

    def test_turn_divisions_table(self):
        tab = self.archive.consult("turn-divisions")
        t_whole = tab.get("whole-turn")
        self.assertIsInstance(t_whole, Turn)
        self.assertEqual(t_whole.fraction, Rational(0))

        t_half = tab.get("half-turn")
        self.assertIsInstance(t_half, Turn)
        self.assertEqual(t_half.fraction, Rational(1, 2))

        t_quarter = tab.get("quarter-turn")
        self.assertIsInstance(t_quarter, Turn)
        self.assertEqual(t_quarter.fraction, Rational(1, 4))

        t_eighth = tab.get("eighth-turn")
        self.assertIsInstance(t_eighth, Turn)
        self.assertEqual(t_eighth.fraction, Rational(1, 8))


class TestFourierAlgorithms(unittest.TestCase):
    """Tests reference DFT and Radix-2 recursive FFT on directed sequences."""

    def test_dft_impulse_signal(self):
        # Impulse signal: [1, 0, 0, 0]
        # The Fourier transform of an impulse is flat across all harmonic bins: [1, 1, 1, 1]
        sig = [
            DirectedQuantity(1),
            DirectedQuantity(0),
            DirectedQuantity(0),
            DirectedQuantity(0),
        ]
        res_tablet = reference_dft(sig)
        out_list = sequence_to_directed_list(res_tablet)
        self.assertEqual(len(out_list), 4)
        for dq in out_list:
            self.assertEqual(dq.magnitude.value, Rational(1))

    def test_dft_dc_constant_signal(self):
        # DC signal: [1, 1, 1, 1]
        # Energy concentrates entirely at frequency bin 0 (DC component = 4)
        sig = [
            DirectedQuantity(1),
            DirectedQuantity(1),
            DirectedQuantity(1),
            DirectedQuantity(1),
        ]
        res_tablet = reference_dft(sig)
        out_list = sequence_to_directed_list(res_tablet)
        self.assertEqual(len(out_list), 4)
        # DC component
        self.assertEqual(out_list[0].magnitude.value, Rational(4))
        # Non-DC components cancel to 0
        for dq in out_list[1:]:
            self.assertLess(dq.magnitude.base_value(), Rational(1, 100))

    def test_fft_matches_dft_4_points(self):
        # Test N = 4 signal
        sig = [
            DirectedQuantity(1),
            DirectedQuantity(2),
            DirectedQuantity(3),
            DirectedQuantity(4),
        ]
        dft_res = sequence_to_directed_list(reference_dft(sig))
        fft_res = sequence_to_directed_list(recursive_fft(sig))

        self.assertEqual(len(dft_res), len(fft_res))
        for i in range(len(dft_res)):
            diff = abs(dft_res[i].magnitude.base_value() - fft_res[i].magnitude.base_value())
            self.assertLess(diff, Rational(1, 100))

    def test_fft_matches_dft_8_points(self):
        # Test N = 8 signal
        sig = [
            DirectedQuantity(2),
            DirectedQuantity(1),
            DirectedQuantity(0),
            DirectedQuantity(3),
            DirectedQuantity(1),
            DirectedQuantity(4),
            DirectedQuantity(2),
            DirectedQuantity(1),
        ]
        dft_res = sequence_to_directed_list(reference_dft(sig))
        fft_res = sequence_to_directed_list(recursive_fft(sig))

        self.assertEqual(len(dft_res), len(fft_res))
        for i in range(len(dft_res)):
            diff = abs(dft_res[i].magnitude.base_value() - fft_res[i].magnitude.base_value())
            self.assertLess(diff, Rational(1, 100))

    def test_fourier_reversibility_inverse_dft(self):
        # Forward DFT then Inverse DFT recovers original signal
        original = [
            DirectedQuantity(5),
            DirectedQuantity(2),
            DirectedQuantity(8),
            DirectedQuantity(1),
        ]
        fwd = reference_dft(original)
        inv = reference_dft(fwd, inverse=True)
        inv_list = sequence_to_directed_list(inv)

        for orig_dq, rec_dq in zip(original, inv_list):
            diff = abs(orig_dq.magnitude.base_value() - rec_dq.magnitude.base_value())
            self.assertLess(diff, Rational(1, 100))

    def test_fourier_reversibility_inverse_fft(self):
        # Forward FFT then Inverse FFT recovers original signal
        original = [
            DirectedQuantity(3),
            DirectedQuantity(7),
            DirectedQuantity(1),
            DirectedQuantity(5),
        ]
        fwd = recursive_fft(original)
        inv = recursive_fft(fwd, inverse=True)
        inv_list = sequence_to_directed_list(inv)

        for orig_dq, rec_dq in zip(original, inv_list):
            diff = abs(orig_dq.magnitude.base_value() - rec_dq.magnitude.base_value())
            self.assertLess(diff, Rational(1, 100))


class TestLanguageFourierExecution(unittest.TestCase):
    """Tests execution of DFT and FFT pipelines in DUB.SAR programs."""

    def test_dft_execution_scholar(self):
        src = textwrap.dedent("""
        PROBLEM
            working sig of length 0
            sig 1 append
            sig 0 append
            sig 0 append
            sig 0 append
            res : sig dft
            l : res length
            first_entry : res 0 take
            mag : first_entry.magnitude
        RESULT
            output l
            output mag
        """).strip()
        tree = Parser(Lexer(src).tokenize()).parse()
        out_ast = Interpreter().run(tree)
        self.assertEqual(out_ast, ["4", "1"])

        out_vm = VirtualMachine().execute(Compiler().compile(tree))
        self.assertEqual(out_vm, ["4", "1"])

    def test_fft_execution_scholar(self):
        src = textwrap.dedent("""
        PROBLEM
            working sig of length 0
            sig 1 append
            sig 1 append
            sig 1 append
            sig 1 append
            res : sig fft
            l : res length
            dc_entry : res 0 take
            mag : dc_entry.magnitude
        RESULT
            output l
            output mag
        """).strip()
        tree = Parser(Lexer(src).tokenize()).parse()
        out_ast = Interpreter().run(tree)
        self.assertEqual(out_ast, ["4", "4"])

        out_vm = VirtualMachine().execute(Compiler().compile(tree))
        self.assertEqual(out_vm, ["4", "4"])


if __name__ == "__main__":
    unittest.main()

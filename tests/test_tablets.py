"""DUB.SAR 1.0 — Tablet-Oriented Data Model Conformance and Unit Test Suite.

Verifies:
- Sequence tablets (consecutive 0-based integer keys)
- Mathematical tables (arbitrary exact keys)
- Structured tablets (named fields)
- First-class operations: take, put, append, length, remove, seek (first, last, nearest)
- Iteration: consider entries of, consider k, v of
- Error handling: DubSarImmutableTabletError, DubSarEntryNotFoundError
- Execution parity: Interpreter vs VirtualMachine
- Syntax parity: Scholar Mode vs Canonical Cuneiform
"""

import unittest
from dubsar.archive.archive import SQLiteTabletArchive
from dubsar.archive.models import TabletShape
from dubsar.archive.working import WorkingTablet
from dubsar.errors import (
    DubSarEntryNotFoundError,
    DubSarImmutableTabletError,
)
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.numbers import Rational
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer
from dubsar.units import DIMENSIONLESS, Quantity, lookup_unit
from dubsar.vm import VirtualMachine


class TestWorkingTabletModel(unittest.TestCase):
    """Direct unit tests for WorkingTablet python class."""

    def test_sequence_append_and_length(self):
        t = WorkingTablet(name="samples", shape=TabletShape.SEQUENCE)
        self.assertEqual(t.length(), 0)
        t.append(10)
        t.append(20)
        t.append(30)
        self.assertEqual(t.length(), 3)
        self.assertEqual(t[0], 10)
        self.assertEqual(t[1], 20)
        self.assertEqual(t[2], 30)
        self.assertEqual(t.first(), (Rational(0), 10))
        self.assertEqual(t.last(), (Rational(2), 30))

    def test_working_tablet_initial_length(self):
        t = WorkingTablet(name="buffer", shape=TabletShape.SEQUENCE, length=4)
        self.assertEqual(t.length(), 4)
        for i in range(4):
            self.assertEqual(t[i], Rational(0))
        t[0] = 100
        self.assertEqual(t[0], 100)

    def test_entry_not_found(self):
        t = WorkingTablet(name="tab")
        with self.assertRaises(DubSarEntryNotFoundError):
            _ = t[5]
        with self.assertRaises(DubSarEntryNotFoundError):
            _ = t["missing"]
        with self.assertRaises(DubSarEntryNotFoundError):
            t.remove(99)

    def test_remove_entry(self):
        t = WorkingTablet(name="tab")
        t.put(1, 100)
        t.put(2, 200)
        self.assertEqual(t.length(), 2)
        removed = t.remove(1)
        self.assertEqual(removed, 100)
        self.assertEqual(t.length(), 1)
        with self.assertRaises(DubSarEntryNotFoundError):
            _ = t[1]


class TestTabletLanguageExecution(unittest.TestCase):
    """Compiler, Interpreter, and VM execution tests for tablet model."""

    def _run_both(self, source: str, archive=None):
        tokens = Lexer(source).tokenize()
        prog = Parser(tokens).parse()
        SemanticAnalyzer().analyze(prog)
        
        # Interpreter
        interp = Interpreter(archive=archive)
        out_interp = interp.run(prog)

        # VM
        chunk = Compiler().compile(prog)
        vm = VirtualMachine(archive=archive)
        out_vm = vm.execute(chunk)

        self.assertEqual(out_interp, out_vm, f"Interpreter and VM output diverged! Interp: {out_interp}, VM: {out_vm}")
        return out_interp

    def test_sequence_append_and_length_scholar(self):
        src = """
problem:
    working seq of length 0
    append 10 to seq
    append 20 to seq
    append 30 to seq
    l : length of seq
    f : first from seq
    last_val : last from seq
result:
    l
    f
    last_val
"""
        out = self._run_both(src)
        self.assertEqual(out, ["3", "10", "30"])

    def test_sequence_postfix_scholar(self):
        src = """
problem:
    working s of length 0
    s 10 append
    s 20 append
    s 30 append
    l : s length
    second : s 1 take
result:
    l
    second
"""
        out = self._run_both(src)
        self.assertEqual(out, ["3", "20"])

    def test_sequence_cuneiform(self):
        src = """
𒂊𒁹
    working s of length 0
    s 15 𒈭
    s 25 𒈭
    l : s 𒁍
    x : s 0 𒋗
    y : s 1 𒋗
𒅗𒁹
    l
    x
    y
"""
        out = self._run_both(src)
        self.assertEqual(out, ["2", "15", "25"])

    def test_table_take_put_scholar(self):
        src = """
problem:
    working squares
    put 1 into squares at 1
    put 4 into squares at 2
    put 9 into squares at 3
    put 16 into squares at 4
    v3 : take entry 3 from squares
    v4 : squares 4 take
result:
    v3
    v4
"""
        out = self._run_both(src)
        self.assertEqual(out, ["9", "16"])

    def test_structured_tablet_initial_fields(self):
        src = """
problem:
    working planet:
        mass : 100
        radius : 20
    m : take entry mass from planet
    r : take entry radius from planet
result:
    m
    r
"""
        out = self._run_both(src)
        self.assertEqual(out, ["100", "20"])

    def test_consider_entries_scholar(self):
        src = """
problem:
    working vals of length 0
    append 5 to vals
    append 10 to vals
    append 15 to vals
    total : 0
    consider entries of vals:
        total : total + v
result:
    total
"""
        out = self._run_both(src)
        self.assertEqual(out, ["30"])

    def test_consider_key_val_scholar(self):
        src = """
problem:
    working coords
    put 10 into coords at 1
    put 20 into coords at 2
    sum_keys : 0
    sum_vals : 0
    consider k, val of coords:
        sum_keys : sum_keys + k
        sum_vals : sum_vals + val
result:
    sum_keys
    sum_vals
"""
        out = self._run_both(src)
        self.assertEqual(out, ["3", "30"])

    def test_sequence_transformation(self):
        src = """
problem:
    working origin of length 0
    append 1 to origin
    append 2 to origin
    append 3 to origin
    append 4 to origin

    working doubled of length 0
    consider entries of origin:
        append v * 2 to doubled

    l : length of doubled
    v0 : take entry 0 from doubled
    v3 : take entry 3 from doubled
result:
    l
    v0
    v3
"""
        out = self._run_both(src)
        self.assertEqual(out, ["4", "2", "8"])

    def test_remove_entry_execution(self):
        src = """
problem:
    working tab
    put 100 into tab at 1
    put 200 into tab at 2
    put 300 into tab at 3
    remove entry 2 from tab
    l : length of tab
    v1 : take entry 1 from tab
    v3 : take entry 3 from tab
result:
    l
    v1
    v3
"""
        out = self._run_both(src)
        self.assertEqual(out, ["2", "100", "300"])

    def test_immutable_tablet_error_on_put(self):
        src = """
problem:
    consult tablet reciprocals
    put 5 into reciprocals at 7
result:
    0
"""
        tokens = Lexer(src).tokenize()
        prog = Parser(tokens).parse()
        
        # Interpreter error
        interp = Interpreter()
        with self.assertRaises(DubSarImmutableTabletError):
            interp.run(prog)

        # VM error
        chunk = Compiler().compile(prog)
        vm = VirtualMachine()
        with self.assertRaises(DubSarImmutableTabletError):
            vm.execute(chunk)

    def test_immutable_tablet_error_on_append(self):
        src = """
problem:
    consult tablet reciprocals
    append 5 to reciprocals
result:
    0
"""
        tokens = Lexer(src).tokenize()
        prog = Parser(tokens).parse()
        
        # Interpreter error
        interp = Interpreter()
        with self.assertRaises(DubSarImmutableTabletError):
            interp.run(prog)

        # VM error
        chunk = Compiler().compile(prog)
        vm = VirtualMachine()
        with self.assertRaises(DubSarImmutableTabletError):
            vm.execute(chunk)

    def test_entry_not_found_error(self):
        src = """
problem:
    consult tablet reciprocals
    val : take entry 99 from reciprocals
result:
    val
"""
        tokens = Lexer(src).tokenize()
        prog = Parser(tokens).parse()
        
        interp = Interpreter()
        with self.assertRaises(DubSarEntryNotFoundError):
            interp.run(prog)

        chunk = Compiler().compile(prog)
        vm = VirtualMachine()
        with self.assertRaises(DubSarEntryNotFoundError):
            vm.execute(chunk)

    def test_inscribe_and_consult_sequence(self):
        arc = SQLiteTabletArchive(":memory:")
        src = """
problem:
    working fib of length 0
    append 1 to fib
    append 1 to fib
    append 2 to fib
    append 3 to fib
    append 5 to fib
    append 8 to fib
    inscribe tablet fib
result:
    length of fib
"""
        out = self._run_both(src, archive=arc)
        self.assertEqual(out, ["6"])
        
        # Consult inscribed tablet from archive
        tab = arc.consult("fib")
        self.assertEqual(tab.length(), 6)
        self.assertEqual(tab[0], Quantity(1))
        self.assertEqual(tab[5], Quantity(8))
        self.assertEqual(tab.first(), (Rational(0), Quantity(1)))
        self.assertEqual(tab.last(), (Rational(5), Quantity(8)))


if __name__ == "__main__":
    unittest.main()

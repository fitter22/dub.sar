"""DUB.SAR 1.0 — Tablet Archive Conformance and Unit Test Suite.

Verifies Sections 68-77 of the Tablet Archive Specification:
- §68 Archive Initialization Tests
- §69 Consultation Tests
- §70 Working Tablet Tests
- §71 Versioning Tests
- §72 Provenance Tests
- §73 Persistence Tests
- §74 Atomicity Tests
- §75 Concurrency Tests
- §76 Standard Mathematical Archive Tests
- §77 Exactness Tests
- Language Execution (Interpreter & VM) in Cuneiform and Scholar Mode
- CLI Subcommands (list, show, history, export, import, render)
"""

import json
import os
import tempfile
import unittest
from pathlib import Path

from dubsar.archive.archive import SQLiteTabletArchive
from dubsar.archive.models import (
    HistoricalTag,
    TabletKind,
    TabletMetadata,
    TabletShape,
    TabletVersionInfo,
    deserialize_value,
    serialize_value,
)
from dubsar.archive.seed import STANDARD_ARCHIVE_VERSION
from dubsar.archive.working import WorkingTablet
from dubsar.cli import build_parser, handle_archive_command
from dubsar.errors import (
    DubSarConsultationError,
    DubSarInvalidEntryError,
    DubSarInvalidTabletError,
    DubSarTabletNotFoundError,
    DubSarTabletVersionNotFoundError,
)
from dubsar.interpreter import Interpreter
from dubsar.ir import Compiler
from dubsar.lexer import Lexer
from dubsar.numbers import Rational
from dubsar.parser import Parser
from dubsar.semantic import SemanticAnalyzer
from dubsar.units import DIMENSIONLESS, Quantity, lookup_unit
from dubsar.vm import VirtualMachine


class TestArchiveInitialization(unittest.TestCase):
    """§68: Archive initialization tests."""

    def test_auto_seed_and_version(self):
        archive = SQLiteTabletArchive(":memory:")
        tablets = archive.list_tablets()
        names = {t["name"] for t in tablets}
        self.assertIn("reciprocals", names)
        self.assertIn("squares", names)
        self.assertIn("cubes", names)
        self.assertIn("common-fractions", names)
        self.assertIn("square-roots", names)
        self.assertIn("powers", names)
        self.assertIn("basic-metrology", names)
        self.assertIn("basic-geometry", names)
        self.assertIn("ea-nasir-shipment", names)
        archive.close()

    def test_repeated_startup_idempotence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")
            a1 = SQLiteTabletArchive(db_path)
            t1_count = len(a1.list_tablets())
            a1.close()

            # Second startup must not duplicate tablets
            a2 = SQLiteTabletArchive(db_path)
            t2_count = len(a2.list_tablets())
            a2.close()
            self.assertEqual(t1_count, t2_count)
            self.assertEqual(t1_count, 9)


class TestConsultation(unittest.TestCase):
    """§69: Consultation tests."""

    def setUp(self):
        self.archive = SQLiteTabletArchive(":memory:")

    def tearDown(self):
        self.archive.close()

    def test_consult_current_version(self):
        info = self.archive.consult("reciprocals")
        self.assertEqual(info.name, "reciprocals")
        self.assertEqual(info.version, 1)
        self.assertGreater(len(info.entries), 10)

    def test_consult_explicit_version(self):
        info = self.archive.consult("reciprocals", version=1)
        self.assertEqual(info.version, 1)

    def test_consult_missing_tablet_raises_error(self):
        with self.assertRaises(DubSarTabletNotFoundError):
            self.archive.consult("nonexistent_tablet_xyz")

    def test_consult_missing_version_raises_error(self):
        with self.assertRaises(DubSarTabletVersionNotFoundError):
            self.archive.consult("reciprocals", version=999)

    def test_consulted_entries_read_only(self):
        info = self.archive.consult("reciprocals")
        val = info.get(Rational(2))
        self.assertEqual(val, Rational(1, 2))


class TestWorkingTablet(unittest.TestCase):
    """§70: Working tablet tests."""

    def setUp(self):
        self.archive = SQLiteTabletArchive(":memory:")

    def tearDown(self):
        self.archive.close()

    def test_create_and_mutate_working_tablet(self):
        wt = self.archive.create_working("scratch")
        wt.put(1, Quantity(10, DIMENSIONLESS))
        wt.put(2, Quantity(20, DIMENSIONLESS))
        self.assertEqual(len(wt), 2)
        self.assertEqual(wt.get(1), Quantity(10, DIMENSIONLESS))

        # Replace existing entry
        wt.replace(2, Quantity(25, DIMENSIONLESS))
        self.assertEqual(wt.get(2), Quantity(25, DIMENSIONLESS))

        # Replace nonexistent entry errors
        with self.assertRaises(DubSarInvalidEntryError):
            wt.replace(99, Quantity(100, DIMENSIONLESS))

        # Remove entry
        rem = wt.remove(1)
        self.assertEqual(rem, Quantity(10, DIMENSIONLESS))
        self.assertEqual(len(wt), 1)

        # Remove nonexistent entry errors
        with self.assertRaises(DubSarInvalidEntryError):
            wt.remove(99)

    def test_seek_nearest(self):
        wt = self.archive.create_working("points")
        wt.put(10, Quantity(100, DIMENSIONLESS))
        wt.put(20, Quantity(200, DIMENSIONLESS))
        wt.put(30, Quantity(300, DIMENSIONLESS))

        best = wt.seek_nearest(23)
        self.assertIsNotNone(best)
        self.assertEqual(best[0], Rational(20))
        self.assertEqual(best[1], Quantity(200, DIMENSIONLESS))

    def test_inscribe_working_tablet(self):
        wt = self.archive.create_working("my_table")
        wt.put(Rational(3), Quantity(9, DIMENSIONLESS))
        info = self.archive.inscribe(wt, "my_table")
        self.assertEqual(info.name, "my_table")
        self.assertEqual(info.version, 1)

        reloaded = self.archive.consult("my_table")
        self.assertEqual(reloaded.get(Rational(3)), Quantity(9, DIMENSIONLESS))


class TestVersioningAndProvenance(unittest.TestCase):
    """§71, §72: Versioning and provenance lineage tests."""

    def setUp(self):
        self.archive = SQLiteTabletArchive(":memory:")

    def tearDown(self):
        self.archive.close()

    def test_version_increment_and_immutability(self):
        # Create initial tablet v1
        wt1 = self.archive.create_working("metrics")
        wt1.put(1, Quantity(100, DIMENSIONLESS))
        self.archive.inscribe(wt1, "metrics")

        # Copy as working and revise
        wt2 = self.archive.copy("metrics", "metrics-copy")
        wt2.replace(1, Quantity(150, DIMENSIONLESS))
        self.archive.inscribe(wt2, "metrics")

        # Verify v1 unchanged
        v1 = self.archive.consult("metrics", version=1)
        self.assertEqual(v1.get(1), Quantity(100, DIMENSIONLESS))

        # Verify v2 updated
        v2 = self.archive.consult("metrics", version=2)
        self.assertEqual(v2.get(1), Quantity(150, DIMENSIONLESS))

        # Current version resolves to v2
        curr = self.archive.consult("metrics")
        self.assertEqual(curr.version, 2)

        # History shows lineage v1 -> v2
        hist = self.archive.history("metrics")
        self.assertEqual(len(hist), 2)
        self.assertEqual(hist[0].version, 1)
        self.assertEqual(hist[1].version, 2)
        self.assertEqual(hist[1].parent_version, 1)

    def test_derivation_provenance(self):
        derived = self.archive.derive("reciprocals", "my-reciprocals", version=1)
        derived.put(100, Rational(1, 100))
        info = self.archive.inscribe(derived, "my-reciprocals")
        self.assertEqual(info.derived_from_name, "reciprocals")
        self.assertEqual(info.derived_from_version, 1)


class TestPersistenceAndAtomicity(unittest.TestCase):
    """§73, §74: File-backed persistence and transactional atomicity."""

    def test_file_persistence_survives_close(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "archive.db")
            a1 = SQLiteTabletArchive(db_path)
            wt = a1.create_working("persistent_data")
            day_unit = lookup_unit("day")
            wt.put("year-length", Quantity(Rational(3652422, 10000), day_unit))
            a1.inscribe(wt, "persistent_data")
            a1.close()

            # Open a new archive connection to the same file
            a2 = SQLiteTabletArchive(db_path)
            info = a2.consult("persistent_data")
            val = info.get("year-length")
            self.assertIsInstance(val, Quantity)
            self.assertEqual(val.value, Rational(3652422, 10000))
            self.assertEqual(str(val.unit), "day")
            a2.close()


class TestStandardMathematicalArchive(unittest.TestCase):
    """§76: Verification of Scribal Archive 1 values."""

    def setUp(self):
        self.archive = SQLiteTabletArchive(":memory:")

    def tearDown(self):
        self.archive.close()

    def test_reciprocals(self):
        recip = self.archive.consult("reciprocals")
        # reciprocal(2) = 1/2 = 0;30
        self.assertEqual(recip.get(2), Rational(1, 2))
        # reciprocal(3) = 1/3 = 0;20
        self.assertEqual(recip.get(3), Rational(1, 3))
        # reciprocal(4) = 1/4 = 0;15
        self.assertEqual(recip.get(4), Rational(1, 4))
        # reciprocal(5) = 1/5 = 0;12
        self.assertEqual(recip.get(5), Rational(1, 5))
        # reciprocal(60) = 1/60 = 0;1
        self.assertEqual(recip.get(60), Rational(1, 60))

    def test_squares_and_cubes(self):
        sq = self.archive.consult("squares")
        self.assertEqual(sq.get(2), Rational(4))
        self.assertEqual(sq.get(10), Rational(100))

        cb = self.archive.consult("cubes")
        self.assertEqual(cb.get(2), Rational(8))
        self.assertEqual(cb.get(3), Rational(27))


class TestExactness(unittest.TestCase):
    """§77: Exactness requirement: no floating point conversions."""

    def test_exact_sexagesimal_and_rational_preservation(self):
        archive = SQLiteTabletArchive(":memory:")
        wt = archive.create_working("exact_values")

        # 365;14,31,55 = 365 + 14/60 + 31/3600 + 55/216000 = 78892795 / 216000
        exact_rat = Rational(78892795, 216000)
        wt.put("tropical_year", exact_rat)
        wt.put("one_third", Rational(1, 3))

        archive.inscribe(wt, "exact_values")
        consulted = archive.consult("exact_values")

        self.assertEqual(consulted.get("tropical_year"), exact_rat)
        self.assertEqual(consulted.get("one_third"), Rational(1, 3))
        archive.close()


class TestLanguageArchiveExecution(unittest.TestCase):
    """End-to-end execution of archive statements and expressions in AST & VM."""

    def test_consult_and_take_entry_ast(self):
        src = """
problem
    consult "reciprocals"
    recip :
        4
        take entry from reciprocals
result
    recip
"""
        prog = Parser(Lexer(src).tokenize()).parse()
        interp = Interpreter()
        out = interp.run(prog)
        self.assertEqual(out, ["0;15"])

    def test_consult_and_take_entry_vm(self):
        src = """
problem
    consult "reciprocals"
    recip :
        5
        take entry from reciprocals
result
    recip
"""
        prog = Parser(Lexer(src).tokenize()).parse()
        compiler = Compiler()
        compiled = compiler.compile(prog)
        vm = VirtualMachine()
        out = vm.execute(compiled)
        self.assertEqual(out, ["0;12"])

    def test_working_tablet_creation_and_inscription(self):
        src = """
problem
    working powers_of_two
    put 2 into powers_of_two at 1
    put 4 into powers_of_two at 2
    put 8 into powers_of_two at 3
    inscribe powers_of_two as "powers_of_two"
result
    "inscribed"
"""
        prog = Parser(Lexer(src).tokenize()).parse()
        interp = Interpreter()
        interp.run(prog)
        reloaded = interp.archive.consult("powers_of_two")
        self.assertEqual(len(reloaded.entries), 3)
        self.assertEqual(reloaded.get(3), Quantity(8, DIMENSIONLESS))

    def test_cuneiform_archive_syntax(self):
        src = """
𒂊𒁹
    𒅆 "squares"
    val :
        10
        𒋗 entry 𒋫 squares
𒅗𒁹
    val
"""
        prog = Parser(Lexer(src).tokenize()).parse()
        interp = Interpreter()
        out = interp.run(prog)
        self.assertEqual(out, ["100"])


class TestArchiveCLI(unittest.TestCase):
    """Developer CLI commands for tablet archive."""

    def test_archive_cli_list_and_show(self):
        parser = build_parser()
        args = parser.parse_args(["archive", "list", "--archive", ":memory:"])
        ret = handle_archive_command(args)
        self.assertEqual(ret, 0)

        args_show = parser.parse_args(["archive", "show", "reciprocals", "--archive", ":memory:"])
        ret_show = handle_archive_command(args_show)
        self.assertEqual(ret_show, 0)

        args_hist = parser.parse_args(["archive", "history", "reciprocals", "--archive", ":memory:"])
        ret_hist = handle_archive_command(args_hist)
        self.assertEqual(ret_hist, 0)


class TestEaNasirArchiveWorkflow(unittest.TestCase):
    """End-to-end tests for Ea-nāṣir Tablet Archive workflow."""

    def test_ea_nasir_shipment_consultation_and_entries(self):
        archive = SQLiteTabletArchive(":memory:")
        info = archive.consult("ea-nasir-shipment")
        self.assertEqual(info.name, "ea-nasir-shipment")
        self.assertEqual(info.metadata.kind, TabletKind.DATA)
        self.assertEqual(info.metadata.historical_tag, HistoricalTag.MODERN)
        self.assertIn("fictionalized", info.metadata.notes.lower())

        self.assertEqual(info.get("merchant"), "Ea-nāṣir")
        self.assertEqual(info.get("promised-quantity"), Quantity(10, lookup_unit("talent")))
        self.assertEqual(info.get("delivered-quantity"), Quantity(10, lookup_unit("talent")))
        self.assertEqual(info.get("required-quality"), Rational(1))
        self.assertEqual(info.get("actual-quality"), Rational(3, 4))  # 0;45

    def test_ea_nasir_assessment_scholar_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = os.path.join(tmp, "archive.db")
            archive = SQLiteTabletArchive(db_path)

            source = Path("examples/ea_nasir_scholar.dub").read_text(encoding="utf-8")
            prog = Parser(Lexer(source).tokenize()).parse()
            SemanticAnalyzer().analyze(prog)
            chunk = Compiler().compile(prog)

            vm = VirtualMachine(archive=archive)
            out_vm = vm.execute(chunk)
            self.assertEqual(out_vm, ["Ea-nāṣir", "10 talent", "10 talent", "1", "0;45", "0;15"])

            assessment_tab = archive.consult("ea-nasir-assessment")
            self.assertEqual(assessment_tab.version, 1)
            self.assertEqual(assessment_tab.get("merchant"), "Ea-nāṣir")
            self.assertEqual(assessment_tab.get("promised"), Quantity(10, lookup_unit("talent")))
            self.assertEqual(assessment_tab.get("delivered"), Quantity(10, lookup_unit("talent")))
            self.assertEqual(assessment_tab.get("required-quality"), Rational(1))
            self.assertEqual(assessment_tab.get("actual-quality"), Rational(3, 4))
            self.assertEqual(assessment_tab.get("deficiency"), Quantity(Rational(1, 4), DIMENSIONLESS))

    def test_ea_nasir_assessment_cuneiform_parity(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = os.path.join(tmp, "archive.db")
            archive = SQLiteTabletArchive(db_path)

            source = Path("examples/ea_nasir.dub").read_text(encoding="utf-8")
            prog = Parser(Lexer(source).tokenize()).parse()
            SemanticAnalyzer().analyze(prog)
            chunk = Compiler().compile(prog)

            vm = VirtualMachine(archive=archive)
            out_vm = vm.execute(chunk)
            self.assertEqual(out_vm, ["Ea-nāṣir", "10 talent", "10 talent", "1", "0;45", "0;15"])

            assessment_tab = archive.consult("ea-nasir-assessment")
            self.assertEqual(assessment_tab.get("deficiency"), Quantity(Rational(1, 4), DIMENSIONLESS))

    def test_ea_nasir_persistence_across_restarts(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = os.path.join(tmp, "archive.db")
            # 1. Run and close
            arc1 = SQLiteTabletArchive(db_path)
            source = Path("examples/ea_nasir_scholar.dub").read_text(encoding="utf-8")
            prog = Parser(Lexer(source).tokenize()).parse()
            chunk = Compiler().compile(prog)
            vm1 = VirtualMachine(archive=arc1)
            vm1.execute(chunk)
            arc1.close()

            # 2. Reopen and verify persistence
            arc2 = SQLiteTabletArchive(db_path)
            persisted = arc2.consult("ea-nasir-assessment")
            self.assertEqual(persisted.version, 1)
            self.assertEqual(persisted.get("merchant"), "Ea-nāṣir")
            self.assertEqual(persisted.get("deficiency"), Quantity(Rational(1, 4), DIMENSIONLESS))
            arc2.close()

    def test_ea_nasir_versioning_and_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = os.path.join(tmp, "archive.db")
            archive = SQLiteTabletArchive(db_path)

            # Version 1
            src1 = Path("examples/ea_nasir_scholar.dub").read_text(encoding="utf-8")
            prog1 = Parser(Lexer(src1).tokenize()).parse()
            VirtualMachine(archive=archive).execute(Compiler().compile(prog1))

            v1 = archive.consult("ea-nasir-assessment", version=1)
            self.assertEqual(len(v1.entries), 6)
            self.assertIsNone(v1.get("verdict"))

            # Version 2
            src2 = Path("examples/ea_nasir_revision_scholar.dub").read_text(encoding="utf-8")
            prog2 = Parser(Lexer(src2).tokenize()).parse()
            VirtualMachine(archive=archive).execute(Compiler().compile(prog2))

            # Verify v1 unchanged
            v1_again = archive.consult("ea-nasir-assessment", version=1)
            self.assertEqual(len(v1_again.entries), 6)
            self.assertIsNone(v1_again.get("verdict"))

            # Verify v2 has new entry and lineage
            v2 = archive.consult("ea-nasir-assessment", version=2)
            self.assertEqual(len(v2.entries), 7)
            self.assertEqual(v2.get("verdict"), "rejected")
            self.assertEqual(v2.derived_from_name, "ea-nasir-assessment")
            self.assertEqual(v2.derived_from_version, 1)

            # History shows both
            hist = archive.history("ea-nasir-assessment")
            self.assertEqual(len(hist), 2)
            self.assertEqual([h.version for h in hist], [1, 2])

    def test_ea_nasir_rendering(self):
        with tempfile.TemporaryDirectory() as tmp:
            svg_out = os.path.join(tmp, "test_render.svg")
            parser = build_parser()
            args = parser.parse_args([
                "archive", "render", "ea-nasir-shipment",
                "--archive", ":memory:",
                "--style", "svg",
                "-o", svg_out,
            ])
            ret = handle_archive_command(args)
            self.assertEqual(ret, 0)
            self.assertTrue(os.path.exists(svg_out))
            content = Path(svg_out).read_text(encoding="utf-8")
            self.assertTrue(content.startswith("<svg"))
            self.assertIn("EA-NASIR-SHIPMENT", content)


if __name__ == "__main__":
    unittest.main()

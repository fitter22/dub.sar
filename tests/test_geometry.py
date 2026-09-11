"""DUB.SAR 1.0 — Geometric Mathematics Foundation Tests.

Tests the geometric progression (Layers A through G):
- Exact rational square and square root
- Babylonian iterative square root
- Ratio division and metrological units
- Right triangle determinations and Pythagorean validation
- Inclinations and feeds
- Turn system and Direction orientation
- Approximate quantities and explicit tolerance comparison
- Directed quantities, rotation, and vector addition
- Execution via AST interpreter and VM
- Serialization and deserialization in the Tablet Archive
"""

import os
import tempfile
import unittest

from dubsar.archive.models import HistoricalTag, TabletKind, TabletShape
from dubsar.archive.archive import SQLiteTabletArchive
from dubsar.archive.working import WorkingTablet
from dubsar.errors import DubSarGeometricError, DubSarMathError, DubSarTypeError
from dubsar.geometry import (
    ApproximateQuantity,
    DirectedQuantity,
    Direction,
    RightTriangleValue,
    Turn,
    make_inclination,
)
from dubsar.interpreter import Interpreter
from dubsar.lexer import Lexer
from dubsar.numbers import Rational
from dubsar.parser import Parser
from dubsar.units import DIMENSIONLESS, Quantity, lookup_unit
from dubsar.ir import Compiler
from dubsar.vm import VirtualMachine


class TestRationalAndQuantityGeometry(unittest.TestCase):
    """Tests exact squares, square roots, and ratios."""

    def test_rational_exact_square_and_root(self):
        r = Rational(3, 4)
        sq = r * r
        self.assertEqual(sq, Rational(9, 16))
        self.assertTrue(sq.is_perfect_square())
        self.assertEqual(sq.exact_sqrt(), Rational(3, 4))

        # Non-perfect square
        two = Rational(2, 1)
        self.assertFalse(two.is_perfect_square())
        self.assertIsNone(two.exact_sqrt())

    def test_babylonian_sqrt(self):
        two = Rational(2, 1)
        # 6 iterations gives extremely high accuracy
        approx_sqrt2 = two.sqrt_babylonian(iterations=6)
        # Check that approx_sqrt2^2 is very close to 2
        diff = abs(approx_sqrt2 * approx_sqrt2 - two)
        self.assertLess(float(diff.numerator) / float(diff.denominator), 1e-8)

        # Compare with YBC 7289 attested constant 1;24,51,10 = 305470 / 216000
        ybc = Rational(305470, 216000)
        ybc_diff = abs(ybc * ybc - two)
        self.assertLess(float(ybc_diff.numerator) / float(ybc_diff.denominator), 1e-5)

    def test_quantity_square_and_root(self):
        m = lookup_unit("m")
        q = Quantity(4, m)
        q_sq = q.square()
        self.assertEqual(q_sq.value, Rational(16))
        self.assertEqual(q_sq.unit.dimensions, {"length": 2})

        q_root = q_sq.square_root()
        self.assertEqual(q_root.value, Rational(4))
        self.assertEqual(q_root.unit.dimensions, {"length": 1})

        # Incompatible square root without perfect square
        q_non_perf = Quantity(2, m * m)
        with self.assertRaises(DubSarMathError):
            q_non_perf.square_root(allow_approx=False)

        q_approx = q_non_perf.square_root(allow_approx=True)
        self.assertEqual(q_approx.unit.dimensions, {"length": 1})

    def test_ratio_dimensionless_division(self):
        kus = lookup_unit("kus")
        q1 = Quantity(12, kus)
        q2 = Quantity(6, kus)
        ratio = q1 / q2
        self.assertTrue(ratio.is_dimensionless)
        self.assertEqual(ratio.value, Rational(2))

        # Compatible length units across different scales
        # 1 nindan = 12 kus
        nindan = lookup_unit("nindan")
        q_nindan = Quantity(1, nindan)
        ratio_scale = q_nindan / q1
        self.assertTrue(ratio_scale.is_dimensionless)
        self.assertEqual(ratio_scale.value, Rational(1))


class TestRightTriangleAndInclination(unittest.TestCase):
    """Tests right triangles and inclination determinations."""

    def test_right_triangle_properties(self):
        tri = RightTriangleValue(3, 4, 5)
        self.assertTrue(tri.is_valid())
        self.assertEqual(tri.fields["short-side"], Quantity(3, DIMENSIONLESS))
        self.assertEqual(tri.fields["long-side"], Quantity(4, DIMENSIONLESS))
        self.assertEqual(tri.fields["diagonal"], Quantity(5, DIMENSIONLESS))
        self.assertEqual(tri.fields["inclination"], Rational(4, 3))
        self.assertEqual(tri.fields["feed"], Rational(3, 4))
        self.assertEqual(tri.fields["area"], Quantity(6, DIMENSIONLESS))

    def test_right_triangle_determine_missing(self):
        # Solve missing diagonal
        t1 = RightTriangleValue.determine(short_side=5, long_side=12)
        self.assertEqual(t1.fields["diagonal"], Quantity(13, DIMENSIONLESS))
        self.assertTrue(t1.is_valid())

        # Solve missing long-side
        t2 = RightTriangleValue.determine(short_side=8, diagonal=17)
        self.assertEqual(t2.fields["long-side"], Quantity(15, DIMENSIONLESS))
        self.assertTrue(t2.is_valid())

        # Solve missing short-side
        t3 = RightTriangleValue.determine(long_side=21, diagonal=29)
        self.assertEqual(t3.fields["short-side"], Quantity(20, DIMENSIONLESS))
        self.assertTrue(t3.is_valid())

    def test_right_triangle_scale(self):
        t = RightTriangleValue(3, 4, 5)
        scaled = t.scale(Rational(3))
        self.assertEqual(scaled.fields["short-side"], Quantity(9, DIMENSIONLESS))
        self.assertEqual(scaled.fields["long-side"], Quantity(12, DIMENSIONLESS))
        self.assertEqual(scaled.fields["diagonal"], Quantity(15, DIMENSIONLESS))
        # Inclination remains unchanged
        self.assertEqual(scaled.fields["inclination"], Rational(4, 3))

    def test_make_inclination(self):
        inc = make_inclination(rise=1, run=3)
        self.assertEqual(inc.fields["rise"], Quantity(1, DIMENSIONLESS))
        self.assertEqual(inc.fields["run"], Quantity(3, DIMENSIONLESS))
        self.assertEqual(inc.fields["inclination"], Rational(1, 3))
        self.assertEqual(inc.fields["feed"], Rational(3, 1))


class TestTurnAndDirection(unittest.TestCase):
    """Tests Turn cycle fractions and Direction orientations."""

    def test_turn_arithmetic_and_wraparound(self):
        t_quarter = Turn.quarter()
        t_half = Turn.half()
        t_sum = t_quarter + t_half
        self.assertEqual(t_sum.fraction, Rational(3, 4))

        # Wraparound
        t_wrap = t_sum + t_half
        self.assertEqual(t_wrap.fraction, Rational(1, 4))

        # Division
        t_div = Turn.division(3, 12)
        self.assertEqual(t_div, t_quarter)

    def test_direction_orientations_and_components(self):
        d_ref = Direction.reference()
        self.assertEqual(d_ref.components(), (Rational(1), Rational(0)))

        d_perp = Direction.perpendicular()
        self.assertEqual(d_perp.components(), (Rational(0), Rational(1)))

        d_opp = Direction.opposite_reference()
        self.assertEqual(d_opp.components(), (Rational(-1), Rational(0)))

        # 1/8 turn
        d_diag = Direction(Turn.eighth())
        cx, cy = d_diag.components()
        self.assertEqual(cx, Rational(17, 24))
        self.assertEqual(cy, Rational(17, 24))

    def test_direction_from_inclination(self):
        d1 = Direction.from_inclination(rise=0, run=5)
        self.assertEqual(d1, Direction.reference())

        d2 = Direction.from_inclination(rise=4, run=0)
        self.assertEqual(d2, Direction.perpendicular())


class TestApproximateQuantity(unittest.TestCase):
    """Tests explicit approximation and prevention of silent exact equality."""

    def test_rejection_of_silent_exact_equality(self):
        aq = ApproximateQuantity(Rational(3, 2), precision=4)
        with self.assertRaises(DubSarTypeError):
            _ = (aq == Rational(3, 2))

    def test_within_tolerance_check(self):
        aq = ApproximateQuantity(Rational(1414, 1000), precision=3)
        # Target within 1/100
        self.assertTrue(aq.is_within_tolerance(Rational(141, 100), tolerance=Rational(1, 100)))
        # Target outside 1/1000
        self.assertFalse(aq.is_within_tolerance(Rational(150, 100), tolerance=Rational(1, 100)))


class TestDirectedQuantity(unittest.TestCase):
    """Tests magnitude + direction, rotation, scaling, and vector addition."""

    def test_directed_quantity_rotation_and_scaling(self):
        dq = DirectedQuantity(Quantity(10, lookup_unit("m")), Direction.reference())
        rotated = dq.rotate(Turn.quarter())
        self.assertEqual(rotated.magnitude, Quantity(10, lookup_unit("m")))
        self.assertEqual(rotated.direction, Direction.perpendicular())

        scaled = dq.scale(Rational(3, 2))
        self.assertEqual(scaled.magnitude, Quantity(15, lookup_unit("m")))

    def test_directed_quantity_vector_addition(self):
        m = lookup_unit("m")
        # 3 along reference (x-axis) + 4 along perpendicular (y-axis) = 5 along (3, 4)
        dq1 = DirectedQuantity(Quantity(3, m), Direction.reference())
        dq2 = DirectedQuantity(Quantity(4, m), Direction.perpendicular())
        dq_res = dq1 + dq2
        self.assertEqual(dq_res.magnitude, Quantity(5, m))


import textwrap


class TestLanguageGeometricExecution(unittest.TestCase):
    """Tests execution of geometric language syntax in AST and VM."""

    def test_square_and_square_root_scholar(self):
        src = textwrap.dedent("""
        PROBLEM
            x : 5
            sq := x square
            rt := sq square-root
        RESULT
            output sq
            output rt
        """).strip()
        tree = Parser(Lexer(src).tokenize()).parse()
        out_ast = Interpreter().run(tree)
        self.assertEqual(out_ast, ["25", "5"])

        out_vm = VirtualMachine().execute(Compiler().compile(tree))
        self.assertEqual(out_vm, ["25", "5"])

    def test_right_triangle_determination_scholar(self):
        src = textwrap.dedent("""
        PROBLEM
            tri := 3 4 right-triangle
            valid := tri validate-triangle
            diag := tri.diagonal
            inc := tri.inclination
        RESULT
            output valid
            output diag
            output inc
        """).strip()
        tree = Parser(Lexer(src).tokenize()).parse()
        out_ast = Interpreter().run(tree)
        self.assertEqual(out_ast, ["1", "5", "1;20"])

        out_vm = VirtualMachine().execute(Compiler().compile(tree))
        self.assertEqual(out_vm, ["1", "5", "1;20"])

    def test_inclination_determination_scholar(self):
        src = textwrap.dedent("""
        PROBLEM
            slope := 1 3 inclination
            inc := slope.inclination
            fd := slope.feed
        RESULT
            output inc
            output fd
        """).strip()
        tree = Parser(Lexer(src).tokenize()).parse()
        out_ast = Interpreter().run(tree)
        self.assertEqual(out_ast, ["0;20", "3"])

        out_vm = VirtualMachine().execute(Compiler().compile(tree))
        self.assertEqual(out_vm, ["0;20", "3"])

    def test_cuneiform_geometric_syntax(self):
        # 𒅁 (square) and 𒁀𒋛 (ba-si / square-root)
        src = textwrap.dedent("""
        𒂊𒁹
            x : 6
            sq := x 𒅁
            rt := sq 𒁀𒋛
        𒅗𒁹
            𒁹𒀀 sq
            𒁹𒀀 rt
        """).strip()
        tree = Parser(Lexer(src).tokenize()).parse()
        out_ast = Interpreter().run(tree)
        self.assertEqual(out_ast, ["36", "6"])

        out_vm = VirtualMachine().execute(Compiler().compile(tree))
        self.assertEqual(out_vm, ["36", "6"])


class TestArchiveGeometricSerialization(unittest.TestCase):
    """Tests persistent round-trip storage of geometric types in SQLite."""

    def test_archive_stores_and_retrieves_geometric_objects(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "geom_test.db")
            archive = SQLiteTabletArchive(db_path)

            wt = WorkingTablet(
                "my-geom-tablet",
                shape=TabletShape.TABLE,
                kind=TabletKind.MATHEMATICAL,
            )
            wt.put("tri", RightTriangleValue(5, 12, 13))
            wt.put("turn", Turn.quarter())
            wt.put("dir", Direction.perpendicular())
            wt.put("approx", ApproximateQuantity(Rational(7, 5), precision=4))
            wt.put("dq", DirectedQuantity(Quantity(10, lookup_unit("m")), Direction.reference()))

            archive.inscribe(wt, "my-geom-tablet")
            archive.close()

            # Reopen and verify
            archive2 = SQLiteTabletArchive(db_path)
            t = archive2.consult("my-geom-tablet")
            tri = t.get("tri")
            self.assertIsInstance(tri, RightTriangleValue)
            self.assertEqual(tri.fields["diagonal"], Quantity(13, DIMENSIONLESS))

            turn = t.get("turn")
            self.assertIsInstance(turn, Turn)
            self.assertEqual(turn.fraction, Rational(1, 4))

            dir_val = t.get("dir")
            self.assertIsInstance(dir_val, Direction)
            self.assertEqual(dir_val.fraction, Rational(1, 4))

            approx_val = t.get("approx")
            self.assertIsInstance(approx_val, ApproximateQuantity)
            self.assertEqual(approx_val.value, Rational(7, 5))

            dq_val = t.get("dq")
            self.assertIsInstance(dq_val, DirectedQuantity)
            self.assertEqual(dq_val.magnitude, Quantity(10, lookup_unit("m")))

            archive2.close()


if __name__ == "__main__":
    unittest.main()

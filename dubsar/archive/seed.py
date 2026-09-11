"""DUB.SAR 1.0 — Standard Scholarly Archive Generator (Scribal Archive 1).

Implements Section 27-34, 47, 76 of the Tablet Archive Change Request:
- Standard mathematical knowledge tablets
- Exact rational values, fractions, powers, metrology, and geometry
- Scholarly provenance and historical authenticity tagging
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from dubsar.archive.models import HistoricalTag, TabletKind, TabletMetadata, TabletShape
from dubsar.archive.working import WorkingTablet
from dubsar.geometry import RightTriangleValue, Turn, make_inclination
from dubsar.numbers import Rational
from dubsar.units import Quantity, lookup_unit


STANDARD_ARCHIVE_VERSION = "Scribal Archive 1"


def build_standard_tablets() -> List[WorkingTablet]:
    """Generates the initial canonical collection of standard scholarly tablets (§27)."""
    tablets: List[WorkingTablet] = []

    # 1. Reciprocals (igi-bi) (§28, §76)
    recip_metadata = TabletMetadata(
        title="Standard Old Babylonian Table of Reciprocals (igi-bi)",
        kind=TabletKind.MATHEMATICAL,
        historical_tag=HistoricalTag.ATTESTED,
        period="Old Babylonian (c. 1900-1600 BCE)",
        confidence="high",
        source="Canonical scribal school curriculum (VAT 6505, BM 80150)",
        provenance="Nippur/Sippar scribal tradition",
        notes="Exact sexagesimal regular reciprocals.",
    )
    recip_tablet = WorkingTablet("reciprocals", shape=TabletShape.TABLE, kind=TabletKind.MATHEMATICAL, metadata=recip_metadata)
    standard_reciprocals = [
        (2, Rational(1, 2)),
        (3, Rational(1, 3)),
        (4, Rational(1, 4)),
        (5, Rational(1, 5)),
        (6, Rational(1, 6)),
        (8, Rational(1, 8)),
        (9, Rational(1, 9)),
        (10, Rational(1, 10)),
        (12, Rational(1, 12)),
        (15, Rational(1, 15)),
        (16, Rational(1, 16)),
        (18, Rational(1, 18)),
        (20, Rational(1, 20)),
        (24, Rational(1, 24)),
        (25, Rational(1, 25)),
        (27, Rational(1, 27)),
        (30, Rational(1, 30)),
        (32, Rational(1, 32)),
        (36, Rational(1, 36)),
        (40, Rational(1, 40)),
        (45, Rational(1, 45)),
        (48, Rational(1, 48)),
        (50, Rational(1, 50)),
        (54, Rational(1, 54)),
        (60, Rational(1, 60)),
    ]
    for k, v in standard_reciprocals:
        recip_tablet.put(k, v)
    tablets.append(recip_tablet)

    # 2. Common Fractions (§29)
    frac_metadata = TabletMetadata(
        title="Elementary Sexagesimal Fractions",
        kind=TabletKind.MATHEMATICAL,
        historical_tag=HistoricalTag.ATTESTED,
        period="Old Babylonian",
        confidence="high",
        notes="Standard fractional divisions of unit 1.",
    )
    frac_tablet = WorkingTablet("common-fractions", shape=TabletShape.TABLE, kind=TabletKind.MATHEMATICAL, metadata=frac_metadata)
    fractions = [
        (Rational(1, 2), Rational(1, 2)),
        (Rational(1, 3), Rational(1, 3)),
        (Rational(2, 3), Rational(2, 3)),
        (Rational(1, 4), Rational(1, 4)),
        (Rational(3, 4), Rational(3, 4)),
        (Rational(1, 5), Rational(1, 5)),
        (Rational(1, 6), Rational(1, 6)),
        (Rational(5, 6), Rational(5, 6)),
        (Rational(1, 8), Rational(1, 8)),
        (Rational(1, 10), Rational(1, 10)),
        (Rational(1, 12), Rational(1, 12)),
    ]
    for k, v in fractions:
        frac_tablet.put(k, v)
    tablets.append(frac_tablet)

    # 3. Table of Squares (íb-sá) (§30, §76)
    sq_metadata = TabletMetadata(
        title="Table of Squares (íb-si8 / íb-sá)",
        kind=TabletKind.MATHEMATICAL,
        historical_tag=HistoricalTag.ATTESTED,
        period="Old Babylonian",
        confidence="high",
        source="Canonical scribal school curriculum",
    )
    sq_tablet = WorkingTablet("squares", shape=TabletShape.TABLE, kind=TabletKind.MATHEMATICAL, metadata=sq_metadata)
    for n in range(1, 61):
        sq_tablet.put(n, Rational(n * n))
    tablets.append(sq_tablet)

    # 4. Table of Cubes (ba-si) (§31, §76)
    cube_metadata = TabletMetadata(
        title="Table of Cubes (ba-si)",
        kind=TabletKind.MATHEMATICAL,
        historical_tag=HistoricalTag.ATTESTED,
        period="Old Babylonian",
        confidence="high",
    )
    cube_tablet = WorkingTablet("cubes", shape=TabletShape.TABLE, kind=TabletKind.MATHEMATICAL, metadata=cube_metadata)
    for n in range(1, 31):
        cube_tablet.put(n, Rational(n * n * n))
    tablets.append(cube_tablet)

    # 5. Square Roots & Approximations (§32)
    sqrt_metadata = TabletMetadata(
        title="Attested Roots and Coefficients",
        kind=TabletKind.MATHEMATICAL,
        historical_tag=HistoricalTag.ATTESTED,
        period="Old Babylonian",
        confidence="high",
        source="Tablet YBC 7289; standard root lists",
        notes="Root of 2 contains canonical sexagesimal approximation 1;24,51,10.",
    )
    sqrt_tablet = WorkingTablet("square-roots", shape=TabletShape.TABLE, kind=TabletKind.MATHEMATICAL, metadata=sqrt_metadata)
    sqrt_entries = [
        (1, Rational(1)),
        (2, Rational(305470, 216000)),  # 1;24,51,10
        (4, Rational(2)),
        (9, Rational(3)),
        (16, Rational(4)),
        (25, Rational(5)),
        (36, Rational(6)),
        (49, Rational(7)),
        (64, Rational(8)),
        (81, Rational(9)),
        (100, Rational(10)),
    ]
    for k, v in sqrt_entries:
        sqrt_tablet.put(k, v)
    tablets.append(sqrt_tablet)

    # 6. Powers Table (§33)
    pow_metadata = TabletMetadata(
        title="Powers of Small Integers",
        kind=TabletKind.MATHEMATICAL,
        historical_tag=HistoricalTag.RECONSTRUCTED,
        confidence="high",
    )
    pow_tablet = WorkingTablet("powers", shape=TabletShape.TABLE, kind=TabletKind.MATHEMATICAL, metadata=pow_metadata)
    # Powers of 2: 1 to 10
    for exp in range(1, 11):
        pow_tablet.put(f"2^{exp}", Rational(2 ** exp))
    # Powers of 3: 1 to 6
    for exp in range(1, 7):
        pow_tablet.put(f"3^{exp}", Rational(3 ** exp))
    # Powers of 5: 1 to 4
    for exp in range(1, 5):
        pow_tablet.put(f"5^{exp}", Rational(5 ** exp))
    tablets.append(pow_tablet)

    # 7. Basic Metrology (§34)
    metro_metadata = TabletMetadata(
        title="Sumerian and Old Babylonian Metrological Standards",
        kind=TabletKind.METROLOGICAL,
        historical_tag=HistoricalTag.ATTESTED,
        period="Old Babylonian",
        provenance="Standard lexical and metrological lists",
        notes="Ratios of length, area, volume, and weight.",
    )
    metro_tablet = WorkingTablet("basic-metrology", shape=TabletShape.TABLE, kind=TabletKind.METROLOGICAL, metadata=metro_metadata)
    metro_entries = [
        ("1-kus-in-su-si", Rational(30)),         # 1 cubit = 30 fingers
        ("1-gi-in-kus", Rational(6)),             # 1 reed = 6 cubits
        ("1-nindan-in-kus", Rational(12)),        # 1 nindan = 12 cubits
        ("1-ese-in-nindan", Rational(10)),        # 1 ese = 10 nindan
        ("1-danna-in-nindan", Rational(1800)),    # 1 league = 1800 nindan
        ("1-sar-in-nindan2", Rational(1)),        # 1 sar = 1 nindan^2
        ("1-iku-in-sar", Rational(100)),          # 1 iku = 100 sar
        ("1-bur-in-iku", Rational(18)),           # 1 bur = 18 iku
        ("1-ban-in-sila", Rational(10)),          # 1 ban = 10 sila
        ("1-bariga-in-ban", Rational(6)),         # 1 bariga = 6 ban (60 sila)
        ("1-gur-in-bariga", Rational(5)),         # 1 gur = 5 bariga (300 sila)
        ("1-gin-in-se", Rational(180)),           # 1 shekel = 180 grains
        ("1-ma-na-in-gin", Rational(60)),         # 1 mina = 60 shekels
        ("1-gu-in-ma-na", Rational(60)),          # 1 talent = 60 minas
    ]
    for k, v in metro_entries:
        metro_tablet.put(k, v)
    tablets.append(metro_tablet)

    # 8. Basic Geometry Coefficients (§27)
    geom_metadata = TabletMetadata(
        title="Old Babylonian Geometric Coefficients",
        kind=TabletKind.MATHEMATICAL,
        historical_tag=HistoricalTag.ATTESTED,
        period="Old Babylonian",
        provenance="Susa mathematical tablets (TMS 3), YBC 7289",
        notes="Standard geometric coefficients: circle perimeter and area, square diagonal (TMS 3 1;25 and YBC 7289 1;24,51,10).",
    )
    geom_tablet = WorkingTablet("basic-geometry", shape=TabletShape.TABLE, kind=TabletKind.MATHEMATICAL, metadata=geom_metadata)
    geom_entries = [
        ("circle-circumference-ratio", Rational(3)),
        ("circle-area-coefficient", Rational(1, 12)),        # 0;05
        ("square-diagonal-coefficient", Rational(17, 12)),    # 1;25 (TMS 3)
        ("square-diagonal-ybc7289", Rational(305470, 216000)), # 1;24,51,10 (YBC 7289)
        ("equilateral-triangle-coefficient", Rational(7, 16)), # 0;26,15
    ]
    for k, v in geom_entries:
        geom_tablet.put(k, v)
    tablets.append(geom_tablet)

    # 9. Right Triangles and Triples (§5, §7)
    rt_metadata = TabletMetadata(
        title="Old Babylonian Right Triangles and Pythagorean Triples",
        kind=TabletKind.MATHEMATICAL,
        historical_tag=HistoricalTag.ATTESTED,
        period="Old Babylonian (c. 1900-1600 BCE)",
        confidence="high",
        source="Plimpton 322 (Columbia University), CBS 2075, UET 6/2 236",
        notes="Exact right triangles with short-side, long-side, diagonal, and inclination. "
              "Represents shared mathematical substrate neutral between Robson's reciprocal/pedagogical analysis "
              "and Mansfield-Wildberger's ratio-based trigonometry.",
    )
    rt_tablet = WorkingTablet("right-triangles", shape=TabletShape.TABLE, kind=TabletKind.MATHEMATICAL, metadata=rt_metadata)
    rt_triples = [
        ("3-4-5", RightTriangleValue(3, 4, 5)),
        ("5-12-13", RightTriangleValue(5, 12, 13)),
        ("8-15-17", RightTriangleValue(8, 15, 17)),
        ("20-21-29", RightTriangleValue(20, 21, 29)),
        ("119-120-169", RightTriangleValue(119, 120, 169)),  # Plimpton 322 row 1
        ("3367-3456-4825", RightTriangleValue(3367, 3456, 4825)),  # Plimpton 322 row 2
        ("4601-4800-6649", RightTriangleValue(4601, 4800, 6649)),  # Plimpton 322 row 3
    ]
    for idx, (name, tri_val) in enumerate(rt_triples, start=1):
        rt_tablet.put(idx, tri_val)
        rt_tablet.put(name, tri_val)
    tablets.append(rt_tablet)

    # 10. Inclinations and Slopes (§5.4, §6, §7)
    inc_metadata = TabletMetadata(
        title="Old Babylonian Inclinations, Batters, and Ramp Feeds",
        kind=TabletKind.MATHEMATICAL,
        historical_tag=HistoricalTag.ATTESTED,
        period="Old Babylonian",
        confidence="high",
        source="Old Babylonian mathematical problem texts (BM 85194, YBC 4675)",
        notes="Attested rise/run slope ratios (kussû and mūṣû) for ramps, walls, and ditch excavations.",
    )
    inc_tablet = WorkingTablet("inclinations", shape=TabletShape.TABLE, kind=TabletKind.MATHEMATICAL, metadata=inc_metadata)
    inc_entries = [
        ("gentle-ramp", make_inclination(rise=1, run=5)),
        ("standard-ramp", make_inclination(rise=1, run=3)),
        ("steep-ramp", make_inclination(rise=1, run=2)),
        ("diagonal-slope", make_inclination(rise=1, run=1)),
        ("wall-batter", make_inclination(rise=6, run=1)),
    ]
    for idx, (name, inc_val) in enumerate(inc_entries, start=1):
        inc_tablet.put(idx, inc_val)
        inc_tablet.put(name, inc_val)
    tablets.append(inc_tablet)

    # 11. Powers of Two (§15, §7)
    p2_metadata = TabletMetadata(
        title="Scholarly Table of Powers of Two",
        kind=TabletKind.MATHEMATICAL,
        historical_tag=HistoricalTag.RECONSTRUCTED,
        period="Scholarly computational table",
        confidence="high",
        notes="Exact integer powers of 2 for length matching, domain bounds, and radix-2 Fourier determination.",
    )
    p2_tablet = WorkingTablet("powers-of-two", shape=TabletShape.TABLE, kind=TabletKind.MATHEMATICAL, metadata=p2_metadata)
    for exp in range(0, 17):
        p_val = Rational(2 ** exp)
        p2_tablet.put(exp, p_val)
        p2_tablet.put(f"2^{exp}", p_val)
        # Also index by value to check if length is power of 2
        p2_tablet.put(f"len-{2 ** exp}", Rational(exp))
    tablets.append(p2_tablet)

    # 12. Turn Divisions (§9, §13, §7)
    td_metadata = TabletMetadata(
        title="Regular Harmonic Divisions of a Full Turn",
        kind=TabletKind.MATHEMATICAL,
        historical_tag=HistoricalTag.MODERN,
        period="DUB.SAR Mathematical Foundation",
        confidence="high",
        notes="Equal cycle fractions of a turn (tau) without premature modern degrees or radians.",
    )
    td_tablet = WorkingTablet("turn-divisions", shape=TabletShape.TABLE, kind=TabletKind.MATHEMATICAL, metadata=td_metadata)
    td_entries = [
        ("whole-turn", Turn.whole()),
        ("half-turn", Turn.half()),
        ("quarter-turn", Turn.quarter()),
        ("eighth-turn", Turn.eighth()),
        ("sixteenth-turn", Turn.division(1, 16)),
    ]
    for idx, (name, t_val) in enumerate(td_entries, start=1):
        td_tablet.put(idx, t_val)
        td_tablet.put(name, t_val)
    tablets.append(td_tablet)

    # 13. Ea-nāṣir Copper Shipment (Thematic Inspiration: UET V 72)
    ea_nasir_metadata = TabletMetadata(
        title="Ea-nāṣir copper shipment",
        kind=TabletKind.DATA,
        historical_tag=HistoricalTag.MODERN,
        period="Old Babylonian (Ur, c. 1750 BCE thematic context)",
        confidence="high",
        source="Inspired by tablet UET V 72 (British Museum BM 131236)",
        provenance="Modern fictionalized computational example",
        notes="Fictionalized computational data inspired by the Ea-nāṣir copper complaint tablet. Not a historical transcription.",
    )
    ea_nasir_tablet = WorkingTablet("ea-nasir-shipment", shape=TabletShape.TABLE, kind=TabletKind.DATA, metadata=ea_nasir_metadata)
    ea_nasir_entries = [
        ("merchant", "Ea-nāṣir"),
        ("promised-quantity", Quantity(10, lookup_unit("talent"))),
        ("delivered-quantity", Quantity(10, lookup_unit("talent"))),
        ("required-quality", Rational(1)),
        ("actual-quality", Rational(45, 60)),  # 0;45
    ]
    for k, v in ea_nasir_entries:
        ea_nasir_tablet.put(k, v)
    tablets.append(ea_nasir_tablet)

    return tablets


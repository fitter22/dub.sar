# Examples Catalog

DUB.SAR includes a variety of executable sample tablets illustrating historical calculations and modern algorithms. Every example is provided in both **Scholar Mode** (`*_scholar.dub`) and **Canonical Cuneiform Tablet Mode** (`*.dub`).

---

## Historical Mesopotamian Archaeology

- **Babylonian Square Root of 2** (`examples/babylonian_sqrt2.dub`, `examples/babylonian_sqrt2_scholar.dub`):
  Computes $\sqrt{2}$ using the iterative Heron-Babylonian reciprocal method from tablet YBC 7289 ($1;24,51,10$).
- **Pythagorean Triples & Plimpton 322** (`examples/geometry_triangle.dub`, `examples/geometry_triangle_scholar.dub`):
  Constructs exact right triangles, verifies Pythagorean consistency, and determines inclination and feed ratios.
- **Ea-Nasir Copper Trade Dispute & Audit** (`examples/ea_nasir.dub`, `examples/ea_nasir_scholar.dub`, `examples/ea_nasir_revision.dub`, `examples/ea_nasir_revision_scholar.dub`):
  Formalizes the famous Ur copper dispute (tablet UET V 72) as a persistent archive audit workflow, computing quality deficiencies and recording versioned verdicts.

---

## Tablet Data Model & Sequences

- **Reciprocal Table Lookup** (`examples/reciprocal_lookup.dub`, `examples/reciprocal_lookup_scholar.dub`):
  Consults the standard mathematical reference tablet `reciprocals` and executes exact division via reciprocal multiplication.
- **Sequence Generation** (`examples/sequence_generation.dub`, `examples/sequence_generation_scholar.dub`):
  Allocates a working sequence tablet, computes Fibonacci-style terms, and inspects length, first, and last entries.
- **Sequence Transformation** (`examples/sequence_transformation.dub`, `examples/sequence_transformation_scholar.dub`):
  Iterates over observation sequence entries using bounded `consider` loops to construct transformed series.
- **Persistent Inscribed Sequences** (`examples/persistent_sequence.dub`, `examples/persistent_sequence_scholar.dub`):
  Inscribes a computed sequence into the persistent archive and verifies immutable version retrieval.

---

## Geometric & Fourier Mathematics

- **Right Triangles & Slopes** (`examples/geometry_triangle.dub`, `examples/geometry_triangle_scholar.dub`):
  Solves missing triangle sides, verifies integer right triangles, and extracts area and diagonal fields.
- **Geometric Inclinations, Feeds & Turns** (`examples/geometric_inclination.dub`, `examples/geometric_inclination_scholar.dub`):
  Calculates canal ramp inclination ($rise/run$) and feed ($run/rise$), builds directed quantities, and rotates by turn fractions.
- **Discrete & Fast Fourier Transforms (DFT / Radix-2 FFT)** (`examples/fourier_dft.dub`, `examples/fourier_dft_scholar.dub`):
  Computes reference $O(N^2)$ DFT and recursive Cooley-Tukey Radix-2 FFT ($O(N \log N)$) on directed quantity sequence tablets, verifying energy conservation and inverse reconstruction.

---

## Numerical Algorithms & Calendar Astronomy

- **Planetary Leap Cycle Search** (`examples/planetary_leap.dub`, `examples/planetary_leap_scholar.dub`):
  Searches candidate astronomical periods to determine optimal intercalation leap-year cycles.
- **Even Intercalation Distribution** (`examples/even_distribution.dub`, `examples/even_distribution_scholar.dub`):
  Distributes leap days uniformly across calendar cycles using exact Bresenham accumulator arithmetic.
- **Unit Conversions & Dimensional Safety** (`examples/unit_conversion.dub`, `examples/unit_conversion_scholar.dub`):
  Demonstrates compile-time dimensional checking and conversions across supported metrological units with defined conversion factors.
- **Persistent Tablet Archives & Lineage** (`examples/tablet_archive.dub`, `examples/tablet_archive_scholar.dub`):
  Illustrates multi-tablet archival persistence, working tablet scratchpads, and versioned lineage derivation.
- **Language Conformance Suite** (`examples/conformance.dub`, `examples/conformance_scholar.dub`):
  Comprehensive verification of arithmetic, unit metrology, procedures, and determination records.

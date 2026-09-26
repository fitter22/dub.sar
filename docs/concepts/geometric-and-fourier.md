# Geometric & Fourier Mathematics

DUB.SAR extends its mathematical model toward advanced numerical mathematics and harmonic analysis through an 8-layer progression grounded in ancient Mesopotamian scribal geometry:

```text
Exact Quantity (Universal Bedrock)
      │
      ▼
Ratio & Reciprocal
      │
      ▼
Geometric Determination (Right Triangles)
      │
      ▼
Inclination & Feed (Proportional Geometry)
      │
      ▼
Direction Abstraction (Ray Orientations)
      │
      ▼
The Turn System (Equal Circular Divisions)
      │
      ▼
Directed Quantities (Magnitude + Direction)
      │
      ▼
Tablet Fourier Mathematics (DFT & Radix-2 FFT)
```

Rather than bolting on modern floating-point primitives (`sin`, `cos`, `tan`, `exp(iθ)`, `complex`), DUB.SAR builds harmonic analysis organically from exact ratios, tablet sequences, and directed quantities.

---

## 1. The 8 Geometric & Fourier Layers

### Layer A: Exact Quantity and Ratio (Universal Bedrock) `[attested]`
Every mathematical calculation in DUB.SAR operates on arbitrary-precision exact rationals ($p/q$) with compile-time algebraic dimensional safety. Quantities multiply, divide, and invert without silent floating-point conversions. Ratios and reciprocals are exact scribal pairings.

### Layer B: Geometric Determinations and Right Triangles `[attested]`
Mesopotamian mathematics calculated with squares, square roots, and right triangles centuries before Pythagoras:

- **Exact Squares & Roots**: `square` and `square-root` compute exact integer squares and roots.
- **Right Triangle Determination**: `right-triangle` constructs a structured determination with fields `width`, `length`, `diagonal`, and boolean `is_valid` ($w^2 + l^2 = d^2$).
- **Missing Side Solver**: Given any two sides, `right-triangle` solves for the exact missing third side (or errors if non-integer).
- **Pythagorean Validation**: `validate-triangle` verifies whether three sides form a true integer right triangle.

```dubsar
problem
    tri : 3 4 right-triangle
    hypotenuse : tri.diagonal
    valid : tri validate-triangle
result
    hypotenuse
```

> **Scholarly Note on Plimpton 322**:
> Tablet Plimpton 322 (c. 1820–1762 BCE, Larsa) contains 15 rows of right triangle parameters. DUB.SAR maintains scholarly neutrality between:
>
> 1. **Eleanor Robson's scribal/pedagogical analysis**: Reciprocal pairs $(x, 1/x)$ generated within Old Babylonian scribal schooling.
> 2. **Mansfield & Wildberger's ratio-based trigonometry**: Exact ratio-based right-triangle geometry without circular angles.
>
> Both perspectives validate DUB.SAR's ratio-based geometric model.

### Layer C: Inclination, Feed, and Proportional Geometry `[attested]`
Ancient canal, ramp, and ziggurat construction relied on proportional slopes rather than modern angles:

- **Inclination (*mūlû*)**: $\text{rise} / \text{run}$ — vertical rise per unit horizontal run.
- **Feed (*mūrqītu* / *šikittum*)**: $\text{run} / \text{rise}$ — horizontal setback per unit vertical rise.
- The `inclination` operator consumes `run` and `rise` to produce a determination with fields `rise`, `run`, `inclination`, and `feed`.
- The `feed` operator computes the reciprocal ratio directly.

### Layer D: Direction Abstraction `[reconstructed]`
Direction in DUB.SAR represents an invariant ray orientation:

- Constructed from orthogonal components: `(run, rise) direction`.
- Constructed from circular fractions: `T direction` (where $T$ is a turn).
- Normalizes to unit components without exposing transcendental functions (`horizontal` and `vertical` coordinates).

### Layer E: The Turn System `[attested / reconstructed]`
A turn represents a fraction of a full revolution $p/q \in [0, 1)$:

- Declared as `(p, q) turn`, capturing quarter-turns ($1/4$), half-turns ($1/2$), and sexagesimal steps ($1/60$, $1/360$).
- Addition, subtraction, and scaling wrap cyclically modulo $1$.

> **Historical Dating of the 360-Degree Division**:
> The 360-degree division of the circle was **not** a Sumerian invention. It was developed in **5th-century BCE Babylonian astronomy** (Achaemenid period, post-450 BCE) for the mathematical zodiac, dividing the ecliptic into 12 equal signs of 30 degrees.

### Layer F: Directed Quantities `[reconstructed]`
A directed quantity binds a physical magnitude to an invariant direction:

- Constructed via `(magnitude, direction) directed`.
- Supports vector addition, scalar scaling, and rotation: `Q T rotate`.
- Rotation composes directions by adding turn fractions: $\text{Turn}_A + \text{Turn}_B \pmod 1$.

### Layer G: Explicit Approximate Determinations `[reconstructed]`
When irrationals arise (such as the diagonal of a unit square, $\sqrt{2}$ on tablet YBC 7289):

- DUB.SAR never silently converts to IEEE float.
- Explicit approximation via `X approximate` executes bounded Babylonian Heron iterations:
  $$x_{n+1} = \frac{1}{2}\left(x_n + \frac{S}{x_n}\right)$$
- Yields a determination with fields `value` (rational estimate), `iterations`, and `error_bound`.

### Layer H: Fourier Mathematics on Tablets (DFT & FFT) `[modern]`
DUB.SAR synthesizes ancient tablet sequences and directed rotations into modern harmonic analysis:

- **Sequence Tablet as Signal**: Time-domain and frequency-domain signals are represented purely as sequence tablets of directed quantities.
- **Harmonic Roots of Unity**: Rotations by $W_N^k = \text{turn}(-k/N)$ replace complex exponentials $e^{-2\pi i k / N}$.
- **Reference Discrete Fourier Transform (`dft`)**:
  $$X[k] = \sum_{n=0}^{N-1} x[n] \cdot \text{turn}\left(-\frac{k \cdot n}{N}\right)$$
- **Radix-2 Fast Fourier Transform (`fft`)**: Recursive Cooley-Tukey decimation-in-time algorithm for sequences of length $N = 2^m$.
- **Inverse Transforms (`inverse-dft`, `inverse-fft`)**: Normalized exact reconstruction ($1/N$ factor) satisfying energy conservation (Parseval's theorem).

---

## 2. First-Class Geometric & Fourier Operations

| Operation | Scholar Mode (Prefix / Postfix) | Canonical Cuneiform | Semantics |
| :--- | :--- | :--- | :--- |
| **Square** | `X square` | `X 𒉏` | Computes $X \cdot X$ |
| **Square Root** | `X square-root` | `X square-root` | Computes exact integer $\sqrt{X}$ (errors if non-square) |
| **Right Triangle** | `w l d right-triangle` | `w l d right-triangle` | Constructs right triangle determination; solves missing side |
| **Validate Triangle** | `w l d validate-triangle` | `w l d validate-triangle` | Validates if $w^2 + l^2 = d^2$ (returns 1 or 0) |
| **Inclination** | `run rise inclination` | `run rise inclination` | Constructs determination with `rise`, `run`, `inclination`, `feed` |
| **Feed** | `run rise feed` | `run rise feed` | Computes horizontal feed ratio ($\text{run} / \text{rise}$) |
| **Direction** | `dx dy direction` | `dx dy direction` | Constructs direction from orthogonal run/rise components |
| **Turn** | `p q turn` | `p q turn` | Constructs turn fraction $p/q \pmod 1$ |
| **Directed Quantity** | `mag dir directed` | `mag dir directed` | Binds scalar magnitude to directional ray |
| **Rotation** | `Q T rotate` | `Q T rotate` | Rotates directed quantity $Q$ by turn $T$ |
| **Approximation** | `X approximate` | `X approximate` | Computes bounded Heron-method rational approximation |
| **Discrete Fourier Transform** | `S dft` | `S dft` | Computes reference $O(N^2)$ DFT on sequence tablet $S$ |
| **Fast Fourier Transform** | `S fft` | `S fft` | Computes Cooley-Tukey $O(N \log N)$ FFT for length $2^m$ |
| **Inverse DFT** | `S inverse-dft` | `S inverse-dft` | Computes normalized inverse DFT reconstruction |
| **Inverse FFT** | `S inverse-fft` | `S inverse-fft` | Computes normalized inverse Radix-2 FFT reconstruction |

---

## 3. Historical Provenance Framework

To maintain scientific and historical integrity, DUB.SAR categorizes all mathematical constructs into explicit provenance tiers:

- **`[attested]`**: Directly verified in excavated cuneiform tablets.
  - Reciprocal tables, multiplication tables, squares, cubes.
  - Right triangle relationships (Plimpton 322, BM 85196, BM 34568).
  - Inclinations and feeds for embankments and ramps (*mūlû*, *mūrqītu*).
  - 360-degree circular division in 5th-century BCE Babylonian astronomy.
- **`[reconstructed]`**: Historically plausible scribal formalizations.
  - Direction abstraction based on run/rise ratios.
  - Rational turn arithmetic.
  - Bounded approximation determinations.
- **`[modern]`**: 20th-century computational mathematics synthesized into Mesopotamian paradigm.
  - Discrete Fourier Transform (DFT).
  - Radix-2 Cooley-Tukey Fast Fourier Transform (FFT).
  - Sequence-tablet harmonic decomposition without complex numbers.

---

## 4. Canonical Examples

Complete, runnable examples of geometric and Fourier computation in the repository include:

- **Right Triangles & Pythagorean Geometry** (`examples/geometry_triangle_scholar.dub` / `examples/geometry_triangle.dub`): Solves missing hypotenuse, validates triangle triples, and consults the `right-triangles` archival tablet.
- **Slopes, Feeds & Directed Quantities** (`examples/geometric_inclination_scholar.dub` / `examples/geometric_inclination.dub`): Computes canal ramp inclination, feed, constructs directed vectors, and performs quarter-turn rotations.
- **Fourier Transform & Harmonic Analysis** (`examples/fourier_dft_scholar.dub` / `examples/fourier_dft.dub`): Verifies sequence length against `powers-of-two`, generates harmonic signal, executes both reference DFT and recursive Radix-2 FFT, and reconstructs signal via inverse DFT.

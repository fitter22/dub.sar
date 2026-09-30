# Using the Native Compiler

DUB.SAR 1.0 provides an ahead-of-time (AOT) native compiler backend that translates mathematical tablets into high-performance C99 source code and compiles them into standalone machine binaries, shared libraries, or LLVM intermediate representation.

---

## 1. Prerequisites and Host Toolchain

The native compiler relies on a standard host C compiler:

- **Clang** (`clang`): The recommended and default compiler on macOS and modern Linux systems. Required when generating textual LLVM IR (`--target=llvm`).
- **GCC** (`gcc`): Supported on Linux, BSD, and Windows (via MinGW-w64 or WSL).
- **Generic CC** (`cc`): Any POSIX-compliant C99 compiler available on the system `$PATH`.

The compiler driver auto-detects the host toolchain by searching for `clang`, `gcc`, and `cc` in order. If no C compiler is found, the native backend issues an informative error explaining that `clang` or `gcc` is required.

To verify your host compiler installation:

```bash
clang --version
# or
gcc --version
```

---

## 2. Running Tablets Natively

You can compile and execute a tablet in a single command using the `run` command with the native backend:

```bash
dubsar run tablet.dub --backend=native
```

### Execution Semantics

When invoked with `--backend=native`:

1. The tablet is tokenized, parsed, and semantically verified.
2. The program is lowered to Semantic IR and translated into optimized C99 source code linked against the DUB.SAR runtime (`dubsar_runtime.h` and `dubsar_runtime.c`).
3. The host compiler builds a temporary machine binary.
4. The binary executes immediately, streaming inscribed results directly to standard output.
5. All temporary compilation artifacts are cleaned up automatically upon exit.

### Supplying Input

Interactive tablets that use the `ask` verb or `𒀀𒁹` sign can receive preset values via the `--input` flag:

```bash
dubsar run survey.dub --backend=native --input="45"
```

The native runner passes this value to the program environment via command-line arguments, where the runtime initializes input streams prior to executing the tablet problem body.

### Backend-Specific Considerations

The native runner executes compiled machine code directly rather than executing through the Python runtime:

- **Tablet Archives**: The native backend executes bare-metal binaries and does not open SQLite database connections. The `--archive` option is ignored.
- **Output Formatting**: The native runtime emits canonical numeric and rational representations directly (such as `42` or `0;50`). Presentation flags (`--format=decimal`, `--format=sexagesimal`) apply to the VM and AST interpreter backends.

---

## 3. Ahead-of-Time Compilation Targets

Use `dubsar compile` to produce persistent binaries, source files, or libraries:

```bash
dubsar compile <file.dub> --target=<target> [-o <output>] [--opt-level=<level>]
```

### Available Targets

| Target | Alias | Output Extension | Description | Intended Use Case |
| :--- | :--- | :--- | :--- | :--- |
| `native` | - | None (executable) | Standalone machine binary (Mach-O on macOS, ELF on Linux) | High-performance CLI tools, batch numerical jobs |
| `c` | - | `.c` | Standalone ANSI C99 source code | Auditing, manual integration into existing C/C++ codebases, embedded targets |
| `llvm` | `ll` | `.ll` | Textual LLVM Intermediate Representation | LLVM analysis passes, link-time optimization (LTO), custom toolchains |
| `shared` | `dylib`, `so` | `.dylib` (macOS) / `.so` (Linux) | Position-independent shared dynamic library (`-fPIC -shared`) | Foreign Function Interface (FFI) embedding in Python, Rust, Go, or Java |

### Target Usage Examples

#### Standalone Native Executable

Compile directly into a standalone machine binary:

```bash
dubsar compile tablet.dub --target=native -o tablet_bin
./tablet_bin
```

If `-o` is omitted, the executable is written to the source file stem in the current directory (for example, `tablet`).

#### ANSI C99 Source Code

Emit clean, human-readable C99 source code. The emitted source code is self-contained and requires only the DUB.SAR C runtime headers/sources and the host C math library (`-lm`), with no third-party package dependencies:

```bash
dubsar compile tablet.dub --target=c -o tablet.c
```

The emitted C source includes `dubsar_runtime.h` and can be compiled manually with any C99 compiler by including and linking `dubsar_runtime.c` alongside `-lm`:

```bash
clang -O3 -I/path/to/dubsar/native/runtime tablet.c /path/to/dubsar/native/runtime/dubsar_runtime.c -lm -o tablet
```

#### Textual LLVM Intermediate Representation

Emit optimized textual LLVM IR:

```bash
dubsar compile tablet.dub --target=llvm -o tablet.ll
```

Generating LLVM IR invokes `clang -S -emit-llvm -O3` under the hood.

#### Dynamically Linked Shared Library

Compile as a shared library for embedding in host applications:

```bash
# On macOS (produces libtablet.dylib)
dubsar compile tablet.dub --target=shared -o libtablet.dylib

# On Linux (produces libtablet.so)
dubsar compile tablet.dub --target=shared -o libtablet.so
```

---

## 4. Compiler Optimization Flags

The native compiler passes optimization flags directly to the host C compiler via `--opt-level`:

| Flag | Meaning | Use Case |
| :--- | :--- | :--- |
| `-O0` | No optimization | Fastest compilation time, debugging with `gdb` or `lldb` |
| `-O1` | Basic optimization | Modest code optimization with short compile times |
| `-O2` | Recommended optimization | Comprehensive optimizations without heavy code size inflation |
| `-O3` | Aggressive optimization *(default)* | Maximum runtime throughput, loop vectorization, aggressive inlining |
| `-Os` | Optimize for code size | Minimizes binary size while retaining `-O2` optimizations |
| `-Oz` | Extreme size reduction (Clang) | Aggressive code size reduction, ideal for resource-constrained environments |

Example:

```bash
dubsar compile tablet.dub --target=native --opt-level=-O3 -o tablet_fast
dubsar compile tablet.dub --target=native --opt-level=-Os -o tablet_small
```

---

## 5. Platform Considerations

### macOS (Darwin)

- **Default Toolchain**: Apple Clang (`/usr/bin/clang`), installed via Xcode or Command Line Tools (`xcode-select --install`).
- **Binary Format**: Mach-O 64-bit executable.
- **Shared Libraries**: `.dylib` extension.
- **Architecture**: Universal support for Apple Silicon (`arm64`) and Intel (`x86_64`). Hardware 128-bit integer operations (`__int128_t`) are supported natively on both architectures.

### Linux

- **Default Toolchain**: GCC (`gcc`) or Clang (`clang`).
- **Binary Format**: ELF 64-bit executable.
- **Shared Libraries**: `.so` extension.
- **Math Library**: The native compiler links the standard math library (`-lm`) automatically for transcendental and geometric helpers.
- **Architecture**: 64-bit x86_64, AArch64, and RISC-V targets provide native `__int128_t` hardware acceleration.

### Rational Storage and 128-bit Intermediate Accumulation

The DUB.SAR native and WebAssembly runtimes store rational numbers using bounded 64-bit signed integers for both numerator and denominator (`dubsar_rat_t` with `int64_t num; int64_t den;`). This differs from the Python AST Interpreter and Bytecode VM backends, which use Python's unbounded arbitrary-precision integers.

On 64-bit platforms where `__SIZEOF_INT128__` is supported by Clang or GCC, the native runtime uses 128-bit integers (`__int128_t`) for intermediate cross-product calculation:

$$\frac{a}{b} \pm \frac{c}{d} = \frac{a \cdot d \pm b \cdot c}{b \cdot d}, \quad \frac{a}{b} \cdot \frac{c}{d} = \frac{a \cdot c}{b \cdot d}$$

This wider intermediate accumulation substantially reduces the likelihood of intermediate overflow during additions, subtractions, and multiplications prior to reduction by the greatest common divisor (GCD).

However, after GCD reduction, the reduced numerator and denominator are cast back into bounded 64-bit integer storage (`int64_t`). The native runtime does not provide unbounded arbitrary-precision arithmetic; if the final reduced rational value exceeds 64-bit signed limits, numeric overflow will occur. On platforms lacking 128-bit compiler support, the runtime falls back to factorized 64-bit GCD arithmetic.

---

## 6. End-to-End Walkthrough

This walkthrough demonstrates writing, validating, compiling, and running a complete mathematical tablet using the native backend.

### Step 1: Author the Tablet

Create a file named `right_triangle.dub`:

<!-- test-id: compiler-native-walkthrough -->
```dubsar
problem
    width : 15
    height : 20
    w_sq : width width multiply
    h_sq : height height multiply
    hyp_sq : w_sq h_sq add
    hyp : hyp_sq square-root
result
    hyp
```

### Step 2: Validate the Tablet

Perform static checking to ensure metrological units and syntax are valid:

```bash
dubsar check right_triangle.dub
```

Output:

```text
[OK] Tablet 'right_triangle.dub' parsed and verified successfully (Mode: scholar).
```

### Step 3: Run with the Native Backend

Execute immediately using the AOT native runner:

```bash
dubsar run right_triangle.dub --backend=native
```

Output:

```text
25
```

### Step 4: Compile to a Standalone Binary

Produce an optimized standalone executable:

```bash
dubsar compile right_triangle.dub --target=native --opt-level=-O3 -o right_triangle
```

Execute the compiled machine binary directly:

```bash
./right_triangle
```

Output:

```text
25
```

### Step 5: Inspect Generated C99 Source

Inspect the generated C source code to see how the mathematical statements were lowered:

```bash
dubsar compile right_triangle.dub --target=c -o right_triangle.c
head -n 25 right_triangle.c
```

The output reveals clean C99 code utilizing `dubsar_rat_t` exact rational primitives and runtime math calls.

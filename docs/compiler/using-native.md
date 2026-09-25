# Using the Native Compiler

DUB.SAR 1.0 includes an ahead-of-time (AOT) native compiler targeting modern C99 compilers (`clang` or `gcc`).

---

## Compilation Targets

### Standalone Executable
Compile directly into a machine binary:

```bash
dubsar compile tablet.dub -o tablet_bin --target=native
./tablet_bin
```

### Shared Dynamic Library
Compile as a shared library (`.so` on Linux, `.dylib` on macOS) for embedding in host applications:

```bash
dubsar compile tablet.dub -o libtablet.so --target=shared
```

### Clean C99 Source Code
Emit standalone, human-readable C99 source code with zero external library dependencies:

```bash
dubsar compile tablet.dub -o tablet.c --target=c
```

### Textual LLVM IR
Emit optimized textual LLVM IR (`.ll`):

```bash
dubsar compile tablet.dub -o tablet.ll --target=llvm
```

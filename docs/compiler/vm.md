# Virtual Machine

DUB.SAR includes a stack-oriented bytecode virtual machine for portable execution.

---

## Bytecode Design

The VM operates on a stack with explicit opcodes:

- `CONST`: Push constant value onto stack.
- `LOAD`, `STORE`: Access local and global lexical environments.
- `ADD`, `SUB`, `MUL`, `DIV`, `REM`, `POW_INT`: Rational stack arithmetic.
- `CMP`: Compare stack operands.
- `JUMP`, `JUMP_IF_FALSE`: Conditional branching and loop execution.
- `CALL`, `RETURN`: Procedure frame invocation.

---

## Running on the VM

```bash
dubsar run tablet.dub --backend=vm
```

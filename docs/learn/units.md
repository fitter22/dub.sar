# 4. Units & Dimensional Safety

Physical numbers in DUB.SAR carry explicit unit dimensions. Operations between quantities enforce strict dimensional consistency.

---

## Supported Metrological Systems

DUB.SAR provides both built-in standard units with defined conversion scales and extensible dynamic dimensions:

- **Standard Length**: `meter`, `cubit` (`kus` / `kùš` / `kush3`), `finger` (`su-si` / `shu-si`), `reed` (`gi`), `nindan` (rod = 12 cubits).
- **Standard Time**: `second`, `minute`, `hour`, `day` (`ud` / `𒌓`).
- **Standard Mass**: `mina` (`ma-na` / `𒈠𒈾`), `talent` (`gun` / `𒄘`).
- **Calendar Dimensions**: `month` (`iti` / `𒌗`), `year` (`mu` / `𒈬`).
- **Dynamic Custom Units**: User-defined unit labels (such as `shekel`, `silver`, `copper`, `sila3`, `sar`, `step`) automatically form custom base dimensions.

---

## Dimensional Verification

Operations between quantities automatically enforce dimensional rules:

```dubsar
problem
    rod : 2 nindan
    depth : 1 kush3
    # 1 nindan = 12 kush3 (cubits), so 1 kush3 = 1/12 = 0;5 nindan
    length_sum : rod + depth
result
    length_sum
```

Output:
```text
2;5 nindan
```

Because 1 `nindan` equals 12 `kush3`, adding 1 `kush3` ($1/12 = 5/60 = 0;5\text{ nindan}$) to 2 `nindan` evaluates to the exact sexagesimal quantity `2;5 nindan`.

Multiplying two lengths yields an area quantity. Dividing distance by time yields speed. Adding incompatible dimensions (such as adding length to time) produces an immediate compile error:

```text
Cannot perform '+' between incompatible units: 'meter' and 'second'
```

---

## Further Reading & Reference

- **[Language Guide: Units & Metrology](../guide/units.md)**: Deep dive into the metrological dimension hierarchy and conversion rules.
- **[Language Reference: Units of Measurement](../reference/units.md)**: Complete catalog of standard lengths, times, masses, and custom dimensions.
- **[Core Concepts: Dimensional Mathematics](../concepts/dimensional-mathematics.md)**: Theoretical foundations of algebraic dimensional type safety.

# 4. Units & Dimensional Safety

Physical numbers in DUB.SAR carry explicit unit dimensions. Operations between quantities enforce dimensional consistency.

---

## Supported Metrological Systems

DUB.SAR includes both modern SI units and historical Mesopotamian units:

- **Length**: `meter`, `centimeter`, `millimeter`, `kilometer`, and Mesopotamian `shu-si` (finger), `kush3` (cubit), `nindan` (rod), `danna` (league).
- **Area**: `sq_meter`, `sar` (garden plot), `iku` (field), `bur3`.
- **Volume & Capacity**: `liter`, `sila3` (bowl), `ban2`, `barig`, `gur` (royal bushel).
- **Mass & Weight**: `gram`, `kilogram`, `she` (grain), `gin2` (shekel), `mana` (mina), `gun2` (talent).
- **Time**: `second`, `minute`, `hour`, `day`, `year`, `gesh` (double hour).

---

## Dimensional Verification

Operations between quantities automatically check dimensional rules:

```dubsar
problem:
    rod : 2 nindan
    depth : 1 kush3
    # rod + depth converts to base meters correctly
    length_sum := rod + depth
result:
    length_sum
```

Multiplying two lengths yields an area quantity. Dividing distance by time yields speed. Adding length to time produces an immediate compile error.

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

Operations between quantities automatically check dimensional rules:

```dubsar
problem
    rod : 2 nindan
    depth : 1 kush3
    # rod + depth converts to common length dimension
    length_sum := rod + depth
result
    length_sum
```

Multiplying two lengths yields an area quantity. Dividing distance by time yields speed. Adding length to time produces an immediate compile error.

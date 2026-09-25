# Units & Metrology

DUB.SAR features compile-time dimensional analysis and conversion between modern metric and historical Mesopotamian units.

---

## Unit Conversions

The `convert(qty, target_unit)` built-in converts quantities between compatible dimensions:

```dubsar
problem:
    field_len : 1 nindan
    in_meters := convert(field_len, "meter")
result:
    in_meters
```

---

## Metrological Table

| Quantity | Historical Unit | Cuneiform | Modern Equivalent |
| :--- | :--- | :--- | :--- |
| Length | 1 `shu-si` (finger) | `𒋗𒋛` | 1.667 cm |
| Length | 1 `kush3` (cubit) | `𒌑` | 30 `shu-si` = 50 cm |
| Length | 1 `nindan` (rod) | `𒃻` | 12 `kush3` = 6 m |
| Area | 1 `sar` | `𒊬` | 1 `nindan` x 1 `nindan` = 36 m² |
| Area | 1 `iku` | `𒃷` | 100 `sar` = 3,600 m² |
| Capacity | 1 `sila3` | `𒋡` | ~1.0 liter |
| Capacity | 1 `gur` | `𒄥` | 300 `sila3` = ~300 liters |
| Mass | 1 `gin2` (shekel) | `𒂆` | ~8.33 grams |
| Mass | 1 `mana` (mina) | `𒈠𒈾` | 60 `gin2` = ~500 grams |
| Mass | 1 `gun2` (talent) | `𒄘` | 60 `mana` = ~30 kilograms |

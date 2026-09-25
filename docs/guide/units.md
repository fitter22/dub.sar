# Units & Metrology

DUB.SAR features compile-time dimensional analysis, strict unit homogeneity, and explicit conversion between compatible standard units.

---

## Standard Implemented Units vs Dynamic Dimensions

DUB.SAR distinguishes between two categories of units:

1. **Standard Implemented Units**: Built-in units belonging to predefined physical dimensions (`time`, `mass`, `length`, `month`, `year`) with known scale factors that support conversion via `convert(qty, target_unit)`.
2. **Custom / Dynamic Dimensions**: Any unrecognized unit identifier (such as `silver`, `copper`, `shekel`, `liter`, or `step`) is automatically instantiated as an independent base dimension. Dynamic dimensions enforce strict dimensional consistency ($A + B$ requires identical units) and compose algebraically under multiplication and division, but cannot convert across different dimension names.

---

## Unit Conversions

The `convert(qty, target_unit)` built-in converts quantities sharing the same physical dimension:

```dubsar
problem
    duration : 1 day
    in_hours := convert(duration, "hour")

    weight : 2 talent
    in_minas := convert(weight, "mina")
result
    in_hours
    in_minas
```

---

## Standard Metrological Units Table

| Dimension | Unit Identifiers | Cuneiform Sign | Scale / Conversion |
| :--- | :--- | :---: | :--- |
| **Time** | `second`, `sec` | - | $1\text{ s}$ (base unit) |
| **Time** | `minute`, `min` | - | $60\text{ second}$ |
| **Time** | `hour`, `hr` | - | $60\text{ minute} = 3600\text{ second}$ |
| **Time** | `day`, `ud` | `𒌓` | $24\text{ hour} = 86400\text{ second}$ |
| **Calendar** | `month`, `iti` | `𒌗` | $1\text{ month}$ (independent calendar dimension) |
| **Calendar** | `year`, `mu` | `𒈬` | $1\text{ year}$ (independent astronomical dimension) |
| **Mass** | `mina`, `ma-na` | `𒈠𒈾` | $60\text{ shekels}$ (base mass scale) |
| **Mass** | `talent`, `gun` | `𒄘` | $60\text{ mina} = 3600\text{ shekels}$ |
| **Length** | `su-si`, `finger` | - | $1/30\text{ cubit}$ |
| **Length** | `kus`, `kùš`, `cubit` | - | $1\text{ cubit}$ (base length scale) |
| **Length** | `gi`, `reed` | `𒄀` | $6\text{ cubits}$ |
| **Length** | `nindan` | - | $12\text{ cubits}$ |
| **Length** | `meter`, `m` | - | $1\text{ standard length}$ |

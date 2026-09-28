# Units Reference

Comprehensive catalog of supported physical, astronomical, and metrological units in DUB.SAR.

---

## 1. Standard Units Table

DUB.SAR embeds standard conversion scale factors for units in the physical dimensions of `time`, `mass`, and `length`, as well as discrete abstract calendar dimensions.

### Time Units (Base Dimension: `time`)

| Unit Identifier | Alternative Aliases | Cuneiform Sign | Scale (Seconds) | Ratio to Base |
| :--- | :--- | :---: | :--- | :--- |
| `second` | `sec` | - | $1\text{ s}$ | $1$ (base unit) |
| `minute` | `min` | - | $60\text{ s}$ | $60\text{ second}$ |
| `hour` | `hr` | - | $3600\text{ s}$ | $60\text{ minute}$ |
| `day` | `ud` | `𒌓` | $86400\text{ s}$ | $24\text{ hour}$ |

### Calendar Dimensions

Mesopotamian astronomical and calendar calculations treat months and years as discrete, independent cycle dimensions:

| Unit Identifier | Alternative Aliases | Cuneiform Sign | Base Dimension | Scale |
| :--- | :--- | :---: | :--- | :--- |
| `month` | `iti` | `𒌗` | `month` | $1$ (abstract calendar cycle) |
| `year` | `mu` | `𒈬` | `year` | $1$ (abstract astronomical cycle) |

> [!NOTE]
> In DUB.SAR, `month` and `year` are distinct abstract dimensions (`{"month": 1}` and `{"year": 1}`), each with scale 1. They are not units within the `time` dimension and do not convert to `day`, `second`, or to each other.

### Mass & Weight Units (Base Dimension: `mass`)

| Unit Identifier | Alternative Aliases | Cuneiform Sign | Scale (Shekels) | Ratio to Mina |
| :--- | :--- | :---: | :--- | :--- |
| `mina` | `ma-na` | `𒈠𒈾` | $60$ | $1\text{ mina}$ (base unit) |
| `talent` | `gun` | `𒄘` | $3600$ | $60\text{ mina}$ |

### Length Units (Base Dimension: `length`)

The internal base unit for length is the Mesopotamian cubit (`kus` / `kùš` / `cubit`).

| Unit Identifier | Alternative Aliases | Cuneiform Sign | Scale (Mesopotamian Cubits) |
| :--- | :--- | :---: | :--- |
| `su-si` | `finger` | - | $1/30\text{ cubit}$ |
| `kus` | `kùš`, `cubit` | - | $1\text{ cubit}$ (base metrology unit) |
| `gi` | `reed` | `𒄀` | $6\text{ cubits}$ |
| `nindan` | - | - | $12\text{ cubits}$ |
| `meter` | `m` | - | Uncalibrated SI length unit (scale = 1) |

> [!NOTE]
> Historical Mesopotamian cubit lengths varied across periods and regions (such as the Classical Nippur cubit of $\approx 51.8\text{ cm}$). DUB.SAR preserves exact internal ratios within the historical sexagesimal metrology system (1 reed = 6 cubits, 1 nindan = 12 cubits), but deliberately avoids imposing an unverified conversion factor between historical cubits and modern SI meters.

---

## 2. Dynamic Custom Dimensions

Any unit name not present in the standard table above (e.g., `shekel`, `silver`, `copper`, `grain`, `liter`, `step`) is dynamically recognized by the compiler and interpreter as a distinct, first-class base dimension.

- **Dimensional Safety**: Quantities with dynamic units can be multiplied and divided to form composite dimensions (e.g., $10\text{ copper} \times 2\text{ silver} = 20\text{ copper}\cdot\text{silver}$).
- **Addition & Subtraction Homogeneity**: Quantities can only be added or subtracted if they share the exact identical dimension exponents.
- **Conversion Limits**: Explicit unit conversion requires both units to belong to the same base dimension with defined scaling factors. Converting across different dimensions causes a `DubSarUnitError`.

---

## 3. Unit Conversion Syntax

DUB.SAR supports explicit conversion through two canonical syntax forms:

1. **Built-in Function Call (indented under quantity establishment)**:
   ```syntax
   target :
       convert(quantity, "target_unit")
   ```
2. **Postfix Calculation Pipeline**:
   ```syntax
   target :
       quantity
       target_unit
       apply convert
   ```
   In authentic cuneiform Tablet Mode:
   ```syntax
   target :
       quantity target_unit 𒀝 convert
   ```

### Minimal Example

<!-- test-id: ref-units-conversion -->
```dubsar
problem
    duration : 1 day
    in_hours :
        convert(duration, "hour")

    weight : 2 talent
    in_minas :
        convert(weight, "mina")
result
    in_hours
    in_minas
```

Output:
```text
24 hour
120 mina
```

---

## 4. Related Documentation

- **Tutorial**: [Chapter 4: Units & Dimensional Safety](../learn/units.md)
- **Language Guide**: [Units & Metrology](../guide/units.md)
- **Language Reference**: [Units & Metrological Conversions](language.md#11-units-metrological-conversions)
- **Specification**: [DUB.SAR 1.0 Specification](../specification/index.md)

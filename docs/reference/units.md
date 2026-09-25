# Units Reference

Comprehensive catalog of supported physical, astronomical, and metrological units in DUB.SAR.

---

## 1. Standard Units Table

DUB.SAR embeds standard conversion scale factors for units in the physical dimensions of `time`, `mass`, `length`, `month`, and `year`.

### Time Units (Base Dimension: `time`)

| Unit Identifier | Alternative Aliases | Cuneiform Sign | Scale (Seconds) |
| :--- | :--- | :---: | :--- |
| `second` | `sec` | - | $1\text{ s}$ |
| `minute` | `min` | - | $60\text{ s}$ |
| `hour` | `hr` | - | $3600\text{ s}$ |
| `day` | `ud` | `𒌓` | $86400\text{ s}$ |

### Calendar Dimensions

Mesopotamian astronomical and calendar calculations treat months and years as discrete cycle dimensions:

| Unit Identifier | Alternative Aliases | Cuneiform Sign | Dimension |
| :--- | :--- | :---: | :--- |
| `month` | `iti` | `𒌗` | `month` |
| `year` | `mu` | `𒈬` | `year` |

### Mass & Weight Units (Base Dimension: `mass`)

| Unit Identifier | Alternative Aliases | Cuneiform Sign | Scale (Shekels) | Ratio to Mina |
| :--- | :--- | :---: | :--- | :--- |
| `mina` | `ma-na` | `𒈠𒈾` | $60$ | $1\text{ mina}$ |
| `talent` | `gun` | `𒄘` | $3600$ | $60\text{ mina}$ |

### Length Units (Base Dimension: `length`)

| Unit Identifier | Alternative Aliases | Cuneiform Sign | Scale (Cubits) |
| :--- | :--- | :---: | :--- |
| `su-si` | `finger` | - | $1/30\text{ cubit}$ |
| `kus` | `kùš`, `cubit` | - | $1\text{ cubit}$ |
| `gi` | `reed` | `𒄀` | $6\text{ cubits}$ |
| `nindan` | - | - | $12\text{ cubits}$ |
| `meter` | `m` | - | $1\text{ standard length}$ |

---

## 2. Dynamic Custom Dimensions

Any unit name not present in the standard table above (e.g., `shekel`, `silver`, `copper`, `grain`, `liter`, `step`) is dynamically recognized by the compiler and interpreter as a distinct, first-class base dimension.

- **Dimensional Safety**: Quantities with dynamic units can be multiplied and divided to form composite dimensions (e.g., $10\text{ copper} \times 2\text{ silver} = 20\text{ copper}\cdot\text{silver}$).
- **Addition & Subtraction Homogeneity**: Quantities can only be added or subtracted if they share the exact identical dimension exponents.
- **Conversion Limits**: Explicit unit conversion via `convert(qty, target_unit)` requires both units to belong to the same base dimension with defined scaling factors.

# Tablet Structure

DUB.SAR programs represent computational clay tablets (`IM.GID.DA`), structured into three formal scribal sections.

---

## The Three Sections

```
+------------------------------------+
|  Problem Section (e-diš / 𒂊𒁹)      |
|  - Inputs, parameters, assumptions |
+------------------------------------+
|  Procedures Section (dub-sar / 𒁾𒊬)|
|  - Named recipes and algorithms    |
+------------------------------------+
|  Result Section (ka-diš / 𒅗𒁹)       |
|  - Inscribed output and determinations
+------------------------------------+
```

### 1. Problem Section (`problem:` / `𒂊𒁹`)
Introduces given parameters and initial state:

```dubsar
problem:
    width : 10 meter
    height : 5 meter
```

### 2. Procedures Section (`recipe ...:` / `𒁾𒊬`)
Defines reusable mathematical algorithms:

```dubsar
procedure double_value(x):
    return x * 2
```

### 3. Result Section (`result:` / `𒅗𒁹`)
Specifies the outputs inscribed into clay:

```dubsar
result:
    double_value(width)
```

# Source Modes

DUB.SAR features a dual-layer syntax: **Tablet Mode** (authentic Unicode cuneiform signs) and **Scholar Mode** (Latin transliteration). Both compile into the exact same Abstract Syntax Tree.

---

## Tablet Mode

Uses authentic Unicode cuneiform signs:

```dubsar
𒂊𒁹
    a : 10
    b : 20
    c := a b 𒍣
𒅗𒁹
    c
```

---

## Scholar Mode

Uses readable Latin keywords and standard algebraic operators:

```dubsar
problem:
    a : 10
    b : 20
    c := a + b
result:
    c
```

---

## Sign Mapping Table

| Concept | Scholar Mode | Tablet Mode (Cuneiform) | Sumerian / Akkadian Reading |
| :--- | :--- | :--- | :--- |
| Problem Header | `problem` | `𒂊𒁹` | `e-diš` |
| Recipe Header | `recipe` / `procedure` | `𒁾𒊬` | `dub-sar` |
| Result Header | `result` | `𒅗𒁹` | `ka-diš` |
| Addition | `add` / `+` | `𒍣` | `zi` |
| Subtraction | `subtract` / `-` | `𒋫` | `ta` |
| Multiplication | `multiply` / `*` | `𒊭` | `ša` |
| Division | `divide` / `/` | `𒉌` | `ni` |
| Square | `square` | `𒅁` | `íb` |
| Square Root | `square-root` / `sqrt` | `𒁀𒋛` | `ba-si` |
| Loop / Domain | `consider ... through` | `𒄀 ... 𒌗` | `gi ... iti` |
| Retain | `retain` | `𒋼` | `te` |
| When | `when` | `𒂊𒀀` | `e-a` |

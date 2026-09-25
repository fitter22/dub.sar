# 1. Your First Tablet

In DUB.SAR, every program models an ancient clay tablet (`IM.GID.DA`). A tablet is divided into distinct scribal sections representing the problem setup, procedure algorithms, and the final recorded result.

---

## The Minimal Tablet

Every tablet begins with a **Problem Statement** and concludes with a **Result**:

```dubsar
problem:
    x : 40
    y : 2
    sum := x + y
result:
    sum
```

In cuneiform script (Tablet Mode):

```dubsar
𒂊𒁹
    𒊕 : 40
    𒅎 : 2
    𒁇 := 𒊕 + 𒅎
𒅗𒁹
    𒁇
```

---

## Sections Explained

- `problem:` (`𒂊𒁹` / `e-diš`): Declares known input variables, assumptions, and initial conditions.
- `result:` (`𒅗𒁹` / `ka-diš`): Specifies the values inscribed onto the tablet as output.
- `recipe:` (`𒁾𒊬` / `dub-sar`): Optional section for reusable mathematical procedures.

Variables declared with `:` are established bindings. Intermediate computations assigned with `:=` compute expressions.

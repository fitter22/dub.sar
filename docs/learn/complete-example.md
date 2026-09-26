# 10. Complete Example: Leap-Cycle Search

This comprehensive example brings together all the concepts covered in this tutorial series: exact sexagesimal arithmetic, stack calculation pipelines, bounded mathematical search, structured determinations, and atomic selection.

The problem searches for the optimal calendar intercalation cycle for a tropical year of $365.2422$ days across a horizon of 200 years, retaining the cycle that minimizes cumulative astronomical drift.

---

## Scholar Mode

```dubsar
problem
    solar-year : 365.2422
    limit : 200
    whole-days : solar-year floor
    fraction : solar-year whole-days subtract

    best : empty
    consider cycle from 1 through limit:
        leaps : cycle fraction multiply nearest
        approx : whole-days + (leaps / cycle)
        error : approx solar-year subtract absolute
        candidate : cycle, leaps, error
        retain candidate when error of candidate is lesser than error of best
result
    best.cycle
    best.leaps
    best.error
```

---

## Tablet Mode (Cuneiform)

```dubsar
𒂊𒁹
    𒈬 : 365.2422
    𒍠 : 200
    𒌓 : 𒈬 𒄥
    𒁇 : 𒈬 𒌓 𒋫

    𒊕 : 𒉡
    𒄀 𒁄 𒋫 1 𒂗 𒍠:
        𒋛 : 𒁄 𒁇 𒊭 𒊑
        𒈬𒁶 : 𒌓 𒋛 𒁄 𒉌 𒍣
        𒇲 : 𒈬𒁶 𒈬 𒋫 𒋼
        𒊮 : 𒁄, 𒋛, 𒇲
        𒋼 𒊮 𒂊𒀀 𒇲 𒊭 𒊮 𒌉 𒇲 𒊭 𒊕
𒅗𒁹
    𒊕
```

Both programs evaluate to the optimal 128-year intercalation cycle:

```text
128
31
0;0,0,2,42
```

---

## Mathematical and Algorithmic Walkthrough

The tablet executes in structured stages:

1. **Parameter Establishment**:
   - `solar-year` (`𒈬`): Set to $365.2422$ days.
   - `limit` (`𒍠`): Search upper bound set to $200$ years.
   - `whole-days` (`𒌓`): `solar-year floor` computes the base 365-day year using the `floor` (`𒄥`, *gur*) verb.
   - `fraction` (`𒁇`): Computes the fractional excess of $0.2422$ days per year using `subtract` (`𒋫`, *ta*).

2. **Sentinel Initialization**:
   - `best : empty` (`𒊕 : 𒉡`): Initializes the accumulator with the `empty` sentinel (`nu`, *lā*). The first comparison will unconditionally retain the initial candidate.

3. **Bounded Iteration**:
   - `consider cycle from 1 through limit:` (`𒄀 𒁄 𒋫 1 𒂗 𒍠:`): Iterates through cycle horizons $n \in [1, 200]$. Because loop bounds are strictly finite, execution is guaranteed to terminate.

4. **Candidate Estimation Pipeline**:
   - `leaps : cycle fraction multiply nearest` (`𒋛 : 𒁄 𒁇 𒊭 𒊑`): Multiplies cycle length by excess fraction and rounds to the nearest integer with `nearest` (`𒊑`, *ri*).
   - `approx : whole-days + (leaps / cycle)` (`𒈬𒁶 : 𒌓 𒋛 𒁄 𒉌 𒍣`): Computes the average year length of the candidate calendar.
   - `error : approx solar-year subtract absolute` (`𒇲 : 𒈬𒁶 𒈬 𒋫 𒋼`): Calculates the absolute discrepancy using `absolute` (`𒋼`, *te*).

5. **Determination and Retention**:
   - `candidate : cycle, leaps, error` (`𒊮 : 𒁄, 𒋛, 𒇲`): Assembles the values into an atomic determination record.
   - `retain candidate when ...` (`𒋼 𒊮 𒂊𒀀 ...`): Retains the candidate if its error is strictly smaller than the existing `best` error.

6. **Inscribing Results**:
   - The result outputs the 128-year cycle with 31 leap years.
   - The residual error is exact sexagesimal $0;0,0,2,42$ days/year (approximately 0.000012 days per year, or less than one day of drift every 80,000 years).

---

## Further Reading & Reference

- **[Language Guide: Calculations](../guide/calculations.md)**: Operators and postfix verbs.
- **[Language Guide: Domains & Selection](../guide/domains-and-selection.md)**: Bounded search loops and atomic retention.
- **[Language Guide: Determinations](../guide/determinations.md)**: Structured determination tuples and field lookups.
- **[Repository Example: Planetary Leap](../examples/index.md)**: Full planetary calendar implementation.


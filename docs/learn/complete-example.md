# 10. Complete Example: Leap-Cycle Search

This comprehensive example searches for the optimal calendar intercalation cycle for a tropical year of 365.2422 days across 200 years, retaining the cycle with minimal cumulative error.

---

## Scholar Mode

```dubsar
problem:
    solar_year : 365.2422
    limit : 200
    whole_days := solar_year floor
    fraction := solar_year - whole_days

    best : empty
    consider cycle from 1 through limit:
        leaps := cycle * fraction nearest
        approx := whole_days + (leaps / cycle)
        error := (approx - solar_year) absolute
        candidate : cycle, leaps, error
        retain candidate when error of candidate is lesser than error of best
result:
    best.cycle
    best.leaps
    best.error
```

---

## Tablet Mode (Cuneiform)

```dubsar
𒂊𒁹
    solar_year : 365.2422
    limit : 200
    whole_days := solar_year 𒄥
    fraction := solar_year whole_days 𒋫

    best : 𒉡
    𒄀 cycle 𒋫 1 𒌗 limit:
        leaps := cycle fraction 𒊭 𒊑
        approx := whole_days leaps cycle 𒉌 𒍣
        error := approx solar_year 𒋫 𒋼
        candidate : cycle, leaps, error
        𒋼 candidate 𒂊𒀀 candidate.error 𒌉 best.error
𒅗𒁹
    best.cycle
    best.leaps
    best.error
```

The algorithm converges on the 128-year leap cycle (31 leap years), producing an exact error of less than 0.0001 days per year.

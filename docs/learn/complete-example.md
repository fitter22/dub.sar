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
    𒈬 : 365.2422
    𒍠 : 200
    𒌓 := 𒈬 𒄥
    𒁇 := 𒈬 𒌓 𒋫

    𒊕 : 𒉡
    𒄀 𒁄 𒋫 1 𒂗 𒍠:
        𒋛 := 𒁄 𒁇 𒊭 𒊑
        𒈬𒁶 := 𒌓 𒋛 𒁄 𒉌 𒍣
        𒇲 := 𒈬𒁶 𒈬 𒋫 𒋼
        𒊮 : 𒁄, 𒋛, 𒇲
        𒋼 𒊮 𒂊𒀀 𒇲 𒊭 𒊮 𒌉 𒇲 𒊭 𒊕
𒅗𒁹
    𒊕
```

The algorithm converges on the 128-year leap cycle (31 leap years), producing an exact error of less than 0.0001 days per year.

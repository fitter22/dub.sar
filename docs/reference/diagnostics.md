# Diagnostics & Errors Reference

DUB.SAR features authentic, dual-script error diagnostics with visual source coordinate highlighting and historical explanations.

---

## Error Classification

| Error Type | Description |
| :--- | :--- |
| `DubSarSyntaxError` | Ill-formed tablet structure or invalid tokens. |
| `DubSarNameError` | Reference to undefined variable or procedure. |
| `DubSarUnitError` | Dimensionally inconsistent unit arithmetic or conversions. |
| `DubSarDivisionByZero` | Division or modulo by zero. |
| `DubSarRangeError` | Invalid loop domain bounds (e.g. non-positive, reversed). |
| `DubSarArchiveError` | Persistent tablet consultation, inscription, or corrupt archive errors. |
| `DubSarReturnError` | Procedure arity mismatch or missing return path. |

---

## Diagnostic Output Format

When an error occurs, DUB.SAR renders a boxed diagnostic showing both the cuneiform sign and scholar transliteration:

```text
══════════════════════════════════════════════════════════════════════
  DUB.SAR DIAGNOSTIC: DubSarUnitError
  Location: tablet.dub:2:16
══════════════════════════════════════════════════════════════════════

  [Tablet/Cuneiform]       x := 1 𒌓 + 2 𒈬
  [Scholar/Latin]          x := 1 day + 2 year
                                      ^

  Explanation:
    Cannot perform '+' between incompatible units: 'day' and 'year'
══════════════════════════════════════════════════════════════════════
```

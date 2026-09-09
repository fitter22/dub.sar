"""DUB.SAR 1.0 — Tablet-Aware Diagnostic Error Reporting.

Implements CR-027 and CR-028:
- Displays source line in both canonical cuneiform and scholar transliteration
- Underlines error coordinate with visual caret pointer
- Clearly states error type, contextual explanation, and file/line/col
"""

from __future__ import annotations

from typing import Optional

from dubsar.errors import DubSarError
from dubsar.normalizer import cuneiformize, transliterate


def format_diagnostic(
    error: DubSarError,
    source_text: Optional[str] = None,
    source_file: Optional[str] = None,
) -> str:
    """Formats a DubSarError into a tablet-aware diagnostic message."""
    file_name = error.source_file or source_file or "<tablet>"
    line_no = error.line
    col_no = error.col

    lines = []
    lines.append("═" * 70)
    lines.append(f"  DUB.SAR DIAGNOSTIC: {error.__class__.__name__}")
    lines.append(f"  Location: {file_name}:{line_no or '?'}:{col_no or '?'}")
    lines.append("═" * 70)

    if source_text and line_no is not None and line_no > 0:
        src_lines = source_text.splitlines()
        if 1 <= line_no <= len(src_lines):
            raw_line = src_lines[line_no - 1]
            cuneiform_line = cuneiformize(raw_line)
            scholar_line = transliterate(raw_line)

            lines.append("")
            lines.append(f"  [Tablet/Cuneiform]   {cuneiform_line}")
            lines.append(f"  [Scholar/Latin]      {scholar_line}")

            # Caret pointer
            if col_no is not None and col_no > 0:
                indent = " " * (23 + max(0, col_no - 1))
                lines.append(f"{indent}^")

    lines.append("")
    lines.append("  Explanation:")
    for msg_line in error.message.splitlines():
        lines.append(f"    {msg_line}")
    lines.append("═" * 70)

    return "\n".join(lines)

"""DUB.SAR 1.0 — Runtime Values and Sentinels.

Defines the runtime value representations for mathematical determinations
and sentinels used across the reference interpreter and virtual machine.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from dubsar.errors import DubSarNameError
from dubsar.numbers import Rational
from dubsar.units import Quantity


class EmptySentinel:
    """Sentinel representing an empty determination or lookup thereon."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "empty"

    def __str__(self) -> str:
        return "empty"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EmptySentinel)


class DeterminationValue:
    """A mathematical determination grouping related named quantities."""

    __slots__ = ("fields",)

    def __init__(self, fields: Optional[Dict[str, Any]] = None) -> None:
        self.fields: Dict[str, Any] = dict(fields) if fields else {}

    @property
    def is_empty(self) -> bool:
        return len(self.fields) == 0

    def get(self, field_name: str) -> Any:
        if self.is_empty:
            return EmptySentinel()
        if field_name not in self.fields:
            raise DubSarNameError(f"Field '{field_name}' not found in determination")
        return self.fields[field_name]

    def set(self, field_name: str, value: Any) -> None:
        self.fields[field_name] = value

    def clone(self) -> DeterminationValue:
        return DeterminationValue(dict(self.fields))

    def __repr__(self) -> str:
        if self.is_empty:
            return "empty"
        items = ", ".join(f"{k}: {v}" for k, v in self.fields.items())
        return f"determination({items})"

    def __str__(self) -> str:
        if self.is_empty:
            return "empty"
        items = []
        for k, v in self.fields.items():
            if isinstance(v, Quantity):
                v_str = v.format()
            else:
                v_str = str(v)
            items.append(f"{k} = {v_str}")
        return ", ".join(items)

    def format_lines(self, format_mode: str = "canonical") -> List[str]:
        if self.is_empty:
            return ["empty"]
        lines = []
        for k, v in self.fields.items():
            if isinstance(v, Quantity):
                v_str = v.format(format_mode=format_mode)
            elif isinstance(v, Rational):
                v_str = v.format_canonical()
            else:
                v_str = str(v)
            lines.append(v_str)
        return lines

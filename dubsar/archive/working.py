"""DUB.SAR 1.0 — Working Tablet (Temporary Mutable Tablet Representation).

Implements Section 15, 17, 18, 54, 55 of the Tablet Archive Change Request:
- In-memory mutable ordered mapping/sequence
- High-performance calculation and mutation without DB writes
- Copy and derivation provenance tracking
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

from dubsar.archive.models import (
    HistoricalTag,
    TabletKind,
    TabletMetadata,
    TabletShape,
    deserialize_value,
    serialize_value,
)
from dubsar.errors import DubSarInvalidEntryError
from dubsar.numbers import Rational
from dubsar.units import Quantity


class WorkingTablet:
    """A temporary, mutable tablet living in memory (§15, §54)."""

    def __init__(
        self,
        name: str,
        shape: TabletShape = TabletShape.TABLE,
        kind: TabletKind = TabletKind.DATA,
        metadata: Optional[TabletMetadata] = None,
        provenance: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.name = name
        self.shape = shape
        self.kind = kind
        self.metadata = metadata or TabletMetadata(
            title=name,
            kind=kind,
            historical_tag=HistoricalTag.MODERN,
            created_by="working-tablet",
        )
        self.provenance = provenance or {}
        self.entries: OrderedDict[Any, Any] = OrderedDict()

    def _normalize_key(self, key: Any) -> Any:
        if isinstance(key, int):
            return Rational(key)
        if isinstance(key, Quantity) and key.unit.is_dimensionless:
            return key.value
        return key

    def put(self, key: Any, value: Any) -> None:
        """Adds or sets an entry in the working tablet (§15)."""
        norm_key = self._normalize_key(key)
        self.entries[norm_key] = value

    def replace(self, key: Any, value: Any) -> None:
        """Replaces an existing entry, erroring if key does not exist (§15)."""
        norm_key = self._normalize_key(key)
        if norm_key not in self.entries:
            raise DubSarInvalidEntryError(f"Cannot replace missing entry with key {key!r} in working tablet {self.name!r}")
        self.entries[norm_key] = value

    def remove(self, key: Any) -> Any:
        """Removes an entry from the working tablet (§15)."""
        norm_key = self._normalize_key(key)
        if norm_key not in self.entries:
            raise DubSarInvalidEntryError(f"Cannot remove missing entry with key {key!r} in working tablet {self.name!r}")
        return self.entries.pop(norm_key)

    def get(self, key: Any, default: Any = None) -> Any:
        """Looks up an entry value by key."""
        norm_key = self._normalize_key(key)
        return self.entries.get(norm_key, default)

    def seek_nearest(self, target: Any) -> Optional[Tuple[Any, Any]]:
        """Finds the entry whose numeric key is nearest to target (§22)."""
        target_val = target
        if isinstance(target, int):
            target_val = Rational(target)
        elif isinstance(target, Quantity):
            target_val = target.value

        best_entry: Optional[Tuple[Any, Any]] = None
        min_diff: Optional[Rational] = None

        for k, v in self.entries.items():
            k_val = None
            if isinstance(k, (int, Rational)):
                k_val = Rational(k) if isinstance(k, int) else k
            elif isinstance(k, Quantity):
                k_val = k.value

            if k_val is not None and isinstance(target_val, Rational):
                diff = abs(k_val - target_val)
                if min_diff is None or diff < min_diff:
                    min_diff = diff
                    best_entry = (k, v)

        return best_entry

    def __getitem__(self, key: Any) -> Any:
        norm_key = self._normalize_key(key)
        if norm_key not in self.entries:
            raise DubSarInvalidEntryError(f"Entry {key!r} not found in working tablet {self.name!r}")
        return self.entries[norm_key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self.put(key, value)

    def __delitem__(self, key: Any) -> None:
        self.remove(key)

    def __len__(self) -> int:
        return len(self.entries)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.entries)

    def items(self) -> List[Tuple[Any, Any]]:
        return list(self.entries.items())

    def keys(self) -> List[Any]:
        return list(self.entries.keys())

    def values(self) -> List[Any]:
        return list(self.entries.values())

    def to_payload(self) -> Dict[str, Any]:
        """Converts working tablet contents into serializable payload."""
        serialized_entries = [
            {
                "key": serialize_value(k),
                "val": serialize_value(v),
            }
            for k, v in self.entries.items()
        ]
        return {
            "shape": self.shape.value if isinstance(self.shape, TabletShape) else str(self.shape),
            "entries": serialized_entries,
        }

    @classmethod
    def from_payload(
        cls,
        name: str,
        payload: Dict[str, Any],
        kind: TabletKind = TabletKind.DATA,
        metadata: Optional[TabletMetadata] = None,
        provenance: Optional[Dict[str, Any]] = None,
    ) -> WorkingTablet:
        shape_str = payload.get("shape", TabletShape.TABLE.value)
        try:
            shape = TabletShape(shape_str)
        except ValueError:
            shape = TabletShape.TABLE

        wt = cls(name=name, shape=shape, kind=kind, metadata=metadata, provenance=provenance)
        for e in payload.get("entries", []):
            k = deserialize_value(e.get("key"))
            v = deserialize_value(e.get("val"))
            wt.put(k, v)
        return wt

    def __repr__(self) -> str:
        return f"WorkingTablet({self.name!r}, entries={len(self.entries)})"

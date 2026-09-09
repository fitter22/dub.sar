"""DUB.SAR 1.0 — Tablet Archive Models and Canonical Serialization.

Implements Sections 8-14, 25-26, 45-46, 65-66 of the Tablet Archive Change Request:
- Immutable persistent tablet versions and metadata
- Exact arbitrary-precision rational and quantity serialization
- Canonical content hashing and provenance tracking
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from dubsar.numbers import Rational
from dubsar.units import Quantity, Unit, lookup_unit
from dubsar.values import DeterminationValue, EmptySentinel


class TabletKind(str, Enum):
    """Semantic category of a tablet."""
    MATHEMATICAL = "mathematical"
    TABLE = "table"
    LEXICAL = "lexical"
    METROLOGICAL = "metrological"
    ASTRONOMICAL = "astronomical"
    PROCEDURAL = "procedural"
    DATA = "data"
    TEXT = "text"


class TabletShape(str, Enum):
    """Structural layout of a tablet."""
    SCALAR = "scalar"
    TABLE = "table"
    SEQUENCE = "sequence"
    STRUCTURED = "structured"
    TEXT = "text"


class HistoricalTag(str, Enum):
    """Historical provenance classification (§46)."""
    ATTESTED = "attested"
    RECONSTRUCTED = "reconstructed"
    MODERN = "modern"


@dataclass
class TabletMetadata:
    """Provenance and scholarly metadata for a persistent tablet (§45)."""
    title: str = ""
    kind: TabletKind = TabletKind.MATHEMATICAL
    version: int = 1
    language: str = "sumerian/latin"
    period: Optional[str] = "Old Babylonian"
    provenance: Optional[str] = None
    author: Optional[str] = None
    source: Optional[str] = None
    confidence: Optional[str] = "high"
    historical_tag: HistoricalTag = HistoricalTag.MODERN
    copied_from: Optional[str] = None
    derived_from: Optional[str] = None
    source_version: Optional[int] = None
    created_by: str = "dubsar"
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["kind"] = self.kind.value if isinstance(self.kind, TabletKind) else str(self.kind)
        d["historical_tag"] = self.historical_tag.value if isinstance(self.historical_tag, HistoricalTag) else str(self.historical_tag)
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TabletMetadata:
        d = dict(data)
        if "kind" in d and isinstance(d["kind"], str):
            try:
                d["kind"] = TabletKind(d["kind"])
            except ValueError:
                d["kind"] = TabletKind.DATA
        if "historical_tag" in d and isinstance(d["historical_tag"], str):
            try:
                d["historical_tag"] = HistoricalTag(d["historical_tag"])
            except ValueError:
                d["historical_tag"] = HistoricalTag.MODERN
        known = {f for f in cls.__dataclass_fields__}
        filtered = {k: v for k, v in d.items() if k in known}
        return cls(**filtered)


@dataclass
class TabletReference:
    """A lightweight handle identifying a persistent tablet (§20)."""
    tablet_id: str
    name: str
    namespace: str = "standard"
    version: int = 1
    kind: TabletKind = TabletKind.MATHEMATICAL
    shape: TabletShape = TabletShape.TABLE

    def __repr__(self) -> str:
        return f"TabletRef({self.name!r} v{self.version})"


@dataclass
class TabletVersionInfo:
    """Complete immutable record of a persisted tablet version (§9, §10)."""
    tablet_id: str
    name: str
    namespace: str
    version: int
    checksum: str
    kind: TabletKind
    shape: TabletShape
    metadata: TabletMetadata
    parent_tablet_id: Optional[str]
    parent_version: Optional[int]
    derived_from_name: Optional[str]
    derived_from_version: Optional[int]
    created_at: str
    created_by: str
    payload: Dict[str, Any]
    entries: List[Tuple[Any, Any]] = field(default_factory=list)

    def get_entry(self, key: Any) -> Optional[Any]:
        """Looks up an entry by key with exact semantic matching."""
        search_key = key
        if isinstance(key, int):
            search_key = Rational(key)
        elif hasattr(key, "unit") and hasattr(key, "value") and getattr(key.unit, "is_dimensionless", False):
            search_key = key.value

        for k, v in self.entries:
            comp_k = Rational(k) if isinstance(k, int) else k
            if hasattr(comp_k, "unit") and hasattr(comp_k, "value") and getattr(comp_k.unit, "is_dimensionless", False):
                comp_k = comp_k.value
            if comp_k == search_key:
                return v
        return None

    def get(self, key: Any, default: Any = None) -> Any:
        res = self.get_entry(key)
        return res if res is not None else default

    def seek_nearest(self, target: Any) -> Optional[Tuple[Any, Any]]:
        """Finds the entry whose numeric key is nearest to target."""
        target_val = target
        if isinstance(target, int):
            target_val = Rational(target)
        elif isinstance(target, Quantity):
            target_val = target.value

        best_entry: Optional[Tuple[Any, Any]] = None
        min_diff: Optional[Rational] = None

        for k, v in self.entries:
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

    def __repr__(self) -> str:
        return f"Tablet({self.name!r} v{self.version}, shape={self.shape.value}, entries={len(self.entries)})"


# ==============================================================================
# Canonical Serialization (§13, §14, §65, §66)
# ==============================================================================

def serialize_value(val: Any) -> Any:
    """Serializes a DUB.SAR runtime value into canonical exact JSON representation."""
    if isinstance(val, Rational):
        return {"_type": "rational", "num": val.numerator, "den": val.denominator}
    if isinstance(val, Quantity):
        return {
            "_type": "quantity",
            "val": serialize_value(val.value),
            "unit": str(val.unit),
        }
    if isinstance(val, DeterminationValue):
        return {
            "_type": "determination",
            "name": val.name,
            "fields": {k: serialize_value(v) for k, v in val.fields.items()},
        }
    if isinstance(val, EmptySentinel):
        return {"_type": "empty"}
    if isinstance(val, TabletReference):
        return {
            "_type": "tablet_ref",
            "tablet_id": val.tablet_id,
            "name": val.name,
            "version": val.version,
        }
    if isinstance(val, (int, str, bool)):
        return val
    if isinstance(val, list):
        return [serialize_value(item) for item in val]
    if isinstance(val, dict):
        return {str(k): serialize_value(v) for k, v in val.items()}
    return str(val)


def deserialize_value(data: Any) -> Any:
    """Reconstitutes a DUB.SAR runtime value from its canonical exact representation."""
    if isinstance(data, dict):
        t = data.get("_type")
        if t == "rational":
            return Rational(data["num"], data["den"])
        if t == "quantity":
            val = deserialize_value(data["val"])
            u = lookup_unit(data["unit"])
            return Quantity(val if isinstance(val, Rational) else Rational(val), u)
        if t == "determination":
            fields = {k: deserialize_value(v) for k, v in data.get("fields", {}).items()}
            return DeterminationValue(name=data.get("name", "determination"), fields=fields)
        if t == "empty":
            return EmptySentinel()
        if t == "tablet_ref":
            return TabletReference(
                tablet_id=data.get("tablet_id", ""),
                name=data.get("name", ""),
                version=data.get("version", 1),
            )
        return {k: deserialize_value(v) for k, v in data.items()}
    if isinstance(data, list):
        return [deserialize_value(x) for x in data]
    return data


def compute_payload_checksum(payload: Dict[str, Any]) -> str:
    """Computes a deterministic SHA-256 content checksum for a tablet payload (§66)."""
    canonical_json = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

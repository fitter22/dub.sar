"""DUB.SAR 1.0 — Tablet Archive Subsystem.

Implements the Tablet Archive (House of Tablets / É.DUB.BA.A):
- Persistent, versioned, immutable scholarly and user-generated mathematical tablets
- In-memory mutable working tablets
- Standard mathematical knowledge collections
"""

from dubsar.archive.archive import SQLiteTabletArchive, TabletArchive
from dubsar.archive.models import (
    HistoricalTag,
    TabletKind,
    TabletMetadata,
    TabletReference,
    TabletShape,
    TabletVersionInfo,
    deserialize_value,
    serialize_value,
)
from dubsar.archive.seed import STANDARD_ARCHIVE_VERSION, build_standard_tablets
from dubsar.archive.working import WorkingTablet

__all__ = [
    "TabletArchive",
    "SQLiteTabletArchive",
    "WorkingTablet",
    "TabletMetadata",
    "TabletVersionInfo",
    "TabletReference",
    "TabletKind",
    "TabletShape",
    "HistoricalTag",
    "STANDARD_ARCHIVE_VERSION",
    "build_standard_tablets",
    "serialize_value",
    "deserialize_value",
]

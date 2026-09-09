"""DUB.SAR 1.0 — Tablet Archive SQLite Storage Backend.

Implements Sections 4-10, 36-43, 63-66 of the Tablet Archive Change Request:
- SQLite embedded single-file archive with atomic transactions
- Monotonically increasing immutable tablet versions
- Provenance lineage, checksums, and export/import
"""

from __future__ import annotations

import datetime
import json
import os
import sqlite3
import threading
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from dubsar.archive.models import (
    HistoricalTag,
    TabletKind,
    TabletMetadata,
    TabletReference,
    TabletShape,
    TabletVersionInfo,
    compute_payload_checksum,
    deserialize_value,
    serialize_value,
)
from dubsar.archive.seed import STANDARD_ARCHIVE_VERSION, build_standard_tablets
from dubsar.archive.working import WorkingTablet
from dubsar.errors import (
    DubSarArchiveConflictError,
    DubSarArchiveCorruptError,
    DubSarArchiveError,
    DubSarConsultationError,
    DubSarInscriptionError,
    DubSarTabletExistsError,
    DubSarTabletNotFoundError,
    DubSarTabletVersionNotFoundError,
)


class TabletArchive(ABC):
    """Abstract interface for DUB.SAR Tablet Archive (§1, §4, §53)."""

    @abstractmethod
    def consult(self, name: str, version: Optional[int] = None, namespace: Optional[str] = None) -> TabletVersionInfo:
        """Consults a persistent tablet, returning an immutable read-only version record (§19)."""
        pass

    @abstractmethod
    def create_working(self, name: str, shape: TabletShape = TabletShape.TABLE, kind: TabletKind = TabletKind.DATA) -> WorkingTablet:
        """Creates a temporary, mutable working tablet in memory (§15)."""
        pass

    @abstractmethod
    def copy(self, source_name: str, target_name: str, version: Optional[int] = None) -> WorkingTablet:
        """Copies a persistent tablet into a new mutable working tablet (§17)."""
        pass

    @abstractmethod
    def derive(self, source_name: str, target_name: str, version: Optional[int] = None) -> WorkingTablet:
        """Derives a new mutable working tablet retaining explicit source provenance (§18)."""
        pass

    @abstractmethod
    def inscribe(self, working: WorkingTablet, target_name: str, metadata: Optional[TabletMetadata] = None) -> TabletVersionInfo:
        """Atomically inscribes a working tablet as a new persistent tablet version (§16, §42)."""
        pass

    @abstractmethod
    def history(self, name: str) -> List[TabletVersionInfo]:
        """Returns the linear version history of a persistent tablet (§38)."""
        pass

    @abstractmethod
    def list_tablets(self, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists available tablets in the archive."""
        pass

    @abstractmethod
    def export_archive(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        """Exports the entire archive state to a canonical reproducible JSON dictionary (§64)."""
        pass

    @abstractmethod
    def import_archive(self, data_or_path: Union[Dict[str, Any], str]) -> int:
        """Imports tablets and versions from exported JSON data (§64)."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Closes archive connections."""
        pass


class SQLiteTabletArchive(TabletArchive):
    """Embedded SQLite implementation of the DUB.SAR Tablet Archive (§4, §53)."""

    def __init__(self, db_path: str = ":memory:", auto_seed: bool = True) -> None:
        self.db_path = db_path
        self._lock = threading.RLock()
        
        # Ensure directory exists for file-backed DBs
        if db_path != ":memory:":
            p = Path(db_path).resolve()
            p.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(str(p), check_same_thread=False)
        else:
            self._conn = sqlite3.connect(":memory:", check_same_thread=False)

        self._conn.row_factory = sqlite3.Row
        self._init_schema()

        if auto_seed:
            self._seed_standard_archive()

    def _init_schema(self) -> None:
        with self._lock, self._conn:
            cur = self._conn.cursor()
            # Metadata table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS archive_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)

            # Tablets master catalog
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tablets (
                    tablet_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    namespace TEXT NOT NULL DEFAULT 'standard',
                    kind TEXT NOT NULL,
                    shape TEXT NOT NULL,
                    current_version INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    UNIQUE(namespace, name)
                )
            """)

            # Immutable versions table (§8, §9)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tablet_versions (
                    version_id TEXT PRIMARY KEY,
                    tablet_id TEXT NOT NULL REFERENCES tablets(tablet_id),
                    version INTEGER NOT NULL,
                    checksum TEXT NOT NULL,
                    parent_tablet_id TEXT,
                    parent_version INTEGER,
                    derived_from_name TEXT,
                    derived_from_version INTEGER,
                    created_at TEXT NOT NULL,
                    created_by TEXT NOT NULL DEFAULT 'dubsar',
                    metadata_json TEXT NOT NULL DEFAULT '{}',
                    payload_json TEXT NOT NULL,
                    UNIQUE(tablet_id, version)
                )
            """)

            # Record schema version
            cur.execute("""
                INSERT OR IGNORE INTO archive_metadata (key, value)
                VALUES ('schema_version', '1')
            """)

    def _seed_standard_archive(self) -> None:
        """Seeds standard mathematical knowledge tablets if not already present (§27, §68)."""
        with self._lock, self._conn:
            cur = self._conn.cursor()
            cur.execute("SELECT value FROM archive_metadata WHERE key = 'standard_archive_version'")
            row = cur.fetchone()
            if row is not None and row["value"] == STANDARD_ARCHIVE_VERSION:
                return  # Already seeded

        # Seed tablets
        standard_tablets = build_standard_tablets()
        for wt in standard_tablets:
            # Check if tablet already exists
            existing = self._find_tablet_row(wt.name)
            if existing is None:
                self.inscribe(wt, target_name=wt.name, metadata=wt.metadata, namespace="standard")

        with self._lock, self._conn:
            self._conn.execute("""
                INSERT OR REPLACE INTO archive_metadata (key, value)
                VALUES ('standard_archive_version', ?)
            """, (STANDARD_ARCHIVE_VERSION,))

    def _find_tablet_row(self, name: str, namespace: Optional[str] = None) -> Optional[sqlite3.Row]:
        cur = self._conn.cursor()
        if namespace is not None:
            cur.execute("SELECT * FROM tablets WHERE name = ? AND namespace = ?", (name, namespace))
            return cur.fetchone()
        
        # Priority order: program/user namespace first, then standard
        cur.execute("SELECT * FROM tablets WHERE name = ? ORDER BY CASE WHEN namespace = 'standard' THEN 1 ELSE 0 END", (name,))
        return cur.fetchone()

    def consult(self, name: str, version: Optional[int] = None, namespace: Optional[str] = None) -> TabletVersionInfo:
        with self._lock:
            t_row = self._find_tablet_row(name, namespace)
            if t_row is None:
                raise DubSarTabletNotFoundError(f"Tablet {name!r} not found in tablet archive")

            target_version = version if version is not None else t_row["current_version"]
            cur = self._conn.cursor()
            cur.execute(
                "SELECT * FROM tablet_versions WHERE tablet_id = ? AND version = ?",
                (t_row["tablet_id"], target_version),
            )
            v_row = cur.fetchone()
            if v_row is None:
                raise DubSarTabletVersionNotFoundError(
                    f"Version {target_version} of tablet {name!r} not found in archive"
                )

            return self._row_to_version_info(t_row, v_row)

    def _row_to_version_info(self, t_row: sqlite3.Row, v_row: sqlite3.Row) -> TabletVersionInfo:
        try:
            meta_dict = json.loads(v_row["metadata_json"])
            payload = json.loads(v_row["payload_json"])
        except Exception as e:
            raise DubSarArchiveCorruptError(f"Corrupt JSON data in tablet {t_row[name]}: {e}")

        metadata = TabletMetadata.from_dict(meta_dict)
        entries: List[Tuple[Any, Any]] = []
        for e in payload.get("entries", []):
            k = deserialize_value(e.get("key"))
            v = deserialize_value(e.get("val"))
            entries.append((k, v))

        return TabletVersionInfo(
            tablet_id=t_row["tablet_id"],
            name=t_row["name"],
            namespace=t_row["namespace"],
            version=v_row["version"],
            checksum=v_row["checksum"],
            kind=TabletKind(t_row["kind"]),
            shape=TabletShape(t_row["shape"]),
            metadata=metadata,
            parent_tablet_id=v_row["parent_tablet_id"],
            parent_version=v_row["parent_version"],
            derived_from_name=v_row["derived_from_name"],
            derived_from_version=v_row["derived_from_version"],
            created_at=v_row["created_at"],
            created_by=v_row["created_by"],
            payload=payload,
            entries=entries,
        )

    def create_working(self, name: str, shape: TabletShape = TabletShape.TABLE, kind: TabletKind = TabletKind.DATA) -> WorkingTablet:
        return WorkingTablet(name=name, shape=shape, kind=kind)

    def copy(self, source_name: str, target_name: str, version: Optional[int] = None) -> WorkingTablet:
        info = self.consult(source_name, version=version)
        wt = WorkingTablet.from_payload(
            name=target_name,
            payload=info.payload,
            kind=info.kind,
            metadata=TabletMetadata(
                title=f"Copy of {info.name}",
                kind=info.kind,
                copied_from=info.name,
                source_version=info.version,
                created_by="copy-tablet",
            ),
            provenance={
                "copied_from": info.name,
                "source_version": info.version,
                "source_checksum": info.checksum,
            },
        )
        return wt

    def derive(self, source_name: str, target_name: str, version: Optional[int] = None) -> WorkingTablet:
        info = self.consult(source_name, version=version)
        wt = WorkingTablet.from_payload(
            name=target_name,
            payload=info.payload,
            kind=info.kind,
            metadata=TabletMetadata(
                title=f"Derived from {info.name}",
                kind=info.kind,
                derived_from=info.name,
                source_version=info.version,
                created_by="derive-tablet",
            ),
            provenance={
                "derived_from": info.name,
                "source_version": info.version,
                "source_checksum": info.checksum,
            },
        )
        return wt

    def inscribe(
        self,
        working: WorkingTablet,
        target_name: str,
        metadata: Optional[TabletMetadata] = None,
        namespace: str = "program",
    ) -> TabletVersionInfo:
        with self._lock:
            try:
                # Prepare payload and checksum (§66)
                payload = working.to_payload()
                checksum = compute_payload_checksum(payload)
                now_str = datetime.datetime.utcnow().isoformat() + "Z"

                meta = metadata or working.metadata
                meta.title = meta.title or target_name
                meta_dict = meta.to_dict()

                parent_tablet_id = None
                parent_version = None
                derived_from_name = working.provenance.get("derived_from") or meta.derived_from
                derived_from_version = working.provenance.get("source_version") or meta.source_version

                with self._conn:
                    cur = self._conn.cursor()
                    cur.execute(
                        "SELECT * FROM tablets WHERE name = ? AND namespace = ?",
                        (target_name, namespace),
                    )
                    t_row = cur.fetchone()

                    if t_row is None:
                        # Create new persistent tablet record
                        t_id = str(uuid.uuid4())
                        new_version = 1
                        shape_str = working.shape.value if isinstance(working.shape, TabletShape) else str(working.shape)
                        kind_str = working.kind.value if isinstance(working.kind, TabletKind) else str(working.kind)

                        cur.execute("""
                            INSERT INTO tablets (tablet_id, name, namespace, kind, shape, current_version, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (t_id, target_name, namespace, kind_str, shape_str, new_version, now_str))
                    else:
                        # Existing tablet: monotonically bump version (§8, §9)
                        t_id = t_row["tablet_id"]
                        parent_tablet_id = t_id
                        parent_version = t_row["current_version"]
                        new_version = parent_version + 1

                        cur.execute("""
                            UPDATE tablets SET current_version = ? WHERE tablet_id = ?
                        """, (new_version, t_id))

                    # Insert immutable version (§8)
                    v_id = str(uuid.uuid4())
                    meta_dict["version"] = new_version
                    payload_json = json.dumps(payload, sort_keys=True)
                    meta_json = json.dumps(meta_dict, sort_keys=True)

                    cur.execute("""
                        INSERT INTO tablet_versions (
                            version_id, tablet_id, version, checksum,
                            parent_tablet_id, parent_version,
                            derived_from_name, derived_from_version,
                            created_at, created_by, metadata_json, payload_json
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        v_id, t_id, new_version, checksum,
                        parent_tablet_id, parent_version,
                        derived_from_name, derived_from_version,
                        now_str, meta.created_by, meta_json, payload_json
                    ))

                # Reload newly inscribed version
                return self.consult(target_name, version=new_version, namespace=namespace)
            except Exception as e:
                if isinstance(e, DubSarArchiveError):
                    raise
                raise DubSarInscriptionError(f"Inscription of tablet {target_name!r} failed: {e}")

    def history(self, name: str) -> List[TabletVersionInfo]:
        with self._lock:
            t_row = self._find_tablet_row(name)
            if t_row is None:
                raise DubSarTabletNotFoundError(f"Tablet {name!r} not found in archive")

            cur = self._conn.cursor()
            cur.execute(
                "SELECT * FROM tablet_versions WHERE tablet_id = ? ORDER BY version ASC",
                (t_row["tablet_id"],),
            )
            rows = cur.fetchall()
            return [self._row_to_version_info(t_row, r) for r in rows]

    def list_tablets(self, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._lock:
            cur = self._conn.cursor()
            if namespace is not None:
                cur.execute("SELECT * FROM tablets WHERE namespace = ? ORDER BY name", (namespace,))
            else:
                cur.execute("SELECT * FROM tablets ORDER BY namespace, name")
            rows = cur.fetchall()
            result = []
            for r in rows:
                result.append({
                    "tablet_id": r["tablet_id"],
                    "name": r["name"],
                    "namespace": r["namespace"],
                    "kind": r["kind"],
                    "shape": r["shape"],
                    "current_version": r["current_version"],
                    "created_at": r["created_at"],
                })
            return result

    def export_archive(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        with self._lock:
            tablets = self.list_tablets()
            export_data: Dict[str, Any] = {
                "format": "DUB.SAR Tablet Archive Export",
                "export_version": 1,
                "exported_at": datetime.datetime.utcnow().isoformat() + "Z",
                "tablets": [],
            }

            for t in tablets:
                history_versions = self.history(t["name"])
                t_record = {
                    "name": t["name"],
                    "namespace": t["namespace"],
                    "kind": t["kind"],
                    "shape": t["shape"],
                    "current_version": t["current_version"],
                    "versions": [
                        {
                            "version": v.version,
                            "checksum": v.checksum,
                            "created_at": v.created_at,
                            "created_by": v.created_by,
                            "metadata": v.metadata.to_dict(),
                            "derived_from_name": v.derived_from_name,
                            "derived_from_version": v.derived_from_version,
                            "payload": v.payload,
                        }
                        for v in history_versions
                    ],
                }
                export_data["tablets"].append(t_record)

            if filepath:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(export_data, f, indent=2, sort_keys=True)

            return export_data

    def import_archive(self, data_or_path: Union[Dict[str, Any], str]) -> int:
        if isinstance(data_or_path, str):
            with open(data_or_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = data_or_path

        imported_count = 0
        tablets = data.get("tablets", [])
        for t in tablets:
            t_name = t["name"]
            t_ns = t.get("namespace", "user")
            t_kind = TabletKind(t.get("kind", TabletKind.DATA.value))
            t_shape = TabletShape(t.get("shape", TabletShape.TABLE.value))

            for v in t.get("versions", []):
                meta = TabletMetadata.from_dict(v.get("metadata", {}))
                payload = v.get("payload", {})
                wt = WorkingTablet.from_payload(
                    name=t_name,
                    payload=payload,
                    kind=t_kind,
                    metadata=meta,
                )
                self.inscribe(wt, target_name=t_name, metadata=meta, namespace=t_ns)
                imported_count += 1

        return imported_count

    def close(self) -> None:
        with self._lock:
            try:
                self._conn.close()
            except Exception:
                pass

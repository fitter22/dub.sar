# Tablet Archive

The DUB.SAR Tablet Archive (`e2-dub-ba-a` / *tablet house*) provides persistent, versioned, cryptographic storage for tablets.

---

## Architecture

- **Storage Engine**: SQLite embedded storage (`.tablets.db`).
- **Cryptographic Provenance**: Every inscribed tablet version computes a canonical SHA-256 hash of its serialized payload and metadata.
- **Immutability**: Inscribed tablets cannot be modified in place. Re-inscribing with changes automatically creates a new immutable version.

---

## Archive Commands

- `consult "name"`: Opens a persistent tablet for reading.
- `inscribe working as "name"`: Inscribes a working tablet into the archive as a new version.
- `copy "source" as working target`: Copies an archived tablet into a new mutable working tablet.
- `history of "name"`: Retrieves the version history and provenance of an archived tablet.

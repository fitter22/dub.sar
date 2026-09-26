# Archive and Provenance

In ancient Mesopotamia, finished clay tablets were deposited in the tablet house (*é-dub-ba-a*) or temple archive, cataloged, and organized in wicker baskets with clay labels (*pisan-dub-ba*).

---

## The Tablet Archive

DUB.SAR mirrors this archival tradition through an integrated SQLite-backed tablet store:

1. **Content Addressing**: Tablets are cryptographically hashed using SHA-256 upon inscription. Changes to problem inputs, recipe operations, or inscribed results produce distinct content fingerprints.
2. **Immutable Versioning**: Tablets inscribed into the archive cannot be overwritten. Successive revisions create parent-child lineage edges, forming an immutable directed acyclic graph (DAG) of tablet provenance.
3. **Execution Metadata**: Stored tablets retain full provenance metadata: timestamp, author, source mode (Scholar, Tablet, or Mixed), backend execution target, and execution duration.
4. **Lineage Queries**: Scribes can inspect tablet ancestry, verify that calculations reproduce across different execution backends, and trace mathematical derivations back to their foundational assumptions.
5. **Standard Knowledge Heritage**: Every new archive initializes with "Scribal Archive 1"—13 attested mathematical reference tablets including reciprocals, squares, square roots, right-triangle triples, and metrology standards.

For complete syntactical examples, CLI commands, and an end-to-end case study of the Ea-nāṣir copper complaint audit, consult the [Tablet Archive Guide](../guide/archive.md).

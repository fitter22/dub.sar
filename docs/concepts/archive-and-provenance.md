# Archive and Provenance

In ancient Mesopotamia, finished clay tablets were deposited in the tablet house (*e2-dub-ba-a*) or temple archive, cataloged, and organized in wicker baskets with clay labels (*pisan-dub-ba*).

---

## The Tablet Archive

DUB.SAR mirrors this archival tradition through an integrated SQLite-backed tablet store:

1. **Content Addressing**: Tablets are cryptographically hashed using SHA-256 upon inscription. Changes to problem inputs, recipe operations, or inscribed results produce distinct content fingerprints.
2. **Immutable Versioning**: Tablets inscribed into the archive cannot be overwritten. Successive revisions create parent-child lineage edges, forming an immutable directed acyclic graph (DAG) of tablet provenance.
3. **Execution Metadata**: Stored tablets retain full provenance metadata: timestamp, author, source mode (Tablet or Scholar), backend execution target, and execution duration.
4. **Lineage Queries**: Scribes can inspect tablet ancestry, verify that calculations reproduce across different execution backends, and trace mathematical derivations back to their foundational assumptions.

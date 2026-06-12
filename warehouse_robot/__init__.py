"""Warehouse robot — deterministic storage layer for the SPQR knowledge warehouse.

B1 scope: markdown store + node/edge layout + instance manifest + SQLite DDL.
Later tickets build on this package: the fold (B2), the query interface (B3),
the write gate (B4), and the audit tripwires (B5).

Design anchors (see docs/NODE_FORMAT.md and the Warehouse Initiation Project
decision record):
- Markdown is the source of truth; the SQLite index is a derived, disposable
  projection (S7).
- The warehouse root is a mandatory runtime parameter — there is no default
  and no hardcoded path (A4).
- The robot writes files; it never runs git (G3).
"""

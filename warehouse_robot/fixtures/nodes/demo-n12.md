---
id: demo-n12
kind: constraint
status: active
title: WAL mode requires a writable directory
scope: data-layer
origin: inherited
timestamp: 2026-06-07T10:30:00Z
source: SQLite documentation
schema_version: 1
---

Platform-inherited constraint: SQLite WAL journaling creates sidecar
files next to the database, so the index directory must stay writable.
Deliberately edge-free fixture for parser and audit coverage.

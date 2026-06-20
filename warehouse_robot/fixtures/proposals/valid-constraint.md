---
kind: constraint
status: active
title: SQLite must ship FTS5
origin: inherited
source: platform
edges:
  - type: constrains
    target: demo-n1
---

The runtime SQLite build must provide FTS5 or the index cannot be created.

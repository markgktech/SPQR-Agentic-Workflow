---
id: demo-f2
kind: flag
status: active
title: Contradiction: demo-n2 conflicts with the demo-n6 lesson
flag_type: contradiction
origin: observed
timestamp: 2026-06-04T12:00:00Z
schema_version: 1
edges:
  - type: flags
    target: demo-n2
---

Semantic-audit fixture: the RED lesson demo-n6 contradicts the
typed-envelope decision demo-n2 in practice. demo-n7 carries a resolves
edge to this flag, so it is derived RESOLVED — the resolved half of the
v_flag_status test pair. The flag never mutates its target (S6).

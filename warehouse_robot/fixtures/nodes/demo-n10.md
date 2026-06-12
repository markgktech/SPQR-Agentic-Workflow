---
id: demo-n10
kind: lesson
status: active
title: Supersede chain verified end to end
verdict: GREEN
origin: observed
timestamp: 2026-06-06T16:00:00Z
ticket: DEMO-5
agent: Probator
schema_version: 1
edges:
  - type: about
    target: demo-n7
---

Verification run on the result-envelope migration: the superseded node
demo-n2 correctly disappears from active queries while staying readable
in history. Clean pass, recorded with evidence.

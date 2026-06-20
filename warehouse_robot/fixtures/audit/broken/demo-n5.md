---
id: demo-n5
kind: lesson
status: active
title: A lesson that forgot its about edge
origin: observed
timestamp: 2026-06-02T09:05:00Z
ticket: DEMO-4
agent: Probator
schema_version: 1
edges:
  - type: relates-to
    target: demo-n1
---

Deliberately broken fixture (A16): a lesson connected only by a weak relates-to
(so it is NOT an orphan) but missing its recommended about edge — the
missing-recommended-edge tripwire target.

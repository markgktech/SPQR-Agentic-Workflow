---
id: demo-n6
kind: decision
status: active
title: A decision that over-relates
scope: ui
origin: decided
timestamp: 2026-06-02T09:10:00Z
ticket: DEMO-5
agent: Praetor
schema_version: 1
edges:
  - type: relates-to
    target: demo-n1
  - type: relates-to
    target: demo-n2
  - type: relates-to
    target: demo-n3
  - type: relates-to
    target: demo-n5
  - type: relates-to
    target: demo-n7
  - type: relates-to
    target: demo-n8
---

Deliberately broken fixture (A16): a decision carrying six relates-to edges
(> K=5) — the relates-to overuse tripwire target. relates-to is any->any, so a
decision may legally emit it; the smell is the count, not the kind.

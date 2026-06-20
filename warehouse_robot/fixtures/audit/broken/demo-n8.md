---
id: demo-n8
kind: constraint
status: active
title: Inherited UI spacing rule
scope: ui
origin: inherited
timestamp: 2026-06-02T09:20:00Z
source: design-system
schema_version: 1
edges:
  - type: constrains
    target: demo-n1
---

A clean connected constraint (constrains demo-n1) — another relates-to target
for demo-n6 that must not itself trip any tripwire.

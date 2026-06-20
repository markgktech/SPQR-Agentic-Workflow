---
id: demo-n7
kind: decision
status: active
title: A derived tooling decision
scope: tooling
origin: decided
timestamp: 2026-06-02T09:15:00Z
ticket: DEMO-6
agent: Praetor
schema_version: 1
edges:
  - type: derived-from
    target: demo-n1
---

A clean connected decision (derived-from demo-n1) — a relates-to target for
demo-n6 that must not itself trip any tripwire.

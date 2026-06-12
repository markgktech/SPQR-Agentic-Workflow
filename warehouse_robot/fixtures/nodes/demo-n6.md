---
id: demo-n6
kind: lesson
status: active
title: Raw errors leaked across the service boundary
verdict: RED
origin: observed
timestamp: 2026-06-04T09:00:00Z
ticket: DEMO-4
agent: Quaestor
schema_version: 1
edges:
  - type: about
    target: demo-n2
---

A service threw a raw error past the boundary the typed-envelope decision
defines, crashing the caller. This lesson is part of what motivated the
superseding decision demo-n7.

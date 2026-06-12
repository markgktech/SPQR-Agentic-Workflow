---
id: demo-n4
kind: constraint
status: active
title: Strict concurrency isolation applies to all services
scope: concurrency
origin: inherited
timestamp: 2026-06-01T10:05:00Z
source: Swift 6.2 strict concurrency mode
schema_version: 1
edges:
  - type: constrains
    target: demo-n2
---

Platform-inherited rule: service types must declare their isolation; the
error-envelope decision must stay Sendable across actor boundaries.

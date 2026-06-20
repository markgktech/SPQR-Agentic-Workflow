---
id: demo-n3
kind: lesson
status: active
title: Async retries need idempotency keys
origin: observed
timestamp: 2026-06-01T09:10:00Z
ticket: DEMO-2
agent: Probator
schema_version: 1
edges:
  - type: about
    target: demo-n1
---

A lesson WITH its recommended about edge — the compliant-lesson control that
must NOT trip the missing-recommended-edge tripwire.

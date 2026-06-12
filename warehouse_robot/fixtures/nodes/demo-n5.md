---
id: demo-n5
kind: lesson
status: active
title: Offline cache invalidation was missed on first pass
verdict: YELLOW
origin: observed
timestamp: 2026-06-03T14:00:00Z
ticket: DEMO-3
agent: Praetor
schema_version: 1
edges:
  - type: about
    target: demo-n1
---

While implementing the local-first store, cache invalidation on schema
change was forgotten and caught in review. Caught by Probator; the subject
agent is recorded in the agent field, the catcher stays in prose (S5).

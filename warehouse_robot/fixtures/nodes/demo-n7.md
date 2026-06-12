---
id: demo-n7
kind: decision
status: active
title: Adopt result-based error envelopes
scope: error-handling
origin: decided
timestamp: 2026-06-05T09:30:00Z
ticket: DEMO-5
agent: Praetor
schema_version: 1
edges:
  - type: supersedes
    target: demo-n2
  - type: derived-from
    target: demo-n1
  - type: resolves
    target: demo-f2
---

Replaces the typed-envelope rule with Result-based envelopes that cannot
be bypassed by throwing. Derived from the local-first decision because
offline operation forces explicit error surfacing. Also resolves the open
contradiction flag demo-f2.
